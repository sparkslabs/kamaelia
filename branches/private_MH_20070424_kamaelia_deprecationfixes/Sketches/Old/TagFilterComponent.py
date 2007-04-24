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
