#!/usr/bin/python
#
# This code is designed soley for the purposes of demonstrating the tools
# for timeshifting.
#

from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.File.UnixPipe import Pipethrough

pipeline(
   DVB_Multiplex(754, [640, 641]), # BBC NEWS 24
   Pipethrough("mencoder -o current.200.avi -ovc lavc -oac lavc -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128 -vf scale=320:-2 -")
   #SimpleFileWriter("BBC_NEWS_24.ts")
).run()
