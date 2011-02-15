#!/usr/bin/env python
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
"""\
=================
Axon base classes
=================

What is defined here is a metaclass that is used as a base class for some key
classes in Axon.

It was originally created to allow super class calling in a slightly nicer
manner in terms of syntactic sugar easier to get right that still
has the good effects of "super" in a multiple inheritance scenario. **Use of
this particular feature has been deprecated** because of more subtle issues in
inheritance situations.

However this metaclass has been retained (and is still used) for possible future
uses.

* AxonObject is the base class for Axon.Microprocess.microprocess and
  Axon.Linkage.linkage

"""

class AxonType(type):
   """\
   Metaclass for Axon objects.
   """
    
   def __init__(cls, name, bases, dict):
      """\
      Override creation of class to set a 'super' attribute to what you get
      when you call super().

      **Note** that this 'super' attribute is deprecated - there are some subtle
      issues with it and it should therefore be avoided.
      """
      super(AxonType, cls).__init__(name, bases, dict)
      setattr(cls, "_%s__super" % name, super(cls))

class AxonObject(object):
   """\
   Base class for axon objects.

   Uses AxonType as its metaclass.
   """
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
