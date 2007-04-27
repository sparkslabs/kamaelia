#!/usr/bin/env python
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
import Axon.Scheduler as Scheduler
from test___str__ import str_Test
from Axon.Microprocess import microprocess as microprocess

class MicroProcess_Test(str_Test):
   """A full set of tests for the Microprocess class."""
   classtotest = microprocess

   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments.  Creates multiple microprocess objects with no arguments and checks they do not have matching ids. "
      self.init_test(microprocess)

   class DummySched:
      run = None
      def __init__(self):
         self.threadcount = 0
         self.threadlist = []
         if (self.__class__.run is None):
            self.__class__.run = self
      def _addThread(self, thread):
         self.threadcount = self.threadcount + 1
         self.threadlist.append(thread)

##name
#   def test_InitWithArgs(self,name = "fred"):
#      "__init__ - With test argument to check that the name gets set"
#      m = self.init_test(microprocess, (name,))
#      self.failIf(name != m.name, "Name not set at __init__")


#init flag
#id
   def init_test(self,mpsubclass=microprocess, args=()):
      "This is an internal method that can be used to create a microprocess object with the arguments that you want.  It also runs the duplicate ID check by creating a couple of objects.  Although there is only one optional argument to init a tuple is used here in case of future extension."
      m=apply(mpsubclass,args)
      self.failUnless(m.init," Microprocess initialization failed with no arguments")
      # This is weak test for duplicate IDs but might catch some silly errors
      n=apply(mpsubclass,(args))
      o=apply(mpsubclass,(args))
      self.failUnless(m.id and n.id and o.id,"All microprocesses should have id values.")
      self.failIf(m.id == n.id or n.id == o.id , "Non-unique IDs")
      return m


#activate test
   def test_activate_basicActivatation(self):
      "Tests the activation method operates as expected with a chosen scheduler"
      testscheduler = self.DummySched()
      mp = self.init_test()
      temp = testscheduler.threadcount
      mp.activate(testscheduler)
      self.failIf(testscheduler.threadcount != temp + 1, "activate doesn't call _addthread on the requested scheduler")
      self.failIf(testscheduler.threadlist.count(mp) != 1, "Microprocess not added to scheduler properly.")

#setSchedulerClass Test
   def test_activate_afterCallingSetSchedulerClass(self):
      "Tests the setting of the scheduler class to be used for a subclass of microprocess is actually reflected at activation"
      # This creates a DummySched.run instance.
      testscheduler = self.DummySched()

      temp = testscheduler.threadcount
      basicmp = self.init_test()
      class SpecialSchedulerMicroprocess(microprocess):
         pass
      SpecialSchedulerMicroprocess.setSchedulerClass(self.DummySched)
      specialmp = self.init_test(SpecialSchedulerMicroprocess)
      basicmp.activate()
      specialmp.activate()
      self.failIf(testscheduler.threadcount != temp + 1, "activate doesn't call _addthread on the requested scheduler")
      self.failIf(testscheduler.threadlist.count(specialmp) != 1, "Microprocess not added to scheduler properly.")

   def test_setSchedulerClass(self):
      "Tests setting scheduler class and that the default scheduler is Scheduler.scheduler"
      class DummySched:
         pass
      premp = self.init_test()
      before = premp.__class__.schedulerClass
      microprocess.setSchedulerClass(DummySched)
      postmp = self.init_test()
      after = postmp.__class__.schedulerClass
      self.failUnless(before == Scheduler.scheduler, "Default scheduler not as expected!")
      self.failUnless(after == DummySched, "Set scheduler failed to set the scheduler properly")
      self.failUnless(before != after, "Setting scheduler did not change class!")
      microprocess.setSchedulerClass(before)
      resetmp=self.init_test()
      self.failUnless(resetmp.__class__.schedulerClass == Scheduler.scheduler)

   def test_overriddenMainWorksWithNext(self):
      "Tests that an overridden main is run correctly by repeatedly calling next() and that termination occurs at the proper time with the proper StopIteration exception."
      class testthread(microprocess):
         def __init__(self):
            self.i = 0
            self.__super.__init__()
         def main(self):
            while self.i < 100:
               self.i = self.i + 1
               yield 1
      class dummyScheduler:
         def _addThread(self,thread):
            pass
      thr = self.init_test(testthread)
      sched = dummyScheduler()
      thr.activate(sched)
      for i in xrange(1,101):
         self.failUnless(thr.next(), "Unexpected false return value")
         self.failUnless(thr.i == i, "Iteration of main not performed!")
      #self.failIf(thr.next(), "Should return false as has returned at this point.")
      self.failUnlessRaises(StopIteration, thr.next)
      self.failUnless(thr.i == 100, "Unexpected final result of iteration")

   def test_Stop(self):
      "Tests that after being stopped a microprocess returns true to _isStopped and false to _isRunnable."
      thr = self.init_test()
      self.failIf(thr._isStopped(), "Thread reports itself stopped before stop is called!")
      self.failUnless(thr._isRunnable(), "Thread doesn't report itself runnable before stop is called.")
      thr.stop()
      self.failUnless(thr._isStopped, "Thread doesn't report itself stopped after stop is called.")
      self.failIf(thr._isRunnable(),"Thread reports as runnable.  Should be stopped at this point.")
      thr._unpause()
      self.failUnless(thr._isStopped, "Thread doesn't report itself stopped after unpause attempt.")
      self.failIf(thr._isRunnable(),"Thread reports as runnable.  Unpause should not have worked at this point.")

   def test_pause(self):
      "Tests that after being pause a microprocess returns false to _isRunnable.  Also tests _isRunnable and _unpause."
      thr = self.init_test()
      self.failUnless(thr._isRunnable(), "Thread doesn't report itself runnable before pause is called.")
      thr.pause()
      self.failIf(thr._isRunnable(),"Thread reports as runnable.  Should be paused at this point.")
      thr._unpause()
      self.failUnless(thr._isRunnable(), "Thread doesn't report itself runnable after _unpause is called.")

   def test_Next(self):
      "Additional checks over the main overridden main checks to test pausing and stopping behaviour."
      class testthread(microprocess):
         def __init__(self):
            self.i = 0
            self.__super.__init__()
         def main(self):
            while 1:
               self.i = self.i + 1
               yield 1
      class dummyScheduler:
         def _addThread(self,thread):
            pass
      thr = self.init_test(testthread)
      sched = dummyScheduler()
      thr.activate(sched)
      for x in xrange(1,5):
         self.failUnless(thr.next())
         self.failUnless(thr.i == x)
      thr.pause()
      for x in xrange(5,10):
         self.failUnless(thr.next())
         self.failUnless(thr.i == 4)
      thr._unpause()
      for x in xrange(5,10):
         self.failUnless(thr.next())
         self.failUnless(thr.i == x)
      thr.stop()
      self.failIf(thr.next())
      self.failUnlessRaises(StopIteration, thr.next)

   def test__closeDownMicroprocess(self):
      "Stub _closeDownMicroprocess should always return 0"
      mp = self.init_test()
      self.failUnless(0 == mp._closeDownMicroprocess())


if __name__=='__main__':
   unittest.main()
