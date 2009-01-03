#!/usr/bin/env python2.3
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
Null sink component.  To ignore a component's outbox connect it to this
component and the box will be emptied but not used in any way.  This will be
necessary with syncronized linkages.
"""
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess
class nullSinkComponent(component):
   Inboxes=["inbox","control"]
   Outboxes=[]

   def mainBody(self):
      while self.dataReady("inbox"):
         data = self.recv("inbox")
      if self.dataReady("control"):
         data = self.recv("control")
         if isinstance(data,producerFinished) or isinstance(data, shutdownMicroprocess):
            return 0
      return 1

__kamaelia_components__  = ( nullSinkComponent, )


if __name__ =="__main__":
   print "This module has no system test"
