#!/usr/bin/env python2.3
#
# Aim: Full coverage testing of the
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")
from classfile import *

class classWeAreTesting_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments ... "
      pass

if __name__=='__main__':
   unittest.main()
