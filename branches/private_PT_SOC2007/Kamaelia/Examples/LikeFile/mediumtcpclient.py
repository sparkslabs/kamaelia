#!/usr/bin/env python

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