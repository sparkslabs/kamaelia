#!/usr/bin/env python2.3
#
# Aim: Full coverage testing of the Axon root module
#

# Test the module loads
import unittest
import sys ; sys.path.append("."); sys.path.append("..")
from Axon import AxonObject, AxonType





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
