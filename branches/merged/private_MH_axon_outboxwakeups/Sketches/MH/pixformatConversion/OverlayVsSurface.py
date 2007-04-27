#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.UI.Pygame.Button import Button
from TwoWaySplitter import TwoWaySplitter

from VideoSurface import VideoSurface, YUVtoRGB

file = "../../../Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.dirac.drc"
framerate = 1

Button(caption="<---overlay", position=(400,10)).activate()
Button(caption="<---surface", position=(400,310)).activate()

Graphline(
         SOURCE = Pipeline( ReadFileAdaptor(file, readmode="bitrate",
                                  bitrate = 300000*8/5),
                   DiracDecoder(),
                   MessageRateLimit(framerate, buffer=15),
                 ),
         SPLIT = TwoWaySplitter(),
         OVERLAY = VideoOverlay(),
         SURFACE = Pipeline(
                  YUVtoRGB(),
                 VideoSurface(position=(0,300))
         ),
         linkages = {
             ("SOURCE","outbox") : ("SPLIT","inbox"),
             ("SPLIT", "outbox") : ("OVERLAY","inbox"),
             ("SPLIT", "outbox2") : ("SURFACE","inbox"),
         }
).run()
