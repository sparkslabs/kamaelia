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

from Kamaelia.Apps.Jam.Internet.UDP_ng import SimplePeer, UDPSender
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Apps.Jam.Protocol.Osc import Osc, DeOsc
from Kamaelia.Util.OneShot import OneShot

Pipeline(OneShot(("/Jam/Connect", 2005)), Osc(),
#         UDPSender(receiver_addr="127.0.0.1", receiver_port=2001)).run()
         SimplePeer(localaddr="127.0.0.1", localport=2005, receiver_addr="127.0.0.1", receiver_port=2001), DeOsc(0), ConsoleEchoer()).run()
