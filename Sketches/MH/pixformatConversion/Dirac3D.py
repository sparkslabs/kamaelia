#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from VideoSurface import VideoSurface, YUVtoRGB

from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper

file = "../../../Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.dirac.drc"
framerate = 15

# override pygame display service
ogl_display = OpenGLDisplay.getDisplayService()
PygameDisplay.setDisplayService(ogl_display[0])

screen = VideoSurface()
screen__in_scene = PygameWrapper(wrap=screen, position=(0, 0,-5), rotation=(-30,15,3)).activate()

Pipeline(
         ReadFileAdaptor(file, readmode="bitrate",
                         bitrate = 300000*8/5),
         DiracDecoder(),
         YUVtoRGB(),
         MessageRateLimit(framerate, buffer=15),
         screen
).run()
