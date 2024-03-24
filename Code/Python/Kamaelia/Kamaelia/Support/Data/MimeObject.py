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

class mimeObject(object):
   """Accepts a Mime header represented as a dictionary object, and a body
   as a string. Provides a way of handling as a coherant unit.
   ATTRIBUTES:
      header : dictionary. (keys == fields, values = field values)
      body : body of MIME object
   """
   def __init__(self, header = {}, body = "",preambleLine=None):
      "Creates a mimeObect"
      self.header = dict(header)
      self.body = body
      if preambleLine:
         self.preambleLine = preambleLine
      else:
         self.preambleLine = None

   def __str__(self):
      """Dumps the Mime object in printable format - specifically as a formatted
      mime object"""
      result = ""
      for anItem in self.header.iteritems():
         (key,[origkey, value]) = anItem                   # For simplifying/checking testing
         result = result + origkey + ": "+value + "\n"
      result = result + "\n"
      result = result + self.body
      if self.preambleLine:
         result = str(self.preambleLine) + "\n"+result + self.body
      return result


if __name__ =="__main__":
   print ("No test harness as yet")
   print ("This file was spun out from the Mime request parsing component")
