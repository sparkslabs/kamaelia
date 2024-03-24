#!/usr/bin/python
# -*- coding: utf-8 -*-

# Checked: 2024/03/24

from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

# ------- START OF CODE FRAGMENT NEEDED TO CONNECT TO INTROSPECTOR ----
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.PureTransformer import PureTransformer

Pipeline(
    Introspector(),
    PureTransformer(lambda x: x.encode("utf8")),
    TCPClient("127.0.0.1", 1600),
).activate()
# ------- END OF CODE FRAGMENT NEEDED TO CONNECT TO INTROSPECTOR ----


FastRestartServer(protocol=EchoProtocol, port=1500).run()
