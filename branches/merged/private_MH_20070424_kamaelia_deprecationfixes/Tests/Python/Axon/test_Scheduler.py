#!/usr/bin/python
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
#
# Aim: Full coverage testing of the
#

# Test the module loads
import unittest

# import preconditions record values
import Axon.Scheduler


class SimpleTestMProc(object):
    """\
    Simple microprocess for testing the scheduler. 
    Runs for the specified count duration, then terminates.
    """
    def __init__(self,count=10):
        super(SimpleTestMProc,self).__init__()
        self.count = count
        self.stopped = False
        self.closedDown = False
    def next(self):
        if self.count > 0:
            self.count = self.count - 1
        else:
            raise StopIteration
    def stop(self):
        if self.count != 0:
            raise "ARGH"
        self.stopped=True
    def _closeDownMicroprocess(self):
        self.closedDown = True

class TestRunningMProc(object):
    def next(self):
        self.mainCalled=True
    def stop(self):
        raise "ARGH"
    def _closeDownMicroprocess(self):
        raise "ARGH 2"

class TestPausedMProc(object):
    def __init__(self, scheduler):
        self.s = scheduler
        self.__thread = self.main()
        self.next = self.__thread.next
    def main(self):
        self.s.pauseThread(self)
        yield 1
    def stop(self):
        pass
    def _closeDownMicroprocess(self):
        pass


class scheduler_Test(unittest.TestCase):
    
   def setUp(self):
      pass
   def test_importsuccess(self):
      self.failUnless(Axon.Scheduler.microprocess.schedulerClass is Axon.Scheduler.scheduler)
      self.failUnless(Axon.Scheduler.scheduler.run)
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments ... "
      Axon.Scheduler.scheduler.run = None
      s=Axon.Scheduler.scheduler()
      self.failUnless(Axon.Scheduler.scheduler.run is s)
      
#   def test_sensiblestructure(self):
#      "Conceptual issue to discuss"
#      self.fail("""Rip out the slowmo stuff from the the scheduler.
#                Option 1: instead make a component that blocks the right amount
#                of time to slow down the system.  This would leave a
#                far simpler system and make dynamic control easier.
#                Option 2: Allow the implementation of simpler ways for running the scheduler
#                Option 3: move slowmo into runThreads instead.
#                etc.""")
      
   def test_stopsIfNoThreads(self):
       """When run, the scheduler microprocess terminates immediately if there are no microprocesses to schedule."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       try:
           # give it a few cycles grace
           for _ in range(0,5):
               sched.next()
               
           self.fail("Should not have succeeded")
       except StopIteration:
           pass
       except:
           raise
       
   def test_runsMicroprocessToCompletionThenStops(self):
       """When run with a single microprocess, the scheduler microprocess only terminates once the scheduled microprocess has terminated."""
       
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       t=SimpleTestMProc()
       s._addThread(t)
       try:
           for _ in range(0,1000):
               sched.next()
           self.fail("Should have stopped by now")
       except StopIteration:
           self.assert_(t.count==0, "Scheduled microprocess should have been run until completion")
           self.assert_(t.stopped, "Microprocess's stop() method should have been called when it finished")
       except:
           raise
               
   def test_runsMicroprocessesAllToCompletionThenStops(self):
       """When run with multiple microprocesses, the scheduler microprocess only terminates once all scheduled microprocesses have terminated."""
       
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       mprocesses = []
       for i in range(1,5):
           t=SimpleTestMProc(i*10)
           s._addThread(t)
           mprocesses.append(t)
       try:
           for _ in range(0,1000):
               sched.next()
           self.fail("Should have stopped by now")
       except StopIteration:
           for mp in mprocesses:
               self.assert_(mp.count==0, "Scheduled microprocess should have been run until completion")
               self.assert_(mp.stopped, "Microprocess's stop() method should have been called when it finished")
       except:
           raise
               
   def test_pausedMicroprocessDoesNotGetCalled(self):
       """A microprocess is run until paused, by calling scheduler.pauseThread(). The microprocess is then no longer 'run'."""
       
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       mprocess = TestRunningMProc()
       s._addThread(mprocess)
       try:
           for _ in range(0,3):   # give it a few cycles grace
               sched.next()
           for _ in range(0,10):
               mprocess.mainCalled=False
               for i in range(0,3):
                   sched.next()
               self.assert_(mprocess.mainCalled, "Microprocess next() should be being called at this stage.")
           s.pauseThread(mprocess)
           for _ in range(0,3):   # give it a few cycles grace
               sched.next()
           for _ in range(0,10):
               mprocess.mainCalled=False
               sched.next()
               self.assert_(mprocess.mainCalled==False, "Microprocess next() should not be being called at this stage.")
       except:
           raise
           
   def test_oneMicroprocessPausesOthersContinueToRun(self):
       """If one microprocess is paused, the scheduler continues to run other microprocesses."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       paused = TestRunningMProc()
       s._addThread(paused)
       others = []
       for _ in range(0,5):
           mp=TestRunningMProc()
           s._addThread(mp)
           others.append(mp)
       all = others + [paused]
       
       try:
           for _ in range(0,3*len(all)):   # give it a few cycles grace
               sched.next()
           for _ in range(0,10):
               for mp in all:
                   mp.mainCalled=False
               for i in range(len(all)*2):
                   sched.next()
               for mp in all:
                   self.assert_(mp.mainCalled, "Microprocess next() should be being called at this stage.")
           s.pauseThread(paused)
           for _ in range(0,3*len(all)):   # give it a few cycles grace
               sched.next()
           for _ in range(0,10):
               for mp in all:
                   mp.mainCalled=False
               for i in range(len(all)*2):
                   sched.next()
               for mp in others:
                   self.assert_(mp.mainCalled, "Microprocess next() should be being called at this stage.")
               self.assert_(paused.mainCalled==False, "Microprocess next() should not be being called at this stage.")
       except:
           raise
               
   def test_pausedMicroprocessCanBeWoken(self):
       """If a microprocess is paused, calling sheduler.wakeThread() will unpause it."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       paused = TestRunningMProc()
       s._addThread(paused)
       others = []
       for _ in range(0,5):
           mp=TestRunningMProc()
           s._addThread(mp)
           others.append(mp)
       all = others + [paused]
       try:
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
           
           s.pauseThread(paused)

           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
               
           for _ in range(0,10):
               for mp in all:
                   mp.mainCalled=False
               for i in range(len(all)*2):
                   sched.next()
               for mp in others:
                   self.assert_(mp.mainCalled, "Microprocess next() should be being called at this stage.")
               self.assert_(paused.mainCalled==False, "Microprocess next() should not be being called at this stage.")
               
           s.wakeThread(paused)
           for _ in range(0,5*len(all)): # give it a few cycles grace
               sched.next()
               
           for _ in range(0,10):
               for mp in all:
                   mp.mainCalled=False
               for i in range(len(all)*2):
                   sched.next()
               for mp in all:
                   self.assert_(mp.mainCalled, "Microprocess next() should be being called at this stage.")
       except:
           raise
       
   def test_wakingPausedMicroprocessDoesntWakeOthers(self):
       """Waking a paused microprocess will not wake other paused microprocesses."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       notpaused = TestRunningMProc()
       s._addThread(notpaused)
       others = []
       for _ in range(0,5):
           mp=TestRunningMProc()
           s._addThread(mp)
           others.append(mp)
       all = others + [notpaused]
       try:
           
           for _ in range(0,5*len(all)): # give it a few cycles grace
               sched.next()
           
           for mp in all:
               s.pauseThread(mp)

           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
               
           for _ in range(0,10):
               for mp in all:
                   mp.mainCalled=False
               for i in range(len(all)*2):
                   sched.next()
               for mp in all:
                   self.assert_(mp.mainCalled==False, "Microprocess next() should not be being called at this stage.")
               
           s.wakeThread(notpaused)
           for _ in range(0,5*len(all)): # give it a few cycles grace
               sched.next()
               
           for _ in range(0,10):
               for mp in all:
                   mp.mainCalled=False
               for i in range(len(all)*2):
                   sched.next()
               for mp in others:
                   self.assert_(mp.mainCalled == False, "Microprocess next() should notbe being called at this stage.")
               self.assert_(notpaused.mainCalled, "Microprocess next() should be being called at this stage.")

       except:
           raise

   def test_wakingAlreadyAwakeMicroprocessHasNoEffect(self):
       """Waking or pausing a microprocess that is already awake or paused (respectively) has no effect."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       themp = TestRunningMProc()
       others = [ TestRunningMProc() for _ in range(0,5) ]
       all = others + [themp]
       
       for m in all: s._addThread(m)
       
       try:
           for m in all:
               m.mainCalled=False
           
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
       
           for m in all:
               self.assert_(m.mainCalled, "Threads should all be running")
               m.mainCalled=False
           
           self.assert_( all.sort() == s.listAllThreads().sort(), "Threads we think should be running are.")
           
           s.wakeThread(themp)
           
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
           
           self.assert_( all.sort() == s.listAllThreads().sort(), "Threads we think should be running are.")
           
           for m in all:
               self.assert_(m.mainCalled, "Threads should all be running")
               m.mainCalled=False

           s.pauseThread(themp)

           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
       
           for m in others:
               self.assert_(m.mainCalled, "Threads should all be running except one")
               m.mainCalled=False
           self.assert_(not themp.mainCalled, "Threads should all be running except one")

       except:
           raise

   def test_wakingOrPausingNonActivatedMicroprocessHasoEffect(self):
       """Waking or pausing a microprocess that has not yet been activated has no effect."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       themp = TestRunningMProc()
       others = [ TestRunningMProc() for _ in range(0,5) ]
       all = others + [themp]
       
       for m in others: s._addThread(m)
       
       try:
           for m in all:
               m.mainCalled=False
           
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
       
           for m in others:
               self.assert_(m.mainCalled, "Threads should all be running")
               m.mainCalled=False
           self.assert_(not themp.mainCalled, "Threads should all be running except one")
           
           self.assert_( others.sort() == s.listAllThreads().sort(), "Threads we think should be running are.")
           
           s.wakeThread(themp)
           
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
           
           self.assert_( others.sort() == s.listAllThreads().sort(), "Threads we think should be running are.")
           
           for m in others:
               self.assert_(m.mainCalled, "Threads should all be running")
               m.mainCalled=False
           self.assert_(not themp.mainCalled, "Threads should all be running except one")

           s.pauseThread(themp)

           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
       
           for m in others:
               self.assert_(m.mainCalled, "Threads should all be running except one")
               m.mainCalled=False
           self.assert_(not themp.mainCalled, "Threads should all be running except one")

       except:
           raise
        
   def test_listAllThreadsMethodListsAllMicroprocesses(self):
       """The listAllThreads() method returns a list of all activated microprocesses whether paused or awake."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       all = [ TestRunningMProc() for _ in range(0,5) ]
       
       for m in all: s._addThread(m)
       
       try:
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
       
           self.assert_( all.sort() == s.listAllThreads().sort(), "Threads we think should be running are.")
           
           s.pauseThread(all[1])
           s.pauseThread(all[4])
           
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
       
           self.assert_( all.sort() == s.listAllThreads().sort(), "Threads we think should be running are.")

       except:
           raise
           
   def test_isThreadPausedWorks(self):
       """The isThreadPaused() method returns True if a thread is currently paused, or False is it is active."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       all = [ TestRunningMProc() for _ in range(0,5) ]
       
       for m in all: s._addThread(m)
       
       try:
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
               
           for m in all:
               self.assert_(not s.isThreadPaused(m))
               
           for mp in all:
               s.pauseThread(mp)
               
               for _ in range(0,3*len(all)): # give it a few cycles grace
                   sched.next()
                   
               for m in all:
                   if m==mp:
                       self.assert_(s.isThreadPaused(m))
                   else:
                       self.assert_(not s.isThreadPaused(m))
                       
               s.wakeThread(mp)

       except:
           raise
       
   def test_isThreadPausedNotRecognised(self):
       """The isThreadPaused() method will return True for micropocesses not scheduled with this scheduler."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()
       all = [ TestRunningMProc() for _ in range(0,5) ]
       other = TestRunningMProc()
       
       for m in all: s._addThread(m)
       
       try:
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
               
           for m in all:
               self.assert_(not s.isThreadPaused(m))
               
           self.assert_(s.isThreadPaused(other))
               
           for mp in all:
               s.pauseThread(mp)
               
           for _ in range(0,3*len(all)): # give it a few cycles grace
               sched.next()
                   
           for m in all:
               self.assert_(s.isThreadPaused(m))
               
           self.assert_(s.isThreadPaused(other))

       except:
           raise
        
   def test_pauseThenTerminateTerminates(self):
       """If a microprocess pauses and immediately terminates (without further yields) it will still terminate properly."""
       s=Axon.Scheduler.scheduler()
       sched = s.main()

       class ImmediateTerminator(object):
           def next(self):
               s.pauseThread(self)
               raise StopIteration
           def stop(self):
               pass # this should happen!
           def _closeDownMicroprocess(self):
               pass # this should happen!
               
       m = ImmediateTerminator()
       s._addThread(m)
       try:
           for _ in range(0,100):
               sched.next()
               
           self.fail("Scheduler should have terminated by now.")
       except StopIteration:
           pass
       except:
           raise

   def test_runThreadsSlowmo(self):
       """Specifying slowMo>0 argument to runThreads() causes a delay of the specified number of seconds between each pass through all microprocesses. During the delay it will yield."""
       
       class MOCK_TIME_MODULE(object):
           def __init__(self):
               self.count = 0
               self.thetime = 0
           def time(self):
               # time jumps to just after 1 second, after 1000 iterations
               self.count += 1
               if self.count > 1000:
                   self.thetime = 1.01
               if self.count > 2000:
                   raise "Test should have finished by now!"
               return self.thetime
           def sleep(self,seconds):
               self.thetime = self.thetime + seconds
           
       # plug in mock
       timemod = MOCK_TIME_MODULE()
       Axon.Scheduler.time = timemod
       
       class Success(Exception): pass
       
       class MProc(object):
           def __init__(self,testcase):
               super(MProc,self).__init__()
               self.testcase = testcase
           def next(self):
               self.testcase.assert_(timemod.thetime >= 1.00, "Should not have been executed before a 1 second delay has passed")
               raise Success
           def stop(self):
               raise "ARGH"
           def _closeDownMicroprocess(self):
               raise "ARGH 2"
       
       try:
           s=Axon.Scheduler.scheduler()
           
           mp = MProc(self)
           s._addThread(mp)
           
           try:
               s.runThreads(slowmo=1.0)
               self.fail("Should not have reached here")
           except Success:
               pass   # test succeeded
           except:
               raise
       finally:
           # unplug mock
           import time as t
           Axon.Scheduler.time = t
        
   def test_directUsageOfMainDoesntBlock(self):
       """By default, if all microprocesses are paused, the scheduler will immediately yield back - it will not block."""
       
       # XXX This test probably needs to be better implemented/defined ... it simply checks that it doesn't
       #     block for too long using a timeout
       import threading
       
       class SchedLaunch(threading.Thread):
           def __init__(self):
               super(SchedLaunch,self).__init__()
               self.exception = None
               self.s = Axon.Scheduler.scheduler()
               self.smain = self.s.main()
               self.mps = [TestRunningMProc() for _ in range(0,5)]
               for mp in self.mps:
                   self.s._addThread(mp)
               for _ in range(0,100):
                   self.smain.next()
               for mp in self.mps:
                   self.s.pauseThread(mp)
           def run(self):
               try:
                   for _ in range(0,100):
                       self.smain.next()
               except:
                    exception = sys.exc_info()
                    def throwexception(exception):
                        raise exception[0], exception[1], exception[2]
                    self.exception = sys.exc_info()
                    
       thread = SchedLaunch()
       thread.start()
       thread.join(5.0)
       self.assert_(not thread.isAlive(), "Scheduler should not have taken this long")
       if thread.exception:
           raise thread.exception[0],thread.exception[1],thread.exception[2]
    
   def test_runThreadsUsesNonBusyWaitingMode(self):
       """If run using the runThreads method, then the scheduler may/will block for short periods, relinquishing processor time, if all microprocesses are paused."""
       
       # we'll measure CPU time used over 3 seconds and expect it to be <1% of 3 seconds
       seconds = 3.0
       
       s = Axon.Scheduler.scheduler()
       mps = [TestPausedMProc(s) for _ in range(0,5)]
       for mp in mps:
           s._addThread(mp)
       
       import os,time
       import threading
       
       def causeCompletion():
           for mp in mps:
               s.wakeThread(mp)
       
       timer = threading.Timer(seconds,causeCompletion)
       
       timer.start()
       starttime = os.times()[1]
       s.runThreads()
       endtime = os.times()[2]
       
       self.assert_(endtime-starttime <= 0.01*seconds, "Time consumed should have been <1% of CPU time")



if __name__=='__main__':
   unittest.main()
