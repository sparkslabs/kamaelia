#!/usr/bin/python
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
"""
This is a simple proxy to relay multicast data from a given multicast
group and port as a TCP Service on a given port. It's worth noting that
this is one way - any data from the TCP connection is discarded.
"""

from Kamaelia.Util.Backplane import Backplane, publishTo, subscribeTo
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Util.PipelineComponent import pipeline
from config import mcast_group, mcast_port, mcast_tcp_splitter_port

p = Backplane("MulticastProxy").activate()


pipeline(
   Multicast_transceiver("0.0.0.0", mcast_port, mcast_group, 0),
   publishTo("MulticastProxy"),
).activate()

def RelayMulticastData(): # Protocol handler for each connected client
     return subscribeTo("MulticastProxy")

SimpleServer( RelayMulticastData, mcast_tcp_splitter_port).run()
