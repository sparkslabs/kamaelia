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
import string


class Colour(object):
   """This is a general colour class and could possibly be pulled out into a
   general datatypes module for reuse and extension to increase the capabilities
   which are currently fairly limited."""
   def __init__(self, col = 0xFFFFFF):
      """Creates the Colour object setting the colour by passing a 24bit integer
      with 8 bits for each of red, green and blue."""
      self.colourval = col
      
   def getColour(self):
      """Returns the integer value of the current colour."""
      return self.colourval
   
   def getPygameColour(self):
      """Returns an (R,G,B) tuple suitable for use with pygame."""
      r = self.colourval / 0x010000
      g = (self.colourval / 0x000100) % 0x000100
      b = self.colourval % 0x000100
      return (r,g,b)

from Axon.Component import component
from Axon.Ipc import producerFinished
#from SubtitleFilter import SubtitleFilter2
class SubtitleColourDecoder(object):
   """Processes text as received from the subtitle server removing tags (HTML
   style markup) and if they are colour tags then it will will also return the
   colour.  Filtered text is returned."""
   def __init__(self):
      self.intag = False # self.intag should be true if the current scanning position is inside markup.
      self.leftover = "" # self.leftover is used to store the undecodable sections that need to wait for more data or just another empty string call to allow multiple returns.
   def filter(self, newtext = ""):
      """Call it with text to filter.  It will return either
         1) Filtered text containing no tags.  More text may be available if called again.
         2) A Colour object if it has decoded a colour tag.  More text may be available if called again.
         3) An empty string "".  More text may be available if called again.
         3) None.  No more text is available unless more is passed to it for filtering.
      """
      if self.leftover != "":
         newtext = self.leftover + newtext
         self.leftover = ""
      if self.intag:
         try:
            end = newtext.index("/>") + 2 # Search for end of markup.  Will throw ValueError if not found.
         except ValueError, e:
            # If we haven't got the end of the tag we need more data.
            # Save what we have.
            self.leftover = newtext[:] 
            # return None to indicate that we have no more text to return without data.
            return None         
         # This code only runs if exception not thrown. i.e. "/>" was found.
         self.intag = False
         self.leftover = newtext[end:] # Save anything after the markup to self.leftover.
         num = newtext[14:end - 3] # Extract the hex if it is a proper colour tag.
         if newtext[:14] == '<font color="#' and newtext[end - 3] == '"' and self.ishex(num):
            # It is a colour tag.  Return the colour object.
            return Colour(int(num, 16))
         # Not a colour tag.  Return empty string but can process more if called again.  Text after the tag was saved to self.leftover
         return ""
      else: # Not in a tag.
         try:
            pnext = newtext.index("<") # Find next tag start
         except ValueError, e:
            # If everything we have is before any tag starts we can just return it.
            return newtext[:]
         #Tag has been found or exception would have been thrown.
         self.leftover = newtext[pnext:] # Saves start of tag onwards.
         self.intag = True
         return newtext[:pnext] #Returns text that precedes the tag.
            
   def ishex(self, s):
      """A utility function to check that all the characters in a string are
      valid hexidecimal digits."""
      for x in s:
         if not x in string.hexdigits:
            return False
      return True
      
class SubtitleColourDecoderComponent(component):
   """This is more or less the standard filter component with a
   SubtitleColourDecoder filter being used.  This class could be refactored out
   and a factory could be used."""
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
