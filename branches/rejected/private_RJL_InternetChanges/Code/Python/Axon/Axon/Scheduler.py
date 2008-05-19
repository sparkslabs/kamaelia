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
import Queue
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

_ACTIVE       = object()        # microprocess is active (is in the runqueue)
_SLEEPING     = object()        # microprocess is paused (is not in the runqueue)
_GOINGTOSLEEP = object()        # microprocess to be paused (should be removed from the runqueue)

class scheduler(microprocess):
   """Scheduler - runs microthreads of control."""
   run = None
   def __init__(self):
      """Creates a scheduler object. If scheduler.run has not been set, sets it.
      Class initialisation ensures that this object/class attribute is initialised - client
      modules always have access to a standalone scheduler.
      Internal attributes:
         * time = time when this object was last active.
         * threads = set of threads to be run, including their state - whether active or sleeping(paused)
      Whilst there can be more than one scheduler active in the general case you will NOT
      want to create a custom scheduler.
      """
      super(scheduler, self).__init__()
      if not scheduler.run:         # If no scheduler already allocated...
         scheduler.run = self       # Make this scheduler the singleton scheduler.

      self.time = time.time()
      
      self.threads = {}    # current set of threads and their states (whether sleeping, or running)
      self.wakeRequests = Queue.Queue()
      self.pauseRequests = Queue.Queue()

   def _addThread(self, mprocess):
      """A Microprocess adds itself to the runqueue using this method, using
      the mannerism scheduler.run._addThread(). Generally components will *not*
      use this method to activate themselves, see the component class to see
      how you do that.
      """
      self.wakeThread(mprocess, True)
      
   def wakeThread(self, mprocess, canActivate=False):
      """\
      wakeThread(mprocess[,canActivate]) - request to wake a sleeping mprocess.
      
      If sleeping or already active, the specified microprocess will be ensured
      to be active on the next cycle through the scheduler.
      
      If the microprocess is not running yet then it will not be woken, unless
      canActivate = True (default is False).
      """
      self.wakeRequests.put( (mprocess, canActivate) )
      
   def pauseThread(self, mprocess):
       """\
       pauseThread(mprocess) - request to put a mprocess to sleep.
       
       If active, or already sleeping, the specified microprocess will be put
       to leep on the next cycle through the scheduler.
       """
       self.pauseRequests.put( mprocess )

   def isThreadPaused(self, mprocess):
       """\
       Returns True if the specified microprocess is sleeping, or the scheduler
       does not know about it.
       """
       return self.threads.get(mprocess, _SLEEPING) == _SLEEPING
       # doesn't include _GOINGTOSLEEP (inference is the thread isn't asleep yet!)
   
   def listAllThreads(self):
       """Returns a list of all microprocesses (both active and sleeping)"""
       return self.threads.keys()
   
   def handleMicroprocessShutdownKnockon(self, knockon):
     if isinstance(knockon, shutdownMicroprocess):
        for i in xrange(len(self.threads)):
           if self.threads[i] in knockon.microprocesses():
              self.threads[i] = None
              
     if isinstance(knockon, reactivate):
         self._addThread(knockon.original)

   def main(self,slowmo=0,canblock=False):
       """\
       main([slowmo][,canblock]) - Scheduler main loop generator
       
       Each pass through this generator does two things:
       * one pass through all active microprocesses, giving executing them.
       * processing of wake/sleep requests
       
       slowmo specifies a delay (in seconds) before the main loop is run.
       slowmo defaults to 0.
       
       If canblock is True, this generator will briefly) block if there are
       no active microprocesses, otherwise it will return immediately (default).
       
       This generator terminates when there are no microprocesses left to run.
       """
       nextrunqueue = []
       running = True
       
       while running:
           sched_yield()
           
           # slowmo
           now = time.time()
           until = now + slowmo
           if canblock:
               time.sleep(until-now)
           else:
               while now < until:
                   yield 1
                   now = time.time()
           
           self.time = now   # set "time" attribute for benefit for microprocesses
           
           runqueue = nextrunqueue
           nextrunqueue = []
           
           # run microprocesses in the runqueue
           for mprocess in runqueue:
               yield 1
               
               if self.threads[mprocess] == _ACTIVE:
                   try:
                       result = mprocess.next()
                       
                       if isinstance(result, newComponent):
                           for c in result.components():
                               c.activate()
                       if isinstance(result, WaitComplete):
                           newThread = microprocess(result.args[0], reactivate(mprocess))
                           newThread.activate()
                           del self.threads[mprocess]
                           mprocess = None
                           
                       if mprocess:
                           nextrunqueue.append(mprocess)
                   except StopIteration:
                       del self.threads[mprocess]
                       mprocess.stop()
                       knockon = mprocess._closeDownMicroprocess()
                       self.handleMicroprocessShutdownKnockon(knockon)
               else:
                   self.threads[mprocess] = _SLEEPING

           # make sure, even if there weren't any micprocesses active, we yield
           # control at least once
           yield 1
           
           # process pause requests first - to prevent race conditions, we do
           # wakeup requests second - safer to leave a thread awake than asleep
           while not self.pauseRequests.empty():
               mprocess = self.pauseRequests.get()
               self.threads[mprocess] = _GOINGTOSLEEP
               # marked as going to sleep, rather than asleep since mprocess
               # is still in runqueue (more efficient to leave it to be
               # removed when we iterate through the runqueue)
           
           allsleeping = len(self.threads) > 0 and len(nextrunqueue) == 0
           
           while (allsleeping and canblock) or not self.wakeRequests.empty():
               
               # process requests to wake threads
               try:
                    # wait for wakeup requests, blocks but with a
                    # modest timeout so we still regularly yield (in case this
                    # is a microprocess running in another scheduler)
                    mprocess, canActivate = self.wakeRequests.get(True,0.01)
                    try:
                        currentstate = self.threads[mprocess]
                        if currentstate == _SLEEPING:
                            nextrunqueue.append(mprocess)
                        allsleeping = False
                        self.threads[mprocess] = _ACTIVE
                    except KeyError:
                        # not activated, can we?
                        if canActivate:
                            nextrunqueue.append(mprocess)
                            self.threads[mprocess] = _ACTIVE

               except Queue.Empty:
                    # catch timeout
                    pass
           
           running = len(self.threads)
               
   def runThreads(self,slowmo=0):
      for i in self.main(slowmo,canblock=True): pass

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

