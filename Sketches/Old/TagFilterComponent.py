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

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX TODO
#
# A useful component in its own right. Move to Kamaelia.Codec, or perhaps
# make a new category, eg. Kamaelia.Text or Kamaelia.Markup?
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

from Axon.Component import component
#from SubtitleFilter import SubtitleFilter2
class TagFilter(object):
   """A simple filter of text between '<' and '/>' tags."""
   def __init__(self):
      self.intag = False
      self.leftover = ""
   def filter(self, newtext):
      if self.leftover != "":
         newtext = self.leftover + newtext
         self.leftover = ""
      outstring = ""
      pos = 0
      try:
         while True:
            if self.intag:
               pos = newtext.index("/>",pos) + 2
               self.intag = False
            else:
               pnext = newtext.index("<",pos)
               outstring = outstring + newtext[pos:pnext]
               self.intag = True
               pos = pnext
      except ValueError, e:
         # Got to end of string without finding next tag or end of tag.
         if not self.intag:
            outstring = outstring + newtext[pos:]
         else:
            self.leftover = newtext[pos:] # in case we have got '/' but not '>'
         return outstring
class TagFilterComponent(component):
   def __init__(self):
      super(TagFilterComponent, self).__init__() # Take default in/out boxes
      self.filt = TagFilter()
      
   def mainBody(self):
      if self.dataReady():
         mes = self.recv()
         outmes = self.filt.filter(mes)
         if outmes != "":
            self.send(outmes)
      if self.dataReady("control"):
         mes = self.recv("control")
         if isinstance(mes, producerFinished):
            self.send(mes, "signal")
            return 0
      return 1
            
   def closeDownComponent(self):
      outmes = self.filt.filter("")
      if outmes != "":
         self.send(outmes)
