#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.File.Writing import SimpleFileWriter

pipeline(
   DVB_Multiplex(754, [640, 641, 620, 621, 622, 610, 611, 612, 600, 601, 602, 18]), # BBC Multiplex
   SimpleFileWriter("BBC_MUX_1.ts"),
).run()
