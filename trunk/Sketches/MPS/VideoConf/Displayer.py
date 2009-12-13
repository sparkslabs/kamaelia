#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoSurface import VideoSurface
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved

import sys
framerate = 10

def player(*argv, **argd):
    return Pipeline(
               DiracDecoder(),
               ToRGB_interleaved(),
               VideoSurface(),
           )

ServerCore(protocol=player, port=1500).run()
