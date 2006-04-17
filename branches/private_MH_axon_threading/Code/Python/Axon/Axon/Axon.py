#!/usr/bin/env python2.3
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
#
# Define a metaclass that allows super class calling in a slightly nicer
# manner in terms of syntactic sugar/easier to get right that still has
# the good effects of "super" in a multiple inheritance scenario.
#
#

class AxonType(type):
   def __init__(cls, name, bases, dict):
      super(AxonType, cls).__init__(name, bases, dict)
      setattr(cls, "_%s__super" % name, super(cls))

class AxonObject(object):
   __metaclass__ = AxonType
   pass

if __name__ == "__main__":

   class foo(AxonObject):
      def __init__(self):
         self.gah =1
         print "foo", self

   class bar(foo):
      def __init__(self):
         super(bar, self).__init__()
         self.gee = 1
         self.gah += 1
         print "bar", self

   class bla(foo):
      def __init__(self):
         super(bla, self).__init__()
         self.goo = 2
         self.gah += 1
         print "bla", self

   class barbla(bar,bla): # Classic hardcase - diagram inheritance.
      def __init__(self):
         super(barbla, self).__init__()
         self.gee += 1
         self.goo += 2
         self.gah += 1   # If common base class called once result is 4, 5 otherwise.
         print "barbla", self

   a=foo()
   assert a.gah==1,"Foo's initialisation failed"
   b=bar()
   assert (b.gee,b.gah)==(1,2) , "Bar & Foo's chained initialisation failed"
   c=bla()
   assert (c.goo,c.gah)==(2,2) , "Bla & Foo's chained initialisation failed"
   d=barbla()
   assert (d.gee,d.goo,d.gah)==(2,4,4) , "BarBla, Bla, Bar & Foo's chained initialisation failed"
