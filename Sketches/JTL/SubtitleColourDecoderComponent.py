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
import string

class Colour(object):
   def __init__(self, col = 0xFFFFFF):
      self.colourval = col
      
   def getColour(self):
      return self.colourval
   
   def getPygameColour(self):
      r = self.colourval / 0x010000
      g = (self.colourval / 0x000100) % 0x000100
      b = self.colourval % 0x000100
      return (r,g,b)

from Axon.Component import component
from Axon.Ipc import producerFinished
#from SubtitleFilter import SubtitleFilter2
class SubtitleColourDecoder(object):
   def __init__(self):
      self.intag = False
      self.leftover = ""
   def filter(self, newtext = ""):
      if self.leftover != "":
         newtext = self.leftover + newtext
         self.leftover = ""
      pos = 0
      try:
         if self.intag:
            end = newtext.index("/>",pos) + 2
            self.intag = False
            self.leftover = newtext[end:]
            num = newtext[pos + 14:end - 3]
            if newtext[pos:pos + 14] == '<font color="#' and newtext[end - 3] == '"' and self.ishex(num):
               return Colour(int(num, 16))
            return ""
         else:
            pnext = newtext.index("<",pos)
            self.leftover = newtext[pnext:]
            self.intag = True
            return newtext[pos:pnext]
      except ValueError, e:
         # Got to end of string without finding next tag or end of tag.
         if not self.intag:
            return newtext[pos:]
         else:
            self.leftover = newtext[pos:] # in case we have got '/' but not '>'
            return None
   def ishex(self, s):
      for x in s:
         if not x in string.hexdigits:
            return False
      return True
      
class SubtitleColourDecoderComponent(component):
   def __init__(self):
      super(SubtitleColourDecoderComponent, self).__init__() # Take default in/out boxes
      self.filt = SubtitleColourDecoder()
      
   def mainBody(self):
      outmes = self.filt.filter()
      if outmes:
         self.send(outmes)
      elif self.dataReady():
         mes = self.recv()
         outmes = self.filt.filter(mes)
         if outmes:
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
