#!/usr/bin/env python2.3
#
# Aim: Full coverage testing of the
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")

# import preconditions record values
from Scheduler import *

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
      
   def test_sensiblestructure(self):
      "Conceptual issue to discuss"
      self.fail("Rip out the slowmo stuff from the the scheduler.  Instead make a component that blocks the right amount of time to slow down the system.  This would leave a far simpler system and make dynamic control easier.")
      

if __name__=='__main__':
   unittest.main()
