#!/usr/bin/env python2.3
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
"""Kamaelia Concurrency Component Framework.

SCHEDULER

You provide the scheduler with microthreads of microprocesses,
and it runs them, clean and simple. This is usually handled by the component
system via returning a newComponent value. An alternative is to call the
component's activate method.

It also has a slow motion mode designed to help with debugging & testing.

"""
import time
import gc as _gc

from util import removeAll
from idGen import strId, numId
from debug import debug
from Microprocess import microprocess
from Axon import AxonObject as _AxonObject
from Ipc import *
try:   
    from ctypes import *   
    libc = cdll.LoadLibrary("/lib/libc.so.6")   
    sched_yield = libc.sched_yield   
except ImportError:   
    def sched_yield(): pass

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
      super(scheduler, self).__init__()
      if not scheduler.run:         # If no scheduler already allocated...
         scheduler.run = self       # Make this scheduler the singleton scheduler.

      self.time = time.time()
      self.threads = list()     # Don't use [] to avoid Python wierdness
      self.newthreads = list()

   def _addThread(self, mprocess):
      """A Microprocess adds itself to the runqueue using this method, using
      the mannerism scheduler.run._addThread(). Generally components will *not*
      use this method to activate themselves, see the component class to see
      how you do that.
      """
      self.newthreads.append(mprocess)

   def handleMicroprocessShutdownKnockon(self, knockon):
     if isinstance(knockon, shutdownMicroprocess):
        for i in xrange(len(self.threads)):
           if self.threads[i] in knockon.microprocesses():
              self.threads[i] = None
              
     if isinstance(knockon, reactivate):
        self._addThread(knockon.original)

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
      nor guaranteed and can be extended by threads that take too long to;
      complete. (Think of it as a "hello world" of soft-real time scheduling)"""

      yield 1
      
      while len(self.newthreads) > 0:
         now = time.time()
         if (now - self.time) > slowmo or slowmo == 0:
             self.threads=self.newthreads     # Make the new runset the run set
             self.newthreads = list()         # We go through all the threads,
                                              # if they don't exit they get put here.
             self.time = now   # Update last run time - only really useful if slowmo != 0
             for mprocess in self.threads:
                sched_yield()
                if mprocess:
                   try:
                      yield 1                       # Relinquish control between every thread
                      result = mprocess.next()      # Run the thread for a cycle. (calls the generator function)

                      if (isinstance(result, newComponent)):
                          for c in result.components():
                              c.activate()

                      if isinstance(result, WaitComplete):
                         newMprocess = microprocess(result.args[0], reactivate(mprocess))
                         newMprocess.activate()
                         mprocess = None
                      if mprocess:
                          self.newthreads.append(mprocess)    # Add the current thread to the new run set
                   except StopIteration:             # Thread exited
                      mprocess.stop() # set the stop flag on the microprocess, so anyone observing can see
                      knockon = mprocess._closeDownMicroprocess()
                      self.handleMicroprocessShutdownKnockon(knockon)

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
   a=foo()
   a.activate()
   print a
   scheduler.run.runThreads()

