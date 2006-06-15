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
        
   def test_runThreadsSlowmo(self):
       """Specifying slowMo>0 argument to runThreads() causes a delay of the specified number of seconds between each pass through all microprocesses. During the delay it will yield."""
       self.fail("Test not yet implemented")
        
   def test_directUsageOfMainDoesntBlock(self):
       """By default, if all microprocesses are paused, the scheduler will immediately yield back - it will not block."""
       self.fail("Test not yet implemented")
    
   def test_runThreadsUsesNonBusyWaitingMode(self):
       """If canBlock argument of main() is True, then the scheduler may/will block if all microprocesses are paused."""
       self.fail("Test not yet implemented")


if __name__=='__main__':
   unittest.main()
