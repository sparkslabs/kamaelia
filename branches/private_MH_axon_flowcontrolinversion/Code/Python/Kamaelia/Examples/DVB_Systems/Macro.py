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

Graphline(
    SOURCE=DVB_Multiplex(754, [600, 601,18]), # BBC ONE + EIT data
    DEMUX=DVB_Demuxer({
        "600": ["BBCONE"],
        "601": ["BBCONE"],
        "18": ["BBCONE"],
    }),
    BBCONE = Pipethrough("mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -"),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),

    }
).run()



#
# mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -
# mencoder -o current.512.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=512:abitrate=128 -vf scale=640:-2 -
#

