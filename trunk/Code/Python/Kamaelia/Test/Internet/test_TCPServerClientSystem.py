#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
#
# Simple test harness for integrating TCP clients and servers in one system, sharing selector components etc.
#
#

from Axon.Scheduler import scheduler as _scheduler

from Kamaelia.SimpleServerComponent import SimpleServer as _SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
from Kamaelia.Util.Console import ConsoleEchoer as _ConsoleEchoer
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

      conecho = _ConsoleEchoer()
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

