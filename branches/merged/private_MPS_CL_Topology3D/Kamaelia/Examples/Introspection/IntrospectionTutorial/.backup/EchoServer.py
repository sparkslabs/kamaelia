#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

FastRestartServer(protocol=EchoProtocol, port=1500).run()

