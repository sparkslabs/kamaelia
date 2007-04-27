#!/usr/bin/python

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay

file = "snowboard-jum-352x288x75.dirac.drc"
framerate = 15

pipeline(
         ReadFileAdaptor(file, readmode="bitrate",
                         bitrate = 300000*8/5),
         DiracDecoder(),
         MessageRateLimit(framerate),
         VideoOverlay(),
).run()
