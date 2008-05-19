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
Echo Checker Protocol Component

This component periodically (once per second) sends data to it's outbox, and
then waits for data on it's inbox. When it recieves the data it checks it
against what it sent. Reports "GOOD" if the data matches, reports "BAD" if
the data doesn't match. After a number of iterations it sends a producer
finished message on it's "signal" outbox, and then shuts down. (It expects
this message to go to the appropriate higher level part of the system to
shutdown the CSA/etc)

It is expected this would be wired in with a client component rather than a
server component, but that's not necessarily the case - it is only designed
for checking echo servers.

EXTERNAL CONNECTORS
      * inboxes : ["inbox"]
      * outboxes=["outbox","signal"])

"""

from Axon.Component import component, scheduler
from Axon.Ipc import status

class EchoCheckerProtocol(component):
   import time
   def __init__(self,packetsToSend=100):
      super(EchoCheckerProtocol, self).__init__() # Accept default in/outboxes
      self.packetsToSend=packetsToSend
   def main(self):
      theMessage = "Some Message"*85
      while self.packetsToSend:
         self.send(theMessage, "outbox")
         #while not self.dataReady("inbox"):
         self.pause() # This means we wait for any message on any inbox
         yield status("ready")
         if self.dataReady("inbox"): # If it isn't this, where is it?
            data = self.recv("inbox")
            if data == theMessage:
               #print "GOOD"
               self.packetsToSend -=1
            else:
               print "BAD"
               return
      print "GOOD"
      return

if __name__ == '__main__':
   print "This code has no direct test parts at present"
#   from Kamaelia.SimpleServerComponent import SimpleServer
#
#   SimpleServer(protocol=EchoProtocol, port=1501).activate()
#   scheduler.run.runThreads(slowmo=0)
