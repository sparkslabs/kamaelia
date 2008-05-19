#!/usr/bin/env python
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
#
# Simple test harness for integrating TCP clients and servers in one system, sharing selector components etc.
#
#

from Axon.Scheduler import scheduler as _scheduler

from Kamaelia.SimpleServerComponent import SimpleServer as _SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
from Kamaelia.Util.ConsoleEcho import consoleEchoer as _consoleEchoer
from Kamaelia.Util.Chargen import Chargen as _Chargen

import Axon as _Axon

from Axon.Component import component, scheduler
class InternetHandlingTest(component):
   def initialiseComponent(self):
      import random
      clientServerTestPort=random.randint(1500,1599)
      server=_SimpleServer(protocol=_Chargen, port=clientServerTestPort).activate()
      self.server=server
      self.addChildren(server)

      conecho = _consoleEchoer()
      self.addChildren(conecho)

      client=_TCPClient("127.0.0.1",clientServerTestPort)
      self.addChildren(client)
      self.link((client,"outbox"), (conecho,"inbox"))
      return _Axon.Ipc.newComponent(*(self.children))

   def mainBody(self):
      self.pause()
      return 1
if __name__ == '__main__':
   t = InternetHandlingTest().activate()

   _scheduler.run.runThreads(slowmo=0)

