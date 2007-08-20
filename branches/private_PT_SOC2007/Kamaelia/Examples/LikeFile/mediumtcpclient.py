#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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


# a slightly more complicated example of a TCP client, where we define an echo.

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.likefile import LikeFile, schedulerThread
import time

schedulerThread(slowmo=0.01).start()

PORT = 1900
# This starts an echo server in the background.
SimpleServer(protocol = EchoProtocol, port = PORT).activate()

# give the component time to commence listening on a port.
time.sleep(0.5)

echoClient = LikeFile(TCPClient(host = "localhost", port = PORT))
while True:
    echoClient.put(raw_input(">>> "))
    print echoClient.get()
