#!/usr/bin/python
#
# This is a mock server that accepts data sent to it, pretending to be an
# encoding streaming systems
#
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