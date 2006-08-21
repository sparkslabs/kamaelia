#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting. For more than one channel the DVB_Demuxer doesn't seem
# to be realtime.
#

from Kamaelia.Device.DVB.Core import DVB_Demuxer
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter

Graphline(
    SOURCE=ReadFileAdaptor("BBC_MUX_1.ts"),
    DEMUX=DVB_Demuxer({
        640: ["NEWS24"],
        641: ["NEWS24"],
        600: ["BBCONE"],
        601: ["BBCONE"],
        610: ["BBCTWO"],
        611: ["BBCTWO"],
        620: ["CBBC"],
        621: ["CBBC"],
        18:  ["NEWS24", "BBCONE"],# "BBCTWO", "CBBC"],
    }),
    NEWS24=SimpleFileWriter("news24.data"),
    BBCONE=SimpleFileWriter("bbcone.data"),
    BBCTWO=SimpleFileWriter("bbctwo.data"),
    CBBC=SimpleFileWriter("cbbc.data"),
    linkages={
       ("SOURCE", "outbox"):("DEMUX","inbox"),
       ("DEMUX", "NEWS24"): ("NEWS24", "inbox"),
       ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),
       ("DEMUX", "BBCTWO"): ("BBCTWO", "inbox"),
       ("DEMUX", "CBBC"): ("CBBC", "inbox"),
    }
).run()

# RELEASE: MH, MPS
