#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class TwoWaySplitter(Axon.Component.component):
    Outboxes = { "outbox"  : "",
                 "outbox2" : "",
                 "signal"  : "",
                 "signal2" : "",
               }

    def main(self):
        done=False
        while not done:

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data, "outbox")
                self.send(data, "outbox2")

            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data, "signal")
                self.send(data, "signal2")
                if isinstance(data, (producerFinished, shutdownMicroprocess)):
                    done=True

            self.pause()
            yield 1
