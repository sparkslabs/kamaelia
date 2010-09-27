#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

Axon.Component.TraceAllSends = True
Axon.Component.TraceAllRecvs = True

FastRestartServer(protocol=EchoProtocol, port=1500).run()

