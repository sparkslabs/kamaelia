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

def _makeThreadBox():
    return list()

class threadedcomponent(component):
    """\
    Revised threading component
    """
    
    def __init__(self):
        super(threadedcomponent,self).__init__()
        self._thethread = threading.Thread(target=self.main)
        self._microprocess__thread = self._microprocessGenerator(self,"_localmain")
        
        self._thread_inboxes = {}
        for name in self.inboxes:
            self._thread_inboxes[name] = _makeThreadBox()
        self._inbox_queue = Queue.Queue()
            
        self._thread_outboxes = {}
        for name in self.outboxes:
            self._thread_outboxes[name] = _makeThreadBox()
        self._outbox_queue = Queue.Queue()
            
        self._cmd = Queue.Queue()
        self._cmd_reply = Queue.Queue()
    
    def _localmain(self):
        """Placeholder microprocess, representing the thread, in the 'main' scheduler"""
        self._thethread.start()
        running = True
        while running:
            running = self._thethread.isAlive()
            
            for boxname in self.inboxes:
                while component.dataReady(self, boxname):
                    msg = component.recv(self, boxname)
                    self._inbox_queue.put_nowait( (boxname, msg) )
                    
            for boxname in self.outboxes:
                # for loop to snapshot of queue length to guarantee we stop!
                for i in xrange(0, self._outbox_queue.qsize() ):
                    (boxname, msg) = self._outbox_queue.get_nowait()
                    component.send(self, msg, boxname)
            
            if self._cmd.qsize():
                cmd, argL, argD = self._cmd.get()
                result = cmd(*argL,**argD)
                self._cmd_reply.put_nowait(result)
            
            
            yield 1
    
    def _process_queues(self):
        # process data arriving at the thread end of the queues
        
        # deliver messages into local inboxes
        for i in xrange(0, self._inbox_queue.qsize()) :
            (boxname, msg) = self._inbox_queue.get_nowait()
            self._thread_inboxes[boxname].append(msg)
    
    # write your own main function body

    def dataReady(self, boxname="inbox"):
        self._process_queues()
        return len(self._thread_inboxes[boxname])
    
    # anyready doesn't need rewrite
    
    def recv(self, boxname="inbox"):
        return self._thread_inboxes[boxname].pop(0)
    
    def send(self, message, boxname="outbox"):
        self._outbox_queue.put_nowait( (boxname, message) )
    
    def pause(self):
        # overriding this, can be more clever later if we want
        return
    
    def link(self, source,sink,passthrough=0):
        cmd = (component.link, [self,source,sink,passthrough], {} )
        self._cmd.put_nowait(cmd)
        return self._cmd_reply.get()
        
    def unlink(self, thecomponent=None, thelinkage=None):
        cmd = (component.unlink, [self,thecomponent,thelinkage], {} )
        self._cmd.put_nowait(cmd)
        return self._cmd_reply.get()


from AdaptiveCommsComponent import _AdaptiveCommsable as _NonThreadedableAdaptiveCommsable

class _AdaptiveCommsable(_NonThreadedableAdaptiveCommsable):
   def addInbox(self,*args):
       cmd = (self._unsafe_addInbox, args, {} )
       self._cmd.put_nowait(cmd)
       return self._cmd_reply.get()

   def _unsafe_addInbox(self,*args):
       name = super(_AdaptiveCommsable,self).addInbox(*args)
       self._thread_inboxes[name] = _makeThreadBox()
       return name

   def deleteInbox(self,name):
       cmd = (self._unsafe_deleteInbox, [name], {} )
       self._cmd.put_nowait(cmd)
       return self._cmd_reply.get()
   
   def _unsafe_deleteInbox(self,name):
       super(_AdaptiveCommsable,self).deleteInbox(name)
       del self._thread_inboxes[name]

   def addOutbox(self,*args):
       cmd = (self._unsafe_addOutbox, args, {} )
       self._cmd.put_nowait(cmd)
       return self._cmd_reply.get()
   
   def _unsafe_addOutbox(self,*args):
       name = super(_AdaptiveCommsable,self).addOutbox(*args)
       self._thread_outboxes[name] = _makeThreadBox()
       return name

   def deleteOutbox(self,name):
       cmd = (self._unsafe_deleteOutbox, [name], {} )
       self._cmd.put_nowait(cmd)
       return self._cmd_reply.get()
   
   def _unsafe_deleteOutbox(self,name):
       super(_AdaptiveCommsable,self).deleteOutbox(name)
       del self._thread_outboxes[name]


class threadedadaptivecommscomponent(threadedcomponent, _AdaptiveCommsable):
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
            count=40
            while count:
                yield 1
                if self.dataReady("inbox"):
                    data = self.recv("inbox")
                    sys.stdout.write(str(data))
                    sys.stdout.flush()
                    count=count-1
            self.send("DONE","signal")

    class AAThread(threadedadaptivecommscomponent):
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
