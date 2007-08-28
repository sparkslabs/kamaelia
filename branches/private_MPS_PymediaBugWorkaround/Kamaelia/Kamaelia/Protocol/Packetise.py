#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
                        print "WARNING, incorrect packet size!"
                print "GOT:", received
                if not self.anyReady():
                    self.pause()
                yield 1

    class BigPackets(Axon.Component.component):
        def main(self):
            data = 0
            while 1:
                self.send("hello"*1000, "outbox")
                data += len("hello")*1000
                print "SENT", data
                yield 1

    Pipeline(
        BigPackets(),
        MaxSizePacketiser(1000),
        packetSizeChecker(1000),
    ).run()
