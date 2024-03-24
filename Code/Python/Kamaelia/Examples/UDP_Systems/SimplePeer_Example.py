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
Simple Kamaelia Example that shows how to use a simple UDP Peer.
A UDP Peer actually sends and recieves however, so we could have
more fun example here with the two peers sending each other messages.

It's worth noting that these aren't "connected" peers in any shape
or form, and they're fixed who they're sending to, etc, which is why
it's a simple peer.
"""

# Checked: 2024/03/24

from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Chargen import Chargen
from Kamaelia.Internet.UDP import SimplePeer
from Kamaelia.Util.PureTransformer import PureTransformer

server_addr = "127.0.0.1"
server_port = 1600

Pipeline(
    Chargen(),
    PureTransformer(lambda x: x.encode("utf8")),
    SimplePeer(receiver_addr=server_addr, receiver_port=server_port),
).activate()

Pipeline(
    SimplePeer(localaddr=server_addr, localport=server_port),
    ConsoleEchoer()
).run()
# RELEASE: MH, MPS
