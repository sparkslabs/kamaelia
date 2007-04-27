#!/usr/bin/python
#
# Mix Client. Passes received data onto stdout. Allows piping into a streaming server.
#
# IMPORTANT:
# If the mix client is not receiving any audio data, it MUST send zero data to cover the gap.
# This must be at a datarate of 44100Hz, 2 byte samples, 2 stereo samples. 
#
# Ie:
#   44100 Hz
#  *    2 2 channel (stereo)
#  *    2 2 bytes per word (16 bit audio)
#  *    8 Bytes -> bits
#  ie 1411200b/s
#  ie 1.3Mbit/s
#

import traceback
import Axon

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient

import sys
if len(sys.argv) > 4:
    mockserverport = int(sys.argv[2])
else:
    mockserverport = 1700


class printer(Axon.Component.component):
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                sys.stdout.write(data)
                sys.stdout.flush()
            yield 1

def dumping_client():
    return pipeline(
        TCPClient("132.185.131.178", 1700),
        printer(),   
    )

dumping_client().run()