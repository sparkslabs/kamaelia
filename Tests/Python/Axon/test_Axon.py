#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#
# Aim: Full coverage testing of the Axon root module
#

# Test the module loads
import unittest
from Axon import AxonObject, AxonType

try:
   import Queue
   version = 2
except ImportError:
   version = 3

if version == 3:
   class Axon_Test(unittest.TestCase):
       pass
else:
      class Axon_Test(unittest.TestCase):
         def multipleInheritanceTest(self, base):
            class foo(base):
               def __init__(self):
                 self.gah =1

            class bar(foo):
               def __init__(self):
                  self.__super.__init__()
                  self.gee = 1
                  self.gah += 1

            class bla(foo):
               def __init__(self):
                  self.__super.__init__()
                  self.goo = 2
                  self.gah += 1

            class barbla(bar,bla): # Classic hardcase - diagram inheritance.
               def __init__(self):
                  self.__super.__init__()
                  self.gee += 1
                  self.goo += 2
                  self.gah += 1   # If common base class called once result is 4, 5 otherwise.

            a=foo()
            self.failUnless(a.gah==1,"Foo's initialisation failed.")
            b=bar()
            self.failUnless((b.gee,b.gah)==(1,2) , "Bar & Foo's chained initialisation failed.")
            c=bla()
            self.failUnless((c.goo,c.gah)==(2,2) , "Bla & Foo's chained initialisation failed")
            d=barbla()
            self.failUnless((d.gee,d.goo,d.gah)==(2,4,4) , "BarBla, Bla, Bar & Foo's chained initialisation failed")



         def test_AxonType(self):
            "AxonType.__init__ - adds an extra __super method to all objects created from classes with this metaclass simplifying superclass method calling. ttbChecked"
            self.failUnless(type(AxonType) is type,"AxonType is not a python type")
            class base(object):
               __metaclass__ = AxonType

            self.failUnless(type(base._base__super) == super)
            self.multipleInheritanceTest(base)




         def test_AxonObject(self):
            "AxonObject - derives from object, but sets a metaclass of AxonType - to allow superclass method calling simply. ttbChecked"

            self.failUnless( issubclass(AxonObject.__metaclass__,AxonType))
            self.multipleInheritanceTest(AxonObject)


if __name__=='__main__':
   unittest.main()
