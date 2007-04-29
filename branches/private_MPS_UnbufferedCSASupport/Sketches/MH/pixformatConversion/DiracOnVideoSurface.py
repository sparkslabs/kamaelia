#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from VideoSurface import VideoSurface
from PixFormatConversion import ToRGB_interleaved

file = "../../../Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.dirac.drc"
framerate = 1

Pipeline(
         ReadFileAdaptor(file, readmode="bitrate",
                         bitrate = 300000*8/5),
         DiracDecoder(),
         ToRGB_interleaved(),
         MessageRateLimit(framerate, buffer=15),
         VideoSurface()
).run()
