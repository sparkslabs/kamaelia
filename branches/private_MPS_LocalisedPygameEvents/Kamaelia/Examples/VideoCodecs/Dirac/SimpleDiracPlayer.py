#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay

import sys
if len(sys.argv) != 2:
    sys.stderr.write("Usage:\n   "+sys.argv[0]+" <dirac-file>\n\n")
    sys.exit(1)

file = sys.argv[1]
framerate = 15

Pipeline(
         ReadFileAdaptor(file, readmode="bitrate",
                         bitrate = 300000*8/5),
         DiracDecoder(),
         MessageRateLimit(framerate),
         VideoOverlay(),
).run()
