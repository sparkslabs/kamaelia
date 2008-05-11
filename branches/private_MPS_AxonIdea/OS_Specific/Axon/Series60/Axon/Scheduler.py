#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""Kamaelia Concurrency Component Framework.

SCHEDULER

You provide the scheduler with microthreads of microprocesses,
and it runs them, clean and simple. This is usually handled by the component
system via returning a newComponent value. An alternative is to call the
component's activate method.

It also has a slow motion mode designed to help with debugging & testing.

"""

from __future__ import generators

import time
#import gc as _gc

from util import removeAll
from idGen import strId, numId
#from debug import debug
from Microprocess import microprocess
from Axon import AxonObject as _AxonObject
from Ipc import *
import e32

def _sort(somelist):
   a=[ x for x in somelist]
   a.sort()
   return a

class scheduler(microprocess):
   """Scheduler - runs microthreads of control."""
   run = None
   def __init__(self):
      """Creates a scheduler object. If scheduler.run has not been set, sets it.
      Class initialisation ensures that this object/class attribute is initialised - client
      modules always have access to a standalone scheduler.
      Internal attributes:
         * time = time when this object was last active.
         * threads = list of threads to run.
      Whilst there can be more than one scheduler active in the general case you will NOT
      want to create a custom scheduler.
      """
      super(scheduler,self).__init__()
      if not scheduler.run:         # If no scheduler already allocated...
         scheduler.run = self       # Make this scheduler the singleton scheduler.

      self.time = time.time()
      self.threads = list()     # Don't use [] to avoid Python wierdness
#      assert self.debugger.note("scheduler.__init__", 1, "STARTED: ", self.name, self.id)

   def _addThread(self, mprocess):
      """A Microprocess adds itself to the runqueue using this method, using
      the mannerism scheduler.run._addThread(). Generally components will *not*
      use this method to activate themselves, see the component class to see
      how you do that.
      """
      self.threads.append(mprocess)

   def main(self,slowmo=0):
      """This is the meat of the scheduler  - this actively loops round the threads
      that it has available to run, and runs them. The only control over the scheduler
      at present is a means to slow it down - ie run in slow motion.
      The way this is runn is as follows:
      scheduler.run.runThreads(slowmo=/delay/)
      where delay is in seconds. If the delay is 0, the the system runs all the
      threads as fast as it can. If the delay is non zero - eg 0.5, then the system
      runs all the threads for one "cycle", waits until the delay has passed, and then
      times again. Note : the delay is between the start points of cycles, and not
      between the start and end points of cycles. The delay is NOT 100% accurate
      nor guaranteed and can be extended by threads that take too long to
      complete. (Think of it as a "hello world" of soft-real time scheduling)
      """
      crashAndBurnWithErrors = True
      mprocesses = self.threads          # Grab the singleton set of threads.
#      assert self.debugger.note("scheduler.main", 1, "SCHEDULER:",self)
#      assert self.debugger.note("scheduler.main", 1, "Scheduler Starting, # threads to run:")
#      assert self.debugger.note("scheduler.main", 1, "   ", len(self.threads) )

      yield 1
      running = len(self.threads) > 0
#      assert self.debugger.note("scheduler.main", 5, "THR", self.threads )
      cx=0
      lastcx=0
      lasttime = time.time()
      starttime= lasttime
#      assert self.debugger.note("scheduler.main", 5, "# CX Ave, CX this" )
      while(running):           # Threads gets re-assigned so this can reduce to []
        e32.ao_yield()
        now = time.time()
        if (now - self.time) > slowmo or slowmo == 0:
         self.time = now   # Update last run time - only really useful if slowmo != 0
#         assert self.debugger.note("scheduler.main.threads", 1, "Threads to run:", len(self.threads) )

#         assert self.debugger.note("scheduler.main.threads", 2, "Threads to run:", _sort([ thr.name for thr in self.threads if thr is not None]))
#         assert self.debugger.note("scheduler.objecttrack", 5, "Axon Objects active", len([ str(x) for x in _gc.get_objects() if isinstance(x, _AxonObject) ]))
#         assert self.debugger.note("scheduler.objecttrack", 10, "Axon Objects active", "\n           ".join([ str(x.__class__) for x in _gc.get_objects() if isinstance(x, _AxonObject) ]))
#         assert self.debugger.note("scheduler.objecttrack", 15, "Axon Objects active", "\n           ".join([ str(x) for x in _gc.get_objects() if isinstance(x, _AxonObject) ]))
         newthreads = list()  # We go through all the threads,
                              # if they don't exit they get put here.

#         assert self.debugger.note("scheduler.scheduler",1,"SCHEDULED", self.name,self.id)
         activeMicroprocesses = 0
         for mprocess in self.threads:
            e32.ao_yield()
            cx=cx+1
            if (now - lasttime)> 1:
#                 assert self.debugger.note("scheduler.main", 10, cx/(now-starttime), ",", cx-lastcx )
                 lasttime = now
                 lastcx=cx
            if mprocess:
               try:
#                  assert self.debugger.note("scheduler.main", 10, "Scheduler about to yield",self)
                  yield 1                       # Relinquish control between every thread

#                  assert self.debugger.note("scheduler.main", 10, "Scheduler back yield",self)
                  result = mprocess.next()      # Run the thread for a cycle. (calls the generator function)

                  if (issubclass(result.__class__, newComponent)):
                     # The class sent us a newComponent message, which
                     # can contain several components.
                     for component in result.components():   # For each one
#                        assert self.debugger.note("scheduler.main", 5, "Starting a new component",component)
                        t = component.activate()      # Activate it - adds itself to the runset
                        if t._activityCreator():
                           activeMicroprocesses +=1
                  if mprocess._activityCreator():
                     activeMicroprocesses +=1
                  newthreads.append(mprocess)    # Add the current thread to the new run set
               except StopIteration:             # Thread exited
#                  assert self.debugger.note("scheduler.main", 5, "STOP ITERATION THROWN", mprocess)
                  knockon = mprocess._closeDownMicroprocess()
                  if knockon:
#                     assert self.debugger.note("scheduler.main", 5, "KNOCKON", knockon)
                     if isinstance(knockon, shutdownMicroprocess):
#                        assert self.debugger.note("scheduler.main", 5, "TO CLOSEDOWN", [(x.name,x.debugname) for x in knockon.microprocesses() ])
                        for i in xrange(len(self.threads)):
                           if self.threads[i] in knockon.microprocesses():
                              self.threads[i] = None
                        # In-efficient first pass at handling knockon threads without having expensive deletions.
                        #for i in xrange(len(newthreads)):
                        #   if newthreads[i] in knockon.microprocesses():
                        #      newthreads[i] = None
               self.threads=newthreads             # Make the new runset the run set
               #_gc.collect()
            running = activeMicroprocesses > 0

   def runThreads(self,slowmo=0):
      for i in self.main(slowmo): pass

microprocess.setSchedulerClass(scheduler)
scheduler() # Initialise the class.

if __name__ == '__main__':
   print "This code current has no test code"
   class foo(microprocess):
      def main(self):
         while 1:
            yield 1
      def _activityCreator(self):
         return True
   a=foo()
   a.activate()
   print a
   scheduler.run.runThreads()

