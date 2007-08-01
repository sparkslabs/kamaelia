#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from VideoSurface import VideoSurface
from PixFormatConversion import ToRGB_interleaved

from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper
from Kamaelia.UI.OpenGL.SkyGrassBackground import SkyGrassBackground
from Kamaelia.UI.OpenGL.Movement import SimpleRotator

file = "../../../Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.dirac.drc"
framerate = 15

# override pygame display service
ogl_display = OpenGLDisplay.getDisplayService()
PygameDisplay.setDisplayService(ogl_display[0])

SkyGrassBackground(size=(5000,5000,0), position=(0,0,-100)).activate()
screen = VideoSurface()
screen__in_scene = PygameWrapper(wrap=screen, position=(0, 0,-5), rotation=(-30,15,3)).activate()
rotator = SimpleRotator(amount=(0.0,0.0,0.5)).activate()
rotator.link((rotator,"outbox"), (screen__in_scene,"rel_rotation"))

Pipeline(
         ReadFileAdaptor(file, readmode="bitrate",
                         bitrate = 300000*8/5),
         DiracDecoder(),
         ToRGB_interleaved(),
         MessageRateLimit(framerate, buffer=15),
         screen
).run()
