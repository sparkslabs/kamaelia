#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Demuxer,DVB_Multiplex
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.UnixPipe import Pipethrough

Graphline(
    SOURCE=DVB_Multiplex(754, [600, 601,18]), # BBC ONE + EIT data
    DEMUX=DVB_Demuxer({
        "600": "BBCONE",
        "601": "BBCONE",
        "18": "EIT",
    }),
    BBCONE=Pipethrough("mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -"),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),
    }
).run()
#    BBCONE=SimpleFileWriter("bbcone.data"),
