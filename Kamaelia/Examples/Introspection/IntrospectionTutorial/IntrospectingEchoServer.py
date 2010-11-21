#!/usr/bin/python
# -*- coding: utf-8 -*-
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

# ------- START OF CODE FRAGMENT NEEDED TO CONNECT TO INTROSPECTOR ----
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient

Pipeline(
    Introspector(),
    TCPClient("127.0.0.1", 1600),
).activate()
# ------- END OF CODE FRAGMENT NEEDED TO CONNECT TO INTROSPECTOR ----


FastRestartServer(protocol=EchoProtocol, port=1500).run()

