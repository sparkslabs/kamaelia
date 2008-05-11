#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from Axon.Ipc import producerFinished, shutdownMicroprocess

class BitRateExtractor(component):
    """Extracts the bitrate from pymedia audio frames"""

    def __init__(self, asByteRate=False):
        super(BitRateExtractor, self).__init__()
        self.bitrate = None
        if asByteRate:
            self.multiplier = 0.125
        else:
            self.multiplier = 1

    def main(self):
        done = False
        while not done:

            while self.dataReady("inbox"):
                frame = self.recv("inbox")
                if frame.bitrate != self.bitrate:
                    self.bitrate = frame.bitrate
                    self.send( self.multiplier * self.bitrate, "outbox" )

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    done=True
                self.send(msg, "signal")
                    
            if not done:
                self.pause()
                yield 1

