#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

import Axon

class Forwarder(Axon.Component.component):
        Inboxes = {
                "inbox"             : "Received messages are forwarder to outbox",
                "secondary-inbox"   : "Received messages are forwarder to outbox",
                "control"           : "Received messages are forwarder to signal",
                "secondary-control" : "Received messages are forwarder to signal",
        }
        def __init__(self, **argv):
                super(Forwarder, self).__init__(**argv)

        def main(self):
                while True:
                        while self.dataReady("inbox"):
                                data = self.recv("inbox")
                                self.send(data,"outbox")

                        while self.dataReady("secondary-inbox"):
                                data = self.recv("secondary-inbox")
                                self.send(data,"outbox")

                        while self.dataReady("control"):
                                data = self.recv("control")
                                self.send(data, "signal")
                                return

                        while self.dataReady("secondary-control"):
                                data = self.recv("secondary-control")
                                self.send(data, "signal")
                                return

                        if not self.anyReady():
                                self.pause()
                        yield 1
