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
This is a simple proxy to relay data from a TCP Server out over multicast.
This is designed to be used with MulticastTCPRelay to allow tunnelling of
multicast over TCP in a single direction.
"""

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from config import multicast_group, multicast_port, mcast_tcp_splitter_ip, mcast_tcp_splitter_port

pipeline(
   TCPClient(mcast_tcp_splitter_ip, mcast_tcp_splitter_port),
   Multicast_transceiver("0.0.0.0", 0, multicast_group, multicast_port),
).activate()
