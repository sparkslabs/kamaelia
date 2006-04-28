#!/usr/bin/env python
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

from __future__ import generators

import threading
import Queue
import time
import Component
from AxonExceptions import noSpaceInBox
from Ipc import newComponent

class threadedcomponent(Component.component):
   """This component is intended to allow blocking calls to be made from within
      a component by running them inside a thread in the component.
   """

   def __init__(self):
      super(threadedcomponent,self).__init__()
      
      self._thethread = threading.Thread(target=self.main)
      self._threadrunning = False
      self._microprocess__thread = self._microprocessGenerator(self,"_localmain")

      self.inqueues = dict()
      self.outqueues = dict()
      for box in self.inboxes.iterkeys():
         self.inqueues[box] = Queue.Queue()
      for box in self.outboxes.iterkeys():
         self.outqueues[box] = Queue.Queue()

      self.outbuffer = dict()

      self.threadtoaxonqueue = Queue.Queue()
      self.axontothreadqueue = Queue.Queue()

      self._thethread.setDaemon(True) # means the thread is stopped if the main thread stops.
   
   def main(self):
      """'C.main()' **You normally will not want to override or call this method**
      This is the function that gets called by microprocess. If you override
      this do so with care. If you don't do it properly, your initialiseComponent,
      mainBody & closeDownComponent parts will not be called. Ideally you
      should not NEED to override this method. You also should not call this
      method directly since activate does this for you in order to create a
      microthread of control.

      """
      self.initialiseComponent()
      result=1
      while (result):
         result = self.mainBody()
      self.closeDownComponent()

   def initialiseComponent(self):
      """Stub method. **This method is designed to be overridden.** """
      return 1
   def mainBody(self):
      """Stub method. **This method is designed to be overridden.** """
      return None
   def closeDownComponent(self):
      """Stub method. **This method is designed to be overridden.** """
      return 1


   def _localmain(self):
       """Do not overide this unless you reimplement the pass through of the boxes to the threads.
       """

       # start the thread
       self._thethread.start()
       running = True
       self._threadrunning = True
       while running:
          # decide if we need to stop...
          running = self._thethread.isAlive()
          # ...but we'll still flush queue's through:
          # (must make sure we flush ALL messages from each queue)
          
          # decide how many requests from the thread that we'll handle
          # before flushing queues
          # If we don't consider: a thread puts item in an outqueue then issues
          # a command to delete that queue. It does this *after* we've checked 
          # outqueues, but *before* we process threadtoaxonqueue. That item
          # in the outqueue would be lost.
          # This way we guarantee flushing any queue activity done by the thread
          # before the command
          msgcount = self.threadtoaxonqueue.qsize()
          
          for box in self.inboxes:
              while self._nonthread_dataReady(box):
                  msg = self._nonthread_recv(box)
                  self.inqueues[box].put(msg)
                  
          for box in self.outboxes:
              while not self.outqueues[box].empty():
                  msg = self.outqueues[box].get()
                  self._nonthread_send(msg, box)
                  
          for i in range(0,msgcount):
              msg = self.threadtoaxonqueue.get()
              self._handlemessagefromthread(msg)

          yield 1
       self._threadrunning = False

   def _handlemessagefromthread(self,msg):
       """STUB - for handling messages from the thread"""
       (cmd, argL, argD) = msg
       result = cmd(*argL,**argD)
       self.axontothreadqueue.put(result)

   _nonthread_dataReady = Component.component.dataReady
   _nonthread_recv      = Component.component.recv
   _nonthread_send      = Component.component.send

   def dataReady(self,boxname="inbox"):
       return self.inqueues[boxname].qsize()

   def recv(self,boxname="inbox"):
       return self.inqueues[boxname].get()

   def send(self,message, boxname="outbox"):
       self.outqueues[boxname].put(message)


from AdaptiveCommsComponent import _AdaptiveCommsable as _AC


class threadedadaptivecommscomponent(threadedcomponent, _AC):
    def __init__(self):
        threadedcomponent.__init__(self)
        _AC.__init__(self)

    def addInbox(self,*args):
        name = super(threadedadaptivecommscomponent,self).addInbox(*args)
        self.inqueues[name] = Queue.Queue()
        return name
    
    def deleteInbox(self,name):
        super(threadedadaptivecommscomponent,self).deleteInbox(name)
        del self.inqueues[name]
    
    def addOutbox(self,*args):
        if self._threadrunning:
            # call must be synchronous (wait for reply) because there is a reply
            # and because next instruction in thread might assume this outbox
            # exists
            cmd = (self._unsafe_addOutbox, args, {} )
            self.threadtoaxonqueue.put( cmd )
            return self.axontothreadqueue.get()
        else:
            return self._unsafe_addOutbox(*args)
        
    def _unsafe_addOutbox(self,*args):
        name = super(threadedadaptivecommscomponent,self).addOutbox(*args)
        self.outqueues[name] = Queue.Queue()
        return name
    
    def deleteOutbox(self,name):
        if self._threadrunning:
            # call must be synchronous (wait for reply) because there is a reply
            # and because next instruction in thread might assume this outbox
            # is destroyed.
            cmd = (self._unsafe_deleteOutbox, [name], {} )
            self.threadtoaxonqueue.put( cmd )
            return self.axontothreadqueue.get()
        else:
            self._unsafe_deleteOutbox(self,name)
        
    def _unsafe_deleteOutbox(self,name):
        super(threadedadaptivecommscomponent,self).deleteOutbox(name)
        del self.outqueues[name]


if __name__ == "__main__":
    import time, sys
    
    class TheThread(threadedcomponent):
        def main(self):
            self.send("ADD SRC")
            for i in range(10):
                time.sleep(1.0)
                self.send("Threaded: "+str(i))
            self.send("DEL SRC")
                
    class FSMThread(threadedcomponent):
        def initialiseComponent(self):
            self.count=10
            self.send("ADD SRC")
        def mainBody(self):
            time.sleep(1.0)
            self.send("FSMThread: "+str(self.count))
            self.count=self.count-1
            return self.count
        def closeDownComponent(self):
            self.send("DEL SRC")
            
    class NotThread(Component.component):
        def main(self):
            self.send("ADD SRC")
            for i in range(20):
                t=time.time()+0.5
                while time.time() < t:
                    yield 1
                self.send("Normal: "+str(i))
                yield 1
            self.send("DEL SRC")
                    
    class AAThread(threadedadaptivecommscomponent):
        def add(self,dst):
            newname = self.addOutbox("sink")
            linkage = self.link( (self, newname), dst )
            self.destinations[newname] = (dst, linkage)
            self.send("ADD SRC", newname)
            
        def rem(self,dst):
            box,linkage = [(box,linkage) for (box,(d,linkage)) in self.destinations.items() if d==dst][0]
            del self.destinations[box]
            self.send("DEL SRC", box)
            self.unlink(linkage)
            self.deleteOutbox(box)
            
        def main(self):
            self.destinations = {}
            
            for i in range(10):
                time.sleep(1.0)
                while self.dataReady("inbox"):
                    cmd,dst = self.recv("inbox")
                    if cmd=="ADD":
                        self.add(dst)
                    elif cmd=="DEL":
                        self.rem(dst)
                
                for box in self.destinations:
                    self.send("AAThread "+box+": "+str(i)+"\n", box)
                    
            for dst, _ in self.destinations.values():
                self.rem(dst)
    
    class OneShot(threadedcomponent):
        def __init__(self,msg,delay=0):
            super(OneShot,self).__init__()
            self.msg = msg
            self.delay = delay
            
        def main(self):
            time.sleep(self.delay)
            self.send( self.msg )
    
    class Outputter(Component.component):
        def main(self):
            refcount = 0
            done=False
            while not done:
                yield 1
                if self.dataReady("inbox"):
                    data = self.recv("inbox")
                    if data=="ADD SRC":
                        refcount = refcount+1
                    elif data=="DEL SRC":
                        refcount = refcount-1
                        if refcount == 0:
                            done=True
                    sys.stdout.write(str(data)+"\n")
                    sys.stdout.flush()
            self.send("DONE","outbox")

    
    class Container(Component.component):
        def main(self):
            t = TheThread().activate()
            n = NotThread().activate()
            f = FSMThread().activate()
            out = Outputter().activate()
            self.link( (t,"outbox"), (out,"inbox") )
            self.link( (n,"outbox"), (out,"inbox") )
            self.link( (f,"outbox"), (out,"inbox") )
            
            self.link( (out,"outbox"), (self,"inbox") )
            
            a = AAThread().activate()
            start = OneShot(msg=("ADD",(out,"inbox")),delay=0.5).activate() # first received is a '0'
            stop = OneShot(msg=("DEL",(out,"inbox")),delay=5.5).activate() # last received is a '4'
            self.link( (start,"outbox"), (a,"inbox") )
            self.link( (stop,"outbox"), (a,"inbox") )
            
            # wait until outputter sends us a signal its finished
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
                
    c = Container().run()
