#!/usr/bin/env python2.3
#
# Tests __str__ for different classes
#

import unittest

class str_Test(unittest.TestCase):
   classtotest=None

   def test___str__(self):
      if not self.__class__ is str_Test:
         a = self.__class__.classtotest()
         b = self.__class__.classtotest()
         self.failIf(str(a)==str(b), "str does not produce a result unique to" + self.__class__.classtotest.__name__ +" instance.")
         self.failUnless(str(a)==str(a),"str does not produce a consistent result")

