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
"""
Bit Field Record Support
========================

1. subclass bfrec
2. Define a class var "fields"
3. The value for this field should be a list of "field"s, created by calling the static method
   field.mkList. This takes a list of tuples, one tuple per field.
   (fieldname, bitwidth, None or list)

   See  testBFR for an example.

Usage::

   >> import bitfieldrec
   >> bfrec,field = bitfieldrec.bfrec,bitfieldrec.field
   >> reload(bitfieldrec)

Currently only supports packing. Does not support unpacking (yet).
"""

from Axon import AxonObject

class field(str):
   size=0
   extra = None
   #
   def mkList(fieldDefs):
      result = list()
      for definition in fieldDefs:
         name, size,extra = definition
         j = field(name)
         j.size = size
         j.extra=extra
         result.append(j)
      return result
   mkList=staticmethod(mkList)

class bfrec(AxonObject):
   fields = []
   csize = 8
   def __init__(self, **args):
      try:
         self.fields = field.mkList(args["fields"])
      except KeyError:
         pass
      for i in self.fields:
         try:
            self.__dict__[i] = args[i]
         except KeyError:
            if i.extra is list:
               self.__dict__[i] = []
            else:
               self.__dict__[i] = 0
   def structureSize(self):
      bits = 0
      # Calculate the size of the result.
      for aField in self.fields:
         if aField.extra is list:
            bits = bits + (aField.size * len(self.__dict__[aField]))
         else:
            bits = bits + aField.size
      return bits

   def pack(self):
      def serialiseable(convert,aField):
         """ Returns an iterable collection of values. (eg list) Either an
         existing one, or puts scalar/singleton values into a list. Doing
         this removes a special case."""

         # If the value is not a simple value
         if aField.extra is not None:
            # Return the values stored. (likely a list)
            values = convert[aField]
         else:
            # Put the simple value into a list
            values = [convert[aField]]
         return values  # This will always be an iterable type - likely a list.

      csize = self.csize
      fields = self.fields
      convert = self.__dict__
      space,value= 8,0
      r=[]

      # Check that the structure will fit into complete bytes/chunks without any
      # unexpected pad bits. (ie whole bytes/whole chunks)
      assert (self.structureSize() % csize) == 0, "Structure is not a multiple of packsize"

      # Do the actual conversion of fields
      for aField in fields:
         fmax = 2**aField.size-1   # Maximum possible value in the field.

         # We get the value(s) in this field. Given the field may be a list of values or
         # similar we ensure that the value is iterable - this eliminates special cases
         # in the conversion.
         values = serialiseable(convert,aField)

         for aValue in values:  # Might only be one value! Might be 10 bytes wide, non-aligned.
            assert 0 <= aValue <= fmax, "Field value out of range "+aField+"="+str(convert[aField])+" max"+str(fmax)
            fsize = aField.size

            # The conversion of a field is a loop to handle the case whereby a field
            # needs to be stored in multiple bytes/chunks.
            while fsize:  
               # Insert as much of the field into the current value/chunk as we can
               if fsize <= space:
                  # The field size for this value fits into available space
                  data = aValue & (2**fsize)-1  # Crop the value to the field size
                  space = space - fsize         # Note reduced size
                  value = value + (data << space)  # Insert value into space
                  fsize = 0                        # Indicate field inserted

               else:
                  # The field is too wide for the value - it needs to span values, so we
                  # store as many most significant bits as possible, and come back again
                  # for another loop with the reduced value.
                  data = aValue >> (fsize - space) # Store the top most bits that will fit
                  value = value + data             # 
                  aValue = aValue & (2**(fsize - space))-1  # Chop them out of the value
                  fsize = fsize - space            # whilst noting reduced field width
                  space = space-csize              # and reduced space in the current chunk/byte
                  if space <0: space =0            # Chop at zero.

               # If we've used up the current value/chunk space, store it in the result
               # And allocate a new one.
               if space ==0:         # Have we filled up a chunk (normally a byte)
                  if value > 2**csize-1:  # Sanity Check!
                     raise ValueError("Bad Value", value)
                  r.append(value)    # Add the value onto the result
                  space=csize        # Reset available space
                  value = 0          # Reset value

      return r # result is a list of integer values.

if __name__ == "__main__":
   def bin(value,width=8):
      aList = [ value ]
      def _bin(seq): return [ seq[0]/2, seq[0]%2]+ seq[1:]
      while aList[0]>1: aList = _bin(aList)
      r = reduce(lambda x, y: x+y, list(map(lambda x : str(x), aList)) )
      r = "0"*(width-len(r))+r
      return r

   class testBFR(bfrec):#
      fields = field.mkList([("hello", 4, None),
                              ("goodbye",4,None),
                              ("Whatever", 5,list),
                              ("SoWhat", 32, None),
                              ("Bibble", 3, None)
                           ])
   a=testBFR(hello=10,
            goodbye=2,
            Whatever=[10,10,10,10,10,10,10,10,10],
            SoWhat=10,
            Bibble=7)
   a=testBFR()
   a.hello=10
   a.goodbye=2
   a.Whatever=[10,10,10,10,10,10,10,10,10]
   a.SoWhat=10
   a.Bibble=7
   print (a.pack())

   print (map(lambda x:bin(x),a.pack()))
