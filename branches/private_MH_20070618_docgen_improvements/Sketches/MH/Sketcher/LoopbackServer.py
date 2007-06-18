#!/usr/bin/env python

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.EchoProtocol import EchoProtocol

SimpleServer(protocol=EchoProtocol, port=1500).run()
