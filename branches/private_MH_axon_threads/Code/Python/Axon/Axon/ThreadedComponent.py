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
      Component.component.__init__(self)
      
      self._thethread = threading.Thread(target=self.main)
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
      """STUB - Override this to do the work that will block.  Access the in and out
         queues that pass on to the in and out boxes.  You should read from all
         inqueues
      """
      while 1:
         for box in self.inqueues.iterkeys():
            self.outqueues["outbox"].put("ba")
            while not self.inqueues[box].empty():
                   self.outqueues["outbox"].put("dada:" + self.inqueues[box].get())
         self.outqueues["outbox"].put("doing")
         time.sleep(1)
      
   def _localmain(self):
       """Do not overide this unless you reimplement the pass through of the boxes to the threads.
       """
       self._thethread.start()
       running = True
       while running:
          # decide if we need to stop...
          running = self._thethread.isAlive()
          # ...but we'll still flush queue's through:
          # (must make sure we flush ALL messages from each queue)
          
          for box in self.inboxes:
              while self.dataReady(box):
                  msg = self.recv(box)
                  self.inqueues[box].put(msg)
                  
          for box in self.outboxes:
              while not self.outqueues[box].empty():
                  msg = self.outqueues[box].get()
                  self.send(msg, box)
                  
          while not self.threadtoaxonqueue.empty():
              msg = self.threadtoaxonqueue.get()
              if isinstance(msg, newComponent):
                  # If new components have been created and need to be added to the run queue
                  # It might be best that more of the work of adding children is done here to avoid
                  # race conditions.
                  yield msg # yield for the scheduler to add to list of running components.

          yield 1

if __name__ == "__main__":
    import time, sys
    
    class TheThread(threadedcomponent):
        def main(self):
            self.send("ADD SRC")
            t = time.time()
            for i in range(10):
                while time.time() < t:
                    pass
                t=t+1.0
                self.send("Threaded: "+str(i))
            self.send("DEL SRC")
                
    class NotThread(Component.component):
        def main(self):
            self.send("ADD SRC")
            t = time.time()
            for i in range(20):
                while time.time() < t:
                    yield 1
                t=t+0.5
                self.send("Normal: "+str(i))
            self.send("DEL SRC")
                    
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
            out = Outputter().activate()
            self.link( (t,"outbox"), (out,"inbox") )
            self.link( (n,"outbox"), (out,"inbox") )
            
            self.link( (out,"outbox"), (self,"inbox") )
            
            # wait until outputter sends us a signal its finished
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
                
    c = Container().run()
