#!/usr/bin/env python2.3
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

from Axon.Component import component
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess

class lossyConnector(component):
    Inboxes=["inbox","control"]
    Outboxes=["outbox"]
    def mainBody(self):
        while self.dataReady("inbox"):
            try:
                self.send(self.recv())
            except noSpaceInBox:
                pass # This is the lossy bit although most data will get through normally.
        if self.dataReady("control"):
            mes = self.recv("control")
            if isinstance(mes, producerFinished) or isinstance(mes, shutdownMicroprocess):
                return 0
        return 1
