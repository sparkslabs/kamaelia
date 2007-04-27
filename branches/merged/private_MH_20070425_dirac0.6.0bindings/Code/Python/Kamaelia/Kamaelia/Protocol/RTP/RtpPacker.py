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
"""
RtpPacker Component
===================

Takes data from a preframer:

   * Creates an RTP Header Object
   * Uses the timestamp & sample count to generate an RTP timestamp

"""
from Axon.Component import component, scheduler

class RtpPacker(component):
   Inboxes=["inbox"]   # List of inbox names if different
   Outboxes=["outbox"] # List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self,label,looptimes,selfstart=0):
      super(RtpPacker, self).__init__() # !!!! Must happen, if this method exists

   def initialiseComponent(self):
      return 1

   def mainBody(self):
      return 1

   def closeDownComponent(self):
      "closeDownComponent"
      pass

__kamaelia_components__  = ( RtpPacker, )


if __name__ =="__main__":
   # myComponent("A",3,1)
   # myComponent("B",2).activate()
   # scheduler.run.runThreads()
   pass
