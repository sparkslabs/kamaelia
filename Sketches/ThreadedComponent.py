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

import threading
import Queue
import time
import Axon.Component

class _componentthread(threading.Thread):
   """Represents the thread object that will be run. This is a bodge to
      avoid multiple inheritance, essentially a bounceback through to the
      passed component that is to be run as a thread not as a generator.
   """
   def __init__(self, componentToRun=None):
      threading.Thread.__init__(self)
      self.componentToRun  = componentToRun
      
   def run(self):
      self.componentToRun.run()
      
class threadedcomponent(Axon.Component.component):
   """This component is intended to allow blocking calls to be made from within
      a component by running them inside a thread in the component.
   """

   def __init__(self,queuelengths=10):
      self.__super.__init__()
      thethread = _componentthread(self)

      self.queuelengths = queuelengths
      self.inqueues = dict()
      self.outqueues = dict()
      for box in self.inboxes.iterkeys():
         self.inqueues[box] = Queue.Queue(self.queuelengths)
      for box in self.outboxes.iterkeys():
         self.outqueues[box] = Queue.Queue(self.queuelengths)

      self.outbuffer = dict()
      for box in self.outboxes:
         self.outbuffer[box] = None

      self.finished = False
      thethread.start()
   
   def run(self):
      """STUB - Override this to do the work that will block.  Access the in and out
         queues that pass on to the in and out boxes.  You should read from all
         inqueues
      """
      while 1:
         for box in self.inqueues.iterkeys():
            print "ba",
            while not self.inqueues[box].empty():
               print "dada:", self.inqueues[box].get(),
         print "doing"
         time.sleep(1)
      
   def main(self):
      """Do not overide this unless you reimplement the pass through of the boxes to the threads.
      """

      while 1:
         for box in self.inboxes:
            if(self.dataReady(box)):
               if(not self.inqueues[box].full()): # LBYL, but no race hazard
                  self.inqueues[box].put(self.recv(box))

         for box in self.outboxes:
            if self.outbuffer.has_key(box):
               try:
                  self.send(self.outbuffer[box], box)
               except noSpaceInBox:
                  continue # Skip to next box, since outbox full
               del self.outbuffer[box]

            while(not self.outqueues[box].empty()):
               sending = self.outqueues[box].get()
               try:
                  self.send(sending,box)
               except noSpaceInBox:
                  self.outbuffer[box] = sending
                  break

         yield 1
      
if __name__ == '__main__':
   from Axon.Scheduler import scheduler

   tc = threadedcomponent()
   tc.activate()
   tc._deliver("hello","inbox")
   tc._deliver("world","inbox")
   tc._deliver("foo","inbox")
   scheduler.run.runThreads(slowmo=0)
