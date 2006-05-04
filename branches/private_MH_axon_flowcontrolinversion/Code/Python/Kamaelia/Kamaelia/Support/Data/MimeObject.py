#!/usr/bin/env python2.3
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
   print "No test harness as yet"
   print "This file was spun out from the Mime request parsing component"
