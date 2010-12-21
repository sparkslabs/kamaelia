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


class MimeDict(dict):
   def __init__(self, **args):
      super(MimeDict,self).__init__(**args)
      self.insertionorder = []
      self.invalidSource = False
      # This is HIDEOUS
      for k in self.keys():
         if isinstance(self[k], list):
            if self[k] == []:
                self.insertionorder.append(k)
            else:
               for i in self[k]:
                  self.insertionorder.append(k)
         else:
            self.insertionorder.append(k)
      try:
         self["__BODY__"]
      except KeyError:
         self["__BODY__"] = ""

   def __setitem__(self,i,y):
      super(MimeDict, self).__setitem__(i,y)
      if i != "__BODY__":
           self.insertionorder = [ x for x in self.insertionorder if x != i ]
           if isinstance(y,list):
              for _ in y:
                 self.insertionorder.append(i)
           else:
              self.insertionorder.append(i)

   def __delitem__(self,y):
      self.insertionorder = [ x for x in self.insertionorder if x != y ]
      super(MimeDict, self).__delitem__(y)

   def __str__(self):
      # This is HIDEOUS
      result = []

      seen = {}
      for k in self.insertionorder:
         if k == "__BODY__": continue
         try:
            seen[k] += 1
         except KeyError:
            seen[k] = 0
         if isinstance(self[k], list):
            try:
               value = self[k][seen[k]]
            except IndexError: # Empty list, empty value
               value = ""
         else:
            value = self[k]
         result.append("%s: %s\r\n" % (k,value))

      result.append("\r\n")
      result.append(self["__BODY__"])
      resultString = "".join(result)
      if self.invalidSource:
         return resultString[2:]
      else:
         return resultString

   def fromString(source):
      import sre
      result = {}
      insertionorder = []
      fail = False
      originalsource = source # preserve original in case of broken header
      # The leading space in the headervalue RE prevents a continuation line
      # being treated like a key: value line.
      headervalueRE_s = "^([^: ]+[^:]*):( ?)([^\r]+)\r\n" # TODO: This could be optimised
      continuationHeaderRE_s = "^( +[^\r\n]*)\r\n"
      match = sre.search(headervalueRE_s,source)

      # Search for header lines
      inHeader = True
      key = None

      while True: # We break out this loop when matching fails for any reason
         if match:
            (key, spaces,value) = match.groups()
            if value == " " and not spaces: # Empty header
                  value = ""
            try:
               result[key].append(value)
            except KeyError:            
               result[key] = value
            except AttributeError:
               result[key] = [ result[key], value ]
            insertionorder.append(key)

         if not match and key:
            # We have already matched a line. This may be continuation.
            match = sre.search(continuationHeaderRE_s, source)
            if not match:  break
            (value,) = match.groups()
            if isinstance(result[key], list):
               # Append to last item in the list
               result[key][len(result[key])-1] += "\r\n" + value
            else:
               result[key] += "\r\n" + value

         if not match:  break

         source = source[match.end():]
         match = sre.search(headervalueRE_s,source)

      # End of header lines. Start of source should be "\r\n"
      #
      # If it isn't, the header is invalid, and the entire original
      # source becomes the __BODY__, and all keys aside from that removed.
      #
      if source[:2]=="\r\n":
         source = source[2:]
      else:
         source = originalsource
         result = {}
         insertionorder = []
         fail = True
      result["__BODY__"]=source
      md = MimeDict(**result)
      md.insertionorder = insertionorder
      md.invalidSource = fail 
      return md
   fromString = staticmethod(fromString)
