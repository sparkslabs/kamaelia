#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

