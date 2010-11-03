#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
====================================
Scheduler - runs things concurrently
====================================

The Scheduler runs active microprocesses - giving a regular timeslice to each.
It also provides the ability to pause and wake them; allowing an Axon based
system to play nicely and relinquish the cpu when idle.

* The Scheduler runs microprocesses that have been 'activated'
* The Scheduler is itself a microprocess



Using the scheduler
-------------------

The simplest way is to just use the default scheduler ``scheduler.run``.
Simply activate components or microprocesses then call the runThreads() method
of the scheduler::

    from Axon.Scheduler import scheduler
    from MyComponents import MyComponent, AnotherComponent
    
    c1 = MyComponent().activate()
    c2 = MyComponent().activate()
    c3 = AnotherComponent().activate()

    scheduler.run.runThreads()


Alternatively you can create a specific scheduler instance, and activate
them using that specific scheduler::

    mySched = scheduler()

    c1 = MyComponent().activate(Scheduler=mySched)
    c2 = MyComponent().activate(Scheduler=mySched)
    c3 = AnotherComponent().activate(Scheduler=mySched)

    mySched.runThreads()


The runThreads() method is the way of bootstrapping the scheduler. Being a
microprocess, it needs something to schedule it! The runThreads() method does
exactly that.

The activate() method is fully thread-safe. It can handle multiple simultaneous
callers from different threads to the one the scheduler is running in.



Pausing and Waking microprocesses
---------------------------------

The Scheduler supports the ability to, in a thread safe manner, pause and wake
individual microprocesses under its control. Because it is thread safe, any
thread of execution can issue pause and wake requests for any scheduled
microprocess.

The pauseThread() and wakeThread() methods submit requests to pause or wake
microprocesses. The scheduler will process these when it is next able to - the
requests are queued rather than processed immediately. This is done to ensure
thread safety. It can handle multiple simultaneous callers from different
threads to the one the scheduler is running in.

Pausing a microprocess means the scheduler removes it from its 'run queue'. This
means that it no longer executes that microprocess. Waking it puts it back into
the 'run queue'.

If no microprocesses are awake then the scheduler relinquishes cpu usage by
blocking.

If however this scheduler is itself being scheduled by another microprocess then
it does not block. Ideally it should ask its scheduler to pause it, but instead
it busy-waits - self pausing functionality is not yet implemented.



'yielding' new components for activation and replacement generators
-------------------------------------------------------------------

In general, the main() generator in a microprocess (its thread of execution)
can return any values it likes when it uses the ``yield`` statement. It is
recommended to not yield zeros or other kinds of 'false' value as these are
reserved for possible future special meaning.

However, this scheduler does understand certain values that can be yielded:

* **Axon.Ipc.newComponent** - a microprocess can yield this to ask the scheduler
  to activate a new component or microprocess::

        def main(self):
            ...
            x=MyComponent()
            yield Axon.Ipc.newComponent(x)
            ...
      
  This is simply an alternative to calling x.activate().

* **Axon.Ipc.WaitComplete** - this is a way for a microprocess to substitute
  itself (temporarily) with another one that uses a new generator.
  For example::

        def main(self):
            ...
            yield Axon.Ipc.WaitComplete(self.waitOneSecond())
            ...

        def waitOneSecond(self):
            t=time.time()
            while time.time() < t+1.0:
                yield 1

  This is a convenient way to modularise parts of your main() code. But there
  is an important limitation with the current implementation:

  * self.pause() will not cause the replacement generator to pause. (Where
    'self' is the original microprocess - as in the example code above)



What happens when a microprocess finishes?
------------------------------------------

The scheduler will stop running it! It will call the microprocess's stop()
method. It will also call the _closeDownMicroprocess() method and will act on
the return value if it is one of the following:

* **Axon.Ipc.shutdownMicroprocess** - the specified microprocess will also be
  stopped. Use with caution as the implementation is currently untested and
  likely to fail, possibly even crash the scheduler!

* **Axon.Ipc.reactivate** - the specified microprocess will be (re)activated.
  The scheduler uses this internally to pick up where it left off when a
  Axon.Ipc.WaitComplete instigated detour finishes (see above).

  

Querying the scheduler (Introspection)
--------------------------------------

The listAllThreads() method returns a list of all activated microprocesses -
both paused and awake.

The isThreadPaused() method lets you determine if an individual microprocess is
paused. Note that the result returned by this method is conservative (the
default assumption is that a thread is probably awake). the result will vary
depending on the exact moment it is called!

Both these methods are thread safe.



Slowing down execution (for debugging)
--------------------------------------

It also has a slow motion mode designed to help with debugging & testing. Call
runThreads() with the slowmo argument set to the number of seconds the scheduler
should pause after each cycle of executing all microprocesses. For example, to
wait half a second after each cycle of execution::

    scheduler.run.runThreads(slowmo=0.5)



How does it work internally?
----------------------------

The scheduler keeps the following internal state:

* **time** - updated to time.time() every execution cycle - can be inspected by
  microprocesses instead of having to call time.time() themselves.
    
* **threads** - a dictionary containing the state of activated microprocesses
  (whether they are awake or not)

* **wakeRequests** and **pauseRequests** - the thread safe queues of requests to
  wake and pause individual microprocesses

* Internal to the main() generator:
    
  * **runqueue** - the list of active and awake microprocesses being run

  * **nextrunqueue** - the list of microprocesses to be run next time round

The scheduler uses a simple round robin approach - it walks through its run
queue and calls the next() method of each microprocess in turn. As it goes, it
builds a new run queue, ready for the next cycle. If a microprocess terminates
(raises a StopIteration exception) then it is not included in the next cycle's
run queue.

After it has gone through all microprocesses, the scheduler then processes
messages in its wakeRequests and sleepRequests queues. Sleep requests are
processed first; then wake requests second. Suppose there is a sleep and wake
request queued for the same microprocess; should it be left awake or put to
sleep? By processing wake requests last, the scheduler can err on the side of
caution and prefer to leave it awake.

Microprocesses are all in one of three possible states (recorded in the
``threads`` dictionary):
    
* **ACTIVE** - the microprocess is awake. It should be in the run queue being
  prepared for the next execution cycle.

* **SLEEPING** - the microprocess is asleep/paused. It should *not* be in the
  run queue for the next cycle.

* **GOINGTOSLEEP** - the microprocess has been requested to be put to sleep.

A request to put a microprocess to sleep is handled as follows:
    
* If the microprocess is already *sleeping*, then nothing needs to happen.

* If the microprocess is *active*, then it is changed to "going to sleep". It
  is not removed from the run queue immediately. Instead, what happens is:

   * on the next cycle of execution, as the scheduler goes through items in the
     run queue, it doesn't execute any that are "going to sleep" and doesn't
     include them in the next run queue it is building. It also sets them to the
     "sleeping" state,

Wake requests are used to both wake up sleeping microprocesses and also to
activate new ones. A request to wake a microprocess is handled like this:

* If the microprocess is already *active*, then nothing needs to happen.

* If the microprocess is *sleeping* then it is added to the next run queue and
  changed to be *active*.

* If the microprocess is *going to sleep* then it is only changed to be *active*
  (it will already be in the run queue, so doesn't need to be added)

If the request contains a flag indicating that this is actually an activation
request, then this also happens:
  
* If the microprocess is not in the ``threads`` dictionary then it is added to
  both the run queue and ``threads``. It is set to be *active*.

This three state system is a performance optimisation: it means that the
scheduler does not need to waste time searching through the next run queue to
remove items - they simply get removed on the next cycle of execution.

Wake requests and sleep requests are handled through thread-safe queues. This
enables other threads of execution (eg. threaded components) to safely make
requests to wake or pause components.



"""
import time
import gc as _gc
import os

from util import removeAll
from idGen import strId, numId
from debug import debug
from Microprocess import microprocess
from Axon import AxonObject as _AxonObject
from Ipc import *
import Queue

def _sort(somelist):
   a=[ x for x in somelist]
   a.sort()
   return a

_ACTIVE       = object()     # microprocess is active (is in the runqueue)
_SLEEPING     = object()     # microprocess is paused (is not in the runqueue)
_GOINGTOSLEEP = object()     # microprocess to be paused (should be removed from the runqueue)

class scheduler(microprocess):
   """Scheduler - runs microthreads of control."""
   run = None
   wait_for_one = False
   def __init__(self, **argd):
      """Creates a scheduler object. If scheduler.run has not been set, sets it.
      Class initialisation ensures that this object/class attribute is initialised - client
      modules always have access to a standalone scheduler.
      Internal attributes:
       
         * time = time when this object was last active.
         * threads = set of threads to be run, including their state - whether active or sleeping(paused)
        
      Whilst there can be more than one scheduler active in the general case you will NOT
      want to create a custom scheduler.
      """
      super(scheduler, self).__init__(**argd)
      if not scheduler.run:         # If no scheduler already allocated...
         scheduler.run = self       # Make this scheduler the singleton scheduler.

      self.time = time.time()
      
      self.threads = {}    # current set of threads and their states (whether sleeping, or running)
      self.stopRequests = Queue.Queue()
      self.wakeRequests = Queue.Queue()
      self.pauseRequests = Queue.Queue()
      self.exception_caught = StopIteration
      self.debuggingon = False
      if self.wait_for_one:
         self.extra = 1
      else:
         self.extra = 0

   def waitForOne(self):
      self.extra = 1

   def _addThread(self, mprocess):
      """A Microprocess adds itself to the runqueue using this method, using
      the mannerism scheduler.run._addThread(). Generally component writers should
      *not* use this method to activate a component - use the component's own
      activate() method instead.
      """
      self.wakeThread(mprocess, True)
      
   def wakeThread(self, mprocess, canActivate=False):
      """\
      Request to wake a sleeping mprocess, or activate a new one.
      
      If sleeping or already active, the specified microprocess will be ensured
      to be active on the next cycle through the scheduler.
      
      If the microprocess is not running yet then it will be woken if (and only if)
      canActivate is set to True (the default is False).
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
       self.debuggingon = True
       return self.threads.keys()
   
   def handleMicroprocessShutdownKnockon(self, knockon):
     if isinstance(knockon, shutdownMicroprocess):
        # XXX probably doesnt work!
        # as the scheduler goes through the run queue it will expect to find a
        # corresponding entry in self.threads - but its being deleted here!
        # also what about calling stop() and _closeDownMicroprocess() for this
        # one too??? (Matt, 22 March 2007)
        for i in xrange(len(self.threads)):
           if self.threads[i] in knockon.microprocesses():
              self.threads[i] = None
              
     if isinstance(knockon, reactivate):
         self._addThread(knockon.original)

   def immortalise(cls):
       """\
       immortalise() - Class method to make the default scheduler immune to components that crash unexpectedly
       
       immortalise() is a feature you'll want to call when running a
       production system. In short it actively catches rogue components that
       will take out your server during normal development. (Taking out the
       server in normal development is a useful feature since it assists
       with debugging, but a pain for unusual/exceptional scenarios in a
       production system)
       
       It must be called *before* the scheduler starts running. Calling it
       afterwards will have no effect.
       
       Usage: Axon.Scheduler.scheduler.immortalise()       
       """
       cls.run.exception_caught = Exception
   immortalise = classmethod(immortalise)

   def mortalise(cls):
       """\
       mortalise() - Class method to make the default scheduler use the default behaviour - to die if components crash unexpectedly
       
       mortalise undoes a call to immortalise. 
       
       NOTE: It must be called *before* the scheduler starts running.
       Calling it afterwards will have no effect.
       
       Usage: Axon.Scheduler.scheduler.mortalise()
       """
       cls.run.exception_caught = StopIteration
   mortalise = classmethod(mortalise)

   def main(self,slowmo=0,canblock=False):
       """\
       main([slowmo][,canblock]) - Scheduler main loop generator
       
       Each cycle through this generator does two things:
       * one pass through all active microprocesses, giving executing them.
       * processing of wake/sleep requests

       You can optionally slow down execution to aid debugging. You can also
       allow the scheduler to block if there are no active, awake microprocesses.

       Keyword arguments:

       - slowmo    -- slow down execution by waiting this number of seconds each cycle (default=0)
       - canblock  -- if True, then will block (waiting for wake requests) if all microprocesses are sleeping (default=False)
       
       slowmo specifies a delay (in seconds) before the main loop is run.
       slowmo defaults to 0.
       
       If canblock is True, this generator will briefly) block if there are
       no active microprocesses, otherwise it will return immediately (default).
       
       This generator terminates when there are no microprocesses left (either
       sleeping or awake) because they've all terminated. (or because there were
       none to begin with!)
       """
       nextrunqueue = []
       running = True
       exception_caught = self.exception_caught
       
       while running:
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
#           if self.debuggingon:
#               print "-->", [ x.name for x in self.threads], [ x.name for x in runqueue]
           for mprocess in runqueue:
#               if self.debuggingon:
#                   print "Before Run", mprocess

               yield 1
               
               if self.threads[mprocess] == _ACTIVE:
                   try:
                       result = mprocess.next()
                       
                       if isinstance(result, newComponent):
                           for c in result.components():
                               c.activate()
                       if isinstance(result, WaitComplete):
                           tag = result.argd.get("tag","")
                           if tag == "":
                              tag = "__" + mprocess.name[-10:] # So we have a clue of parentage(!)
                           newThread = microprocess(result.args[0], reactivate(mprocess), tag = tag )
                           newThread.activate()
                           del self.threads[mprocess]
                           mprocess = None
                           
#                       if self.debuggingon:
#                           print "After Run", mprocess
                       if mprocess:
                           nextrunqueue.append(mprocess)
                   except exception_caught:
                       del self.threads[mprocess]
                       mprocess.stop()
                       knockon = mprocess._closeDownMicroprocess()
                       self.handleMicroprocessShutdownKnockon(knockon)
               else:
                   # state is _GOINGTOSLEEP or _SLEEPING
                   # so should *not* execute this one and leave it out of the
                   # next run queue
                   self.threads[mprocess] = _SLEEPING

           # make sure, even if there weren't any micprocesses active, we yield
           # control at least once
           yield 1
           
           # process pause requests first - to prevent deadlock, we do
           # wakeup requests second - safer to leave a thread awake than asleep
           while not self.pauseRequests.empty():
               mprocess = self.pauseRequests.get()
               # only sleep if we're actually in the set of threads(!)
               # otherwise it inadvertently gets added!
               if self.threads.has_key(mprocess):
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
                    self.extra = 0   # Fix for race hazard regarding wait_for_one, esp problem with threaded components
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
                            allsleeping = False

               except Queue.Empty:
                    # catch timeout
                    pass
               if not self.stopRequests.empty():
#                   print "Do we get here? 1"
                   break

           if not self.stopRequests.empty():
#               print "Do we get here? 2"
               break
#           print "len(self.threads), wakeRequests" , len(self.threads), self.wakeRequests
           running = len(self.threads) + self.extra

       if not self.stopRequests.empty():
#           print "WE GOT HERE! :-)"
           for X in self.threads:
#               print "We now call .stop() on ", X.name, type(X)
               X.stop()
#       print "All microprocesses now stopped. Halting"

   def stop(self):
#       print "ADDING STOP REQUEST"
       self.stopRequests.put( self )
       super(scheduler, self).stop()

   def runThreads(self,slowmo=0):
      """\
      Runs the scheduler until there are no activated microprocesses left
      (they've all terminated).
      
      Think of this as bootstrapping the scheduler - after all it is a
      microprocess like any other, so needs something to run it!

      Keyword arguments:

      - slowmo  -- Optional. Number of seconds to wait between each cycle of executing microprocesses. (default=0 - no wait)
      """
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

