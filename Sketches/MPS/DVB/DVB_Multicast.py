#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

import dvb3
from Axon.Component import component
from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.Detuple import SimpleDetupler
from Kamaelia.Protocol.Packetise import MaxSizePacketiser

# from Kamaelia.File.Writing import SimpleFileWriter
# from Kamaelia.File.UnixPipe import Pipethrough

freq = 754.166670
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "coderate_HP" : dvb3.frontend.FEC_3_4,
    "coderate_LP" : dvb3.frontend.FEC_3_4,
}
feparams = {}
service_ids = { "BBC ONE": 4168,
                "BBC TWO": 4232,
                "CBEEBIES":16960,
                "CBBC":4671,
              }

class counter(component):
    def __init__(self, tag):
        super(counter, self).__init__()
        self.tag = tag
    def main(self):
        count = 0
        while 1:
            while self.dataReady("inbox"):
                self.send(self.recv("inbox"), "outbox")
                count = count +1
            print self.tag, ":", count
            self.pause()
            yield 1

import time
class dataRateMeasure(component):
    def main(self):
        size = 0
        c = 0
        t = time.time()
        while 1:
            while self.dataReady("inbox"):
                c += 1
                data = self.recv("inbox")
                size += len(data)
                self.send(data, "outbox")
            if (c % 20) == 0:
                t_dash = time.time()
                if t_dash - t > 1:
                    print int((size/(t_dash - t))*8)
                    t = t_dash
                    size = 0
            yield 1

if 0:
    pipeline(
        DVB_Multiplex(freq, [600,601], feparams),
        SimpleFileWriter("somefile.ts"),
    ).run()

if 0:
    pipeline(
        ReadFileAdaptor("somefile.ts",readsize=8000000),
        MaxSizePacketiser(),
        Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
    ).activate()

    pipeline(
        Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
        SimpleDetupler(1),
        SimpleFileWriter("otherfile.ts"),
    ).run()


if 1:
    pipeline(
        DVB_Multiplex(freq, [600,601], feparams),
        MaxSizePacketiser(),
        Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
    ).run()

if 0:
    pipeline(
        Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
        SimpleDetupler(1),
        dataRateMeasure(),
        SimpleFileWriter("otherfile.ts"),
    ).run()
