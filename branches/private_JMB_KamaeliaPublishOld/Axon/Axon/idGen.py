#!/usr/bin/python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
====================
Unique ID generation
====================

The methods of the idGen class are used to generate unique IDs in various forms
(numbers, strings, etc) which are used to give microprocesses and other Axon
objects a unique identifier and name.

* Every Axon.Microprocess.microprocess gets a unique ID
* Axon.ThreadedComponent.threadedcomponent uses unique IDs to identify threads



Generating a new unique ID
--------------------------

Do not use the idGen class defined in this module directly. Instead, use any
of these module methods to obtain a unique ID:

* **Axon.idGen.newId(thing)** - returns a unique identifier as a string based on
  the class name of the object provided

* **Axon.idGen.strId(thing)** - returns a unique identifier as a string based on
  the class name of the object provided

* **Axon.idGen.numId()** - returns a unique identifier as a number

* **Axon.idGen.tupleId(thing)** - returns both the numeric and string versions
  of a new unique id as a tuple (where the string version is based on the class
  name of the object provided)

Calling tupleId(thing) is *not* equivalent to calling numId() then strId(thing)
because doing that would return two different id values! 

Examples::

    >>> x=Component.component()
    >>> idGen.newId(x)
    'Component.component_4'
    >>> idGen.strId(x)
    'Component.component_5'
    >>> idGen.numId()
    6
    >>> idGen.tupleId(x)
    (7, 'Component.component_7')

"""


import debug;
debugger = debug.debug()
debugger.useConfig()
Debug = debugger.debug

# idGen - A class to provide Unique Identifiers
#
# Ids can provide be provided as numerical, string or a tuple.
# 
# numerical ids are integers allocated on a "next integer" basis.
# eg object 1, apple 2, orange 3. (Not object 1, apple 2, orange 3)
#
# string ids consist of the '__str__' of the object, with the numerical
# id tacked on the end.
# 
# tuple ids consists : '(the numerical id, the string id)'
#
class idGen(object):
   """\
   Unique ID creator.

   Use numId(), strId(), and tupleId() methods to obtain unique IDs.
   """
   lowestAllocatedId = 0

   def nextId(self):
      """\
      **INTERNAL**

      Returns the next unique id, incrementing the private class variable
      """
      idGen.lowestAllocatedId = idGen.lowestAllocatedId +1
      return idGen.lowestAllocatedId
   next = nextId # pseudonym

   def idToString(self,thing,aNumId):
      """\
      **INTERNAL**
       
      Combines the 'str()' of the object's class with the id to form a string id
      """
      # This next line takes <class '__main__.foo'>
      # and chops out the __main__.foo part
      r = str(thing.__class__)[8:][:-2] + "_" + str(aNumId)
      return r

   def numId(self):
      """Allocates & returns the next available id"""
      result = self.nextId()
      assert Debug("idGen.numId", 1, "idGen.numId:", result)
      return result

   def strId(self,thing):
      """\
      Allocates & returns the next available id combined with the object's
      class name, in string form
      """
      theId = self.nextId()
      strid = self.idToString(thing,theId)
      assert Debug("idGen.strId", 1, "idGen.strId:", strid)
      return strid

   def tupleId(self,thing):
      """\
      Allocates the next available id and returns it both as a tuple (num,str)
      containing both the numeric version and a string version where it is
      combined with the object's class name.
      """
      theId = self.nextId()
      strId = self.idToString(thing,theId)
      assert Debug("idGen.tupleId", 1, "idGen.tupleId:", theId, strId)
      return theId, strId


newId = idGen().strId
strId=idGen().strId
numId=idGen().numId
tupleId=idGen().tupleId

if __name__ == '__main__':
   class foo: pass
   class bar: pass
   class bibble: pass
   print newId(foo())
   print newId(bar())
   print newId(bibble())
