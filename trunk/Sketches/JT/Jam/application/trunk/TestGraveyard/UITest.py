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

from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer

from Kamaelia.Apps.Jam.UI.XYPad import XYPad
from Kamaelia.Apps.Jam.Protocol.Osc import Osc
from Kamaelia.Apps.Jam.Internet.UDP import SimplePeer

if __name__ == "__main__":
    FPS = 60

    Graphline(clock = Clock(float(1)/FPS),
              xyPad = XYPad(),
              osc = Osc("/UITest"),
              peer = SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000),
              linkages={("clock", "outbox"):("xyPad", "newframe"),
                        ("xyPad", "outbox"):("osc", "inbox"),
                        ("osc", "outbox"):("peer", "inbox"),
                       }
             ).run()


