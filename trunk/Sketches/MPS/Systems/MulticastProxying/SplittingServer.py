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
Splitting server. This expects a single inbound connection on one port and spits it out to all recipients who connect on another port. This can be
used as an alternate server for the TCPRelayMulticast to connect to, and
it would expect to be fed using MulticastTCPClientRelay.

"""

from Kamaelia.Util.Backplane import Backplane, publishTo, subscribeTo
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.SingleServer import SingleServer
from config import tcp_tcp_splitter_port, tcp_splitter_client_port

p = Backplane("Splitting").activate()

pipeline(
    SingleServer( tcp_tcp_splitter_port ),
    publishTo("Splitting"),
).activate()

def SubscribeToSplitData(): # Protocol handler for each connected client
     return subscribeTo("Splitting")

SimpleServer( SubscribeToSplitData, tcp_splitter_client_port).run()
