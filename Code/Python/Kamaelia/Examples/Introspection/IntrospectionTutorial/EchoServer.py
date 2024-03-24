#!/usr/bin/python
# -*- coding: utf-8 -*-
# Checked: 2024/03/24

import Axon
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

Axon.Component.TraceAllSends = True
Axon.Component.TraceAllRecvs = True

FastRestartServer(protocol=EchoProtocol, port=1500).run()

