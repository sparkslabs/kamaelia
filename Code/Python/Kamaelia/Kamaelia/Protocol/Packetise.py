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

import Axon

class MaxSizePacketiser(Axon.Component.component):
    """\
This is a simple class whose purpose is to take a data stream and
convert it into packets of a maximum size. 

The default packet size is 1000 bytes. 

This component was created due to limitations of multicast meaning packets
get discarded more easily over a certain size.

Example usage::

    Pipeline(
        ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000,
                        chunkrate=50),
        SRM_Sender(),
        blockise(), # Ensure chunks small enough for multicasting!
        Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
    ).activate()

This component acts as a simple filter - data is expected on inboxes
and packets come out the outbox. 

This component does not terminate.
"""
    def __init__(self, maxsize=1000):
        super(MaxSizePacketiser, self).__init__()
        self.maxsize=maxsize
    def main(self):
        maxsize = self.maxsize
        buffer = ""
        while 1:
            while self.dataReady("inbox"):
                buffer = buffer + self.recv("inbox")
                while len(buffer) > maxsize:
                    send = buffer[:maxsize]
                    buffer = buffer[maxsize:]
                    self.send(send, "outbox")
                else:
                    send = buffer
                    buffer = ""
                    self.send(send, "outbox")
            if not self.anyReady():
                self.pause()
            yield 1

__kamaelia_components__  = ( MaxSizePacketiser, )

if __name__ == "__main__":

    from Kamaelia.Chassis.Pipeline import Pipeline
    class packetSizeChecker(Axon.Component.component):
        def __init__(self, expectedSize=1000):
            super(packetSizeChecker, self).__init__()
            self.expectedSize = expectedSize
        def main(self):
            received = 0
            while 1:
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    received += len(data)
                    if len(data) > self.expectedSize:
                        print ("WARNING, incorrect packet size!")
                print ("GOT:", received)
                if not self.anyReady():
                    self.pause()
                yield 1

    class BigPackets(Axon.Component.component):
        def main(self):
            data = 0
            while 1:
                self.send("hello"*1000, "outbox")
                data += len("hello")*1000
                print ("SENT", data)
                yield 1

    Pipeline(
        BigPackets(),
        MaxSizePacketiser(1000),
        packetSizeChecker(1000),
    ).run()
