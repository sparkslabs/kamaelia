#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.Util.PureTransformer import PureTransformer

Backplane("CHAT_ONE").activate()

def EchoEveryone(**kwargs):
        peer = str(kwargs.get("peer", "<>"))
        peerport = str(kwargs.get("peerport", "<>"))
        return Pipeline(
                PureTransformer(lambda x: "%s:%s says %s" % (peer,peerport,x)),
                PublishTo("CHAT_ONE"),
                # ------------
                SubscribeTo("CHAT_ONE"),
            )

FastRestartServer(protocol=EchoEveryone, port=1500).run()
