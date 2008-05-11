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
"""
"""
from Axon.Component import component, scheduler
import Axon
import ao
import vorbissimple
import sys

class AOPlayerComponent(component):
   def __init__(self, id=None):
      super(AOPlayerComponent, self).__init__()
      #if id is None:
      #   id = 'oss'
      #print "FOO1"
      self.dev = ao.AudioDevice("oss")

   def main(self):
      print "FOO"
      while 1:
         print "BAR"
         if self.dataReady("inbox"):
            buff = self.recv("inbox")
            bytes = len(buff)
            sys.stdout.write("\nARRGH\n")
            sys.stdout.flush()
            #self.dev.play(buff)
         yield 1

x= AOPlayerComponent()
gen = x.main()
while 1:
   gen.next()
