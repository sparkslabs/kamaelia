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
