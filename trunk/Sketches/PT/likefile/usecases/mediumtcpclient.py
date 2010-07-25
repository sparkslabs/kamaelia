#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# a slightly more complicated example of a TCP client, where we define an echo.

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.likefile import LikeFile, schedulerThread
import time

schedulerThread(slowmo=0.01).start()

PORT = 1900
# This starts an echo server in the background.
SimpleServer(protocol = EchoProtocol, port = PORT).activate()

# give the component time to commence listening on a port.
time.sleep(0.5)

echoClient = LikeFile(TCPClient(host = "localhost", port = PORT))
while True:
    echoClient.put(raw_input(">>> "))
    print echoClient.get()