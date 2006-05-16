#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Demuxer,DVB_Multiplex
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.UnixPipe import Pipethrough
import Axon
import struct
import dvb3

class ChannelTranscoder(Axon.Component.component):
    def main(self):
        transcoder = Pipethrough("mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -").activate()
        self.link((self, "outbox"), (transcoder, "inbox"))
        while 1:
            yield 1
            while self.dataReady("inbox"):
                packet = self.recv("inbox")
                pid = struct.unpack(">H", packet[1: 3])[0] & 0x1fff
                if pid != 18:
                    self.send( packet, "outbox")
                yield 1
            else:
                self.pause()

location = "london"

if location == "london":
    freq = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
else: # manchester
    freq = 754
    feparams = {}


Graphline(
    SOURCE=DVB_Multiplex(freq, [600, 601,18], feparams), # BBC ONE + EIT data
    DEMUX=DVB_Demuxer({
        "600": ["BBCONE"],
        "601": ["BBCONE"],
        "18": ["BBCONE"],
    }),
    BBCONE = Pipethrough("mencoder -o current.200.avi -ovc lavc -oac mp3lame -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -"),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),

    }
).run()



#
# mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -
# mencoder -o current.512.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=512:abitrate=128 -vf scale=640:-2 -
#

