#!/usr/bin/env python
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
from Axon.Ipc import producerFinished, shutdownMicroprocess

import pymedia.audio.sound as sound


class Resample(component):
    def __init__(self, sample_rate, channels, to_sample_rate, to_channels):
        super(Resample,self).__init__()
        
        self.resampler = sound.Resampler( (sample_rate, channels), (to_sample_rate, to_channels) )
        
    def main(self):
        shutdown=False
        data=""
        while self.anyReady() or not shutdown:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                resampled = str(self.resampler.resample(data))
                self.send(resampled, "outbox")
        
            while self.dataReady("control"):
                msg=self.recv("control")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                self.send(msg,"signal")
                
            if not shutdown:
                self.pause()
            yield 1
