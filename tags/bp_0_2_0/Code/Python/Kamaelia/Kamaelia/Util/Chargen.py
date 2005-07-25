#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# Simple udp /multicast/ sender and receiver
# Logically these map to being a single component each
#

import socket
import Axon

class Chargen(Axon.Component.component):
   # SMELL: Might be nice to set a rate.
   def main(self):
      while 1:
         self.send("Hello World", "outbox")
         yield 1

def tests():
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.ConsoleEcho import consoleEchoer

   class testComponent(Axon.Component.component):
      def main(self):
        chargen= Chargen()
        display = consoleEchoer()

        self.link((chargen,"outbox"), (display,"inbox"))
        self.addChildren(chargen, display)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           self.pause()
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":

    tests()
     # Needed to allow import
