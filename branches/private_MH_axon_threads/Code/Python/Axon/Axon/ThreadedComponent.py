#!/usr/bin/env python2.3
#
#      TODO: Thread shutdown
#      TODO: How to allow the thread to start new components?
#            (ie we only yield 1, not a newComponent or any value from the
#            thread.)
#      TODO: Number of minor issues fixed - thread shutdown is an issue though!
#            Added simple trace statements into the code.
#
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

from Component import component
from Microprocess import microprocess
import threading
import Queue

class threadedcomponent(component):
    """\
    Revised threading component
    """
    
    def __init__(self):
        super(threadedcomponent,self).__init__()
        self._thethread = threading.Thread(target=self.main)
        self._microprocess__thread = self._microprocessGenerator(self,"_localmain")
        
        self._inbox_queues = {}
        for name in self.inboxes:
            self._inbox_queues[name] = Queue.Queue()
            
        self._outbox_queues = {}
        for name in self.outboxes:
            self._outbox_queues[name] = Queue.Queue()
            
    def _localmain(self):
        """Placeholder microprocess, representing the thread, in the 'main' scheduler"""
        self._thethread.start()
        running = True
        while running:
            running = self._thethread.isAlive()
            
            for boxname in self.inboxes:
                while component.dataReady(self, boxname):
                    msg = component.recv(self, boxname)
                    self._inbox_queues[boxname].put_nowait(msg)
                    
            for boxname in self.outboxes:
                while self._outbox_queues[boxname].qsize():
                    msg = self._outbox_queues[boxname].get_nowait()
                    component.send(self, msg, boxname)
                    
            yield 1
            
    # write your own main function body

    def dataReady(self, boxname="inbox"):
        return self._inbox_queues[boxname].qsize()
    
    # anyready doesn't need rewrite
    
    def recv(self, boxname="inbox"):
        return self._inbox_queues[boxname].get_nowait()
    
    def send(self, message, boxname="outbox"):
        self._outbox_queues[boxname].put_nowait(message)
    
    def pause(self):
        # overriding this, can be more clever later if we want
        return
    


from AdaptiveCommsComponent import _AdaptiveCommsable as _NonThreadedableAdaptiveCommsable

class _AdaptiveCommsable(_NonThreadedableAdaptiveCommsable):
   def addInbox(self,*args):
       name = super(_AdaptiveCommsable,self).addInbox(*args)
       self._inbox_queues[name] = Queue.Queue()
       return name

   def deleteInbox(self,name):
       super(_AdaptiveCommsable,self).deleteInbox(name)
       del self._inbox_queues[name]

   def addOutbox(self,*args):
       name = super(_AdaptiveCommsable,self).addOutbox(*args)
       self._outbox_queues[name] = Queue.Queue()
       return name

   def deleteOutbox(self,name):
       super(_AdaptiveCommsable,self).deleteOutbox(name)
       del self._outbox_queues[name]


class ThreadedAdaptiveCommsComponent(threadedcomponent, _AdaptiveCommsable):
   def __init__(self):
      threadedcomponent.__init__(self)
      _AdaptiveCommsable.__init__(self)



if __name__ == "__main__":
    import time, sys
    
    class TheThread(threadedcomponent):
        def main(self):
            t = time.time()
            for i in range(10):
                while time.time() < t:
                    pass
                t=t+1.0
                self.send("Threaded: "+str(i)+"\n")
                
    class NotThread(component):
        def main(self):
            t = time.time()
            for i in range(20):
                while time.time() < t:
                    yield 1
                t=t+0.5
                self.send("Normal: "+str(i)+"\n")
                    
    class Outputter(component):
        def main(self):
            count=30
            while count:
                yield 1
                if self.dataReady("inbox"):
                    data = self.recv("inbox")
                    sys.stdout.write(str(data))
                    sys.stdout.flush()
                    count=count-1
            self.send("DONE","signal")

    class AAThread(ThreadedAdaptiveCommsComponent):
        def main(self):
            outs = {}
            
            t = time.time()
            for i in range(10):
                while time.time() < t:
                    pass
                t=t+1.0
                while self.dataReady("inbox"):
                    dst = self.recv("inbox")
                    newname = self.addOutbox("sink")
                    linkage = self.link( (self, newname), dst )
                    outs[newname] = linkage
                
                for o in outs.keys():
                    self.send("AAThread "+o+": "+str(i)+"\n", o)
                    
            for o in outs.keys():
                self.unlink( outs[o] )
                self.deleteOutbox(o)
    
    class OneShot(component):
        def __init__(self,msg):
            super(OneShot,self).__init__()
            self.msg = msg
            
        def main(self):
            self.send( self.msg )
            yield 1
    
    class Container(component):
        def main(self):
            t = TheThread().activate()
            n = NotThread().activate()
            out = Outputter().activate()
            self.link( (t,"outbox"), (out,"inbox") )
            self.link( (n,"outbox"), (out,"inbox") )
            
            self.link( (out,"signal"), (self,"control") )
            
            o = OneShot( msg=(out,"inbox") ).activate()
            a = AAThread().activate()
            self.link( (o,"outbox"), (a,"inbox") )
            
            while not self.dataReady("control"):
                self.pause()
                yield 1
                
    c = Container().run()
