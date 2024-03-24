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

# This is a quick example of using kamaelia as a general tcp client in your system.


host = "irc.freenode.net"
port = 6667

import Axon.background
import Axon.Handle
import time
import queue
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Internet.TCPClient import TCPClient
Axon.background.background().start()

print( "what channel on freenode?")
channel = input(">>> ") # this is to prevent spammage of the default settings.

client = Axon.Handle.Handle(TCPClient(host = host, port = port)).activate()
time.sleep(1)
client.put("user likefile likefile likefile :likefile\n","inbox")
client.put("nick likefile\n","inbox")
client.put("JOIN %s\n" % channel, "inbox")
while True:
    try:
        print( client.get("outbox"))
    except queue.Empty:
        time.sleep(0.1)



