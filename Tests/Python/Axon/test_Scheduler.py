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
from Axon.Scheduler import *


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


class scheduler_Test(unittest.TestCase):
    
   def setUp(self):
      pass
   def test_importsuccess(self):
      self.failUnless(microprocess.schedulerClass is scheduler)
      self.failUnless(scheduler.run)
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments ... "
      scheduler.run = None
      s=scheduler()
      self.failUnless(scheduler.run is s)
      
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
       s=scheduler()
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
       
       s=scheduler()
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
       
       s=scheduler()
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
       
       class TestMProc(microprocess):
           def next(self):
                self.mainCalled=True
           def stop(self):
               raise "ARGH"
           def _closeDownMicroprocess(self):
               raise "ARGH 2"
       
       s=scheduler()
       sched = s.main()
       mprocess = TestMProc()
       s._addThread(mprocess)
       try:
           for _ in range(0,3):   # give it a few cycles grace
               sched.next()
           for _ in range(0,10):
               mprocess.mainCalled=False
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
           

if __name__=='__main__':
   unittest.main()
