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

from __future__ import generators

import threading
import Queue
import time
import Component
from AxonExceptions import noSpaceInBox
from Ipc import newComponent

class threadedcomponent(Component.component,threading.Thread):
   """This component is intended to allow blocking calls to be made from within
      a component by running them inside a thread in the component.
   """

   def __init__(self,queuelengths=10):
      self.__super.__init__()
      threading.Thread.__init__(self)

      self.queuelengths = queuelengths
      self.inqueues = dict()
      self.outqueues = dict()
      for box in self.inboxes.iterkeys():
         self.inqueues[box] = Queue.Queue(self.queuelengths)
      for box in self.outboxes.iterkeys():
         self.outqueues[box] = Queue.Queue(self.queuelengths)

      self.outbuffer = dict()

      self.threadtoaxonqueue = Queue.Queue()
      self.axontothreadqueue = Queue.Queue()

      self.setDaemon(True) # means the thread is stopped if the main thread stops.
   
   def run(self):
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
         if not self.axontothreadqueue.empty():
            mesg = self.axontothreadqueue.get()
            if mesg == "StopThread":
               self.threadtoaxonqueue.put("ThreadStopped")
               break
         time.sleep(1)
      
   def main(self):
      """Do not overide this unless you reimplement the pass through of the boxes to the threads.
      """
      self.start()
      residualdata = False
      while 1:
         time.sleep(0)
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

         if residualdata:
            residualdata = False
            for box in self.outboxes:
               # This checks that there is no pending data that hasn't been put in an outbox
               # before allowing the component to die.
               if self.outbuffer.has_key(box) or not self.outqueues[box].empty():
                  residualdata = True
                  break
            if residualdata:
               continue # There is no point checking for communications from dead thread or
               # adding any more data to the thread.
            else:
               return # The thread has finished, all data has been sent and the component
                          # can be removed from the run queue.
         if not self.threadtoaxonqueue.empty():
         # Check for messages from internal thread.  It could loop through them but that 
         # would change the meaning of the continue statement from skipping the inbox
         #reading.
            m = self.threadtoaxonqueue.get()
            if isinstance(m, newComponent):
            # If new components have been created and need to be added to the run queue
            # It might be best that more of the work of adding children is done here to avoid
            # race conditions.
               yield m # yield for the scheduler to add to list of running components.
            elif m == "ThreadStopped":
            # See if thread has finished in which case the component should finish up and die
            # as soon as all the output from the thread is passed on and no longer pending
               residualdata = True # Assume there is data left to send and send it as soon as possible
               yield 1
               continue # This means we do not pass in more data destined for the dead thread
   
         for box in self.inboxes:
            if(self.dataReady(box)):
               if(not self.inqueues[box].full()): # LBYL, but no race hazard
                  self.inqueues[box].put(self.recv(box))

         yield 1

if __name__ == '__main__':
     def printoutbox(tc):
       tmp = ""
       while len(tc.outboxes["outbox"]) > 0 :
         #print tc._collect("outbox")
         tmp = tmp + tc._collect("outbox")
       print tmp


#   from Scheduler import scheduler
#   try:
     print "starting"
     tc = threadedcomponent()
#     tc.activate()
     print len(tc.outboxes["outbox"])
     axonthread = tc.main()
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     time.sleep(5)
     tc._deliver("hello","inbox")
     axonthread.next()
     printoutbox(tc) 
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     time.sleep(2)
     tc._deliver("world","inbox")
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     time.sleep(3)
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     tc._deliver("foo","inbox")
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     time.sleep(2)
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
     axonthread.next()
     printoutbox(tc)
#      scheduler.run.runThreads(slowmo=0)
#   except Exception, e:
#     print e
#     print "done"

