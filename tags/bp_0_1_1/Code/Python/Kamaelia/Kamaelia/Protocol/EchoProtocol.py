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
Echo Protocol Component

Based on the test code for the ICA & Simple Server.
Simply copies it's input to it's output.

EXTERNAL CONNECTORS
      * inboxes : ["inbox"]
      * outboxes=["outbox"])
   Data recieved on "inbox" is copied to "outbox"
"""

from Axon.Component import component, scheduler

class EchoProtocol(component):
   import time
   allEchoers = []
   def __init__(self):
      self.__super.__init__() # Accept default in/outboxes
      EchoProtocol.allEchoers.append(self)

   def mainBody(self):
      self.pause()
      if self.dataReady("inbox"):
         data = self.recv("inbox")
         #print "NetServ : We were sent data - "
         #print "We should probably do something with it now? :-)"
         #print "I know, let's sling it straight back at them :-)"
         self.send(data,"outbox")
      return 1

if __name__ == '__main__':
   from Kamaelia.SimpleServerComponent import SimpleServer

   SimpleServer(protocol=EchoProtocol, port=1501).activate()
   scheduler.run.runThreads(slowmo=0)
