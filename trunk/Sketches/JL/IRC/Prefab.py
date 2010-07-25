#! /usr/bin/env python
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
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Fanout import Fanout
from IRCClient import *

def ComplexIRCClientPrefab(host="127.0.0.1",
                          port=6667,
                          nick="kamaeliabot",
                          nickinfo="Kamaelia",
                          defaultChannel="#kamaeliatest",
                          IRC_Handler=IRC_Client):
    return Graphline(
        CLIENT = TCPClient(host, port),
        PROTO = IRC_Handler(nick, nickinfo, defaultChannel),
        SPLIT = Fanout(["toGraphline", "toTCP"]),
        linkages = {
              ("CLIENT" , "outbox") : ("PROTO" , "inbox"),
              ("PROTO"  , "outbox") : ("SPLIT", "inbox"),
              ("PROTO"  , "heard")  : ("SELF", "outbox"), #passthrough
              ("SELF"  , "inbox") : ("PROTO" , "talk"), #passthrough
              ("SELF"  , "control") : ("PROTO" , "control"), #passthrough
              ("PROTO"  , "signal") : ("CLIENT", "control"),
              ("CLIENT" , "signal") : ("SELF" , "signal"), #passthrough
              ("SPLIT", "toGraphline") : ("SELF", "sendCopy"), #passthrough
              ("SPLIT", "toTCP") : ("CLIENT", "inbox")
              }
        )

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader
    from NiceTickerPrefab import NiceTickerPrefab as NiceTicker
    from Kamaelia.Chassis.Graphline import Graphline
    Graphline(
        reader = ConsoleReader(),
        irc = ComplexIRCClientPrefab(host="irc.freenode.net", nick="kamaeliabot", defaultChannel="#kamtest"),
        display1 = NiceTicker(render_right = 800,render_bottom = 300),
        display2 = NiceTicker(render_right = 800,render_bottom = 300, position = (0, 340)),
        linkages = {
            ("reader", "outbox") : ("irc", "inbox"),
            ("irc", "outbox") : ("display1", "inbox"),
            ("irc", "sendCopy") : ("display2", "inbox")
            }
            
    ).run()
