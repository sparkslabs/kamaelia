#!/usr/bin/python
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
#
# Very simple Peer to peer radio player.
#
# We have essentially 2 trees constructed - a mesh construction tree and a data tree.
# There are therefore 2 ports for each peer:
#
# control port - request to connect. Either told to connect to a
#    new port number, or given a new ip/port to request to connect to
#
# data port - connecting to here gets you the data. Its good form
#    to ask on the control port first if you can connect there.
#
# As a result that's why there's two SimpleServer instances.
#

import Axon

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient

from likefile import *
background = schedulerThread().start()

class Echo(Axon.Component.component):
   def main(self):
      while 1:
          while self.dataReady("inbox"):
              self.send(self.recv("inbox"), "outbox")
          yield 1

SimpleServer(protocol=Echo, port=1600).activate()

time.sleep(1)

#
# We can then write code here to demo the use of likefile with TCPClient.
#
