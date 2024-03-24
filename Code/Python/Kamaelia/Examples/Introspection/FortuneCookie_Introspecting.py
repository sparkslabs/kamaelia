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
# Checked 2024/03/24

import random
from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

from Kamaelia.Util.Introspector import Introspector

# Start the introspector and connect to a local visualiser
Pipeline(
    Introspector(),
    PureTransformer(lambda x: x.encode("utf8")),
    TCPClient("127.0.0.1", 1600),
).activate()

clientServerTestPort=random.randint(1501,1599)

SimpleServer(protocol=FortuneCookieProtocol, port=clientServerTestPort).activate()

Pipeline(TCPClient("127.0.0.1",clientServerTestPort),
         PureTransformer(lambda x: x.decode("utf8")),
         ConsoleEchoer()
        ).run()

