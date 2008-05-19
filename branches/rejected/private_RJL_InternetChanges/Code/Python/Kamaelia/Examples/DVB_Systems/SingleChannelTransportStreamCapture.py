#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.UnixPipe import Pipethrough

pipeline(
   DVB_Multiplex(754, [640, 641]), # BBC NEWS 24
   SimpleFileWriter("BBC_NEWS_24.ts")
).run()

# RELEASE: MH, MPS
