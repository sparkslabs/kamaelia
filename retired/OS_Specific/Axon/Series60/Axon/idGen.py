#!/usr/bin/python
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
