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
# Aim: Full coverage testing of the Axon root module
#

# Test the module loads
import unittest
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
