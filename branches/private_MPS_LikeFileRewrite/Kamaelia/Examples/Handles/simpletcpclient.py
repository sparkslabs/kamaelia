#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

# This is a quick example of using kamaelia as a general tcp client in your system.


host = "irc.freenode.net"
port = 6667

import Axon.background
import Axon.Handle
import time
import Queue
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Internet.TCPClient import TCPClient
Axon.background.background().start()

print "what channel on freenode?"
channel = raw_input(">>> ") # this is to prevent spammage of the default settings.

client = Axon.Handle.Handle(TCPClient(host = host, port = port)).activate()
time.sleep(1)
client.put("user likefile likefile likefile :likefile\n","inbox")
client.put("nick likefile\n","inbox")
client.put("JOIN %s\n" % channel, "inbox")
while True:
    try:
        print client.get("outbox")
    except Queue.Empty:
        time.sleep(0.1)



