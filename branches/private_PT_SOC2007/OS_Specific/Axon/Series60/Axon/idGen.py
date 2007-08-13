#!/usr/bin/python
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

#import debug;
#debugger = debug.debug()
#debugger.useConfig()
#Debug = debugger.debug

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
   "idGen() - idsequence generator"
   lowestAllocatedId = 0

   def nextId(self):
      """**INTERNAL** - 'IG.nextId()' - returns the next id,
      incrementing the private class variable """
      idGen.lowestAllocatedId = idGen.lowestAllocatedId +1
      return idGen.lowestAllocatedId
   next = nextId # pseudonym

   def idToString(self,thing,aNumId):
      """**INTERNAL** - 'IG.idToString(thing,numId)' - Combines the
      'str()' of the object's class with the id to form a string id"""
      # This next line takes <class '__main__.foo'>
      # and chops out the __main__.foo part
      r = str(thing.__class__)[8:][:-2] + "_" + str(aNumId)
      return r

   def numId(self):
      """'IG.numId()' - Allocates & returns the next available id"""
      result = self.nextId()
#      assert Debug("idGen.numId", 1, "idGen.numId:", result)
      return result

   def strId(self,thing):
      """'IG.strId(object)' - Allocates & returns the next available id
      combined with the object's class name, in string form"""
      theId = self.nextId()
      strid = self.idToString(thing,theId)
#      assert Debug("idGen.strId", 1, "idGen.strId:", strid)
      return strid

   def tupleId(self,thing):
      """'IG.tupleId(thing)' -> (IG.numId(), IG.strId(thing)),
      but with ids the same in num & str"""
      theId = self.nextId()
      strId = self.idToString(thing,theId)
#      assert Debug("idGen.tupleId", 1, "idGen.tupleId:", theId, strId)
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
