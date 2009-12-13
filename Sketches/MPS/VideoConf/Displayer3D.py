#!/usr/bin/python

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoSurface import VideoSurface
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved

from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.OpenGL.Movement import SimpleRotator
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper

import sys
framerate = 10

# override pygame display service
ogl_display = OpenGLDisplay.getDisplayService()
PygameDisplay.setDisplayService(ogl_display[0])
from Kamaelia.UI.OpenGL.MatchedTranslationInteractor import MatchedTranslationInteractor

def player(*argv, **argd):
    screen = VideoSurface()
    screen_in_scene = PygameWrapper(wrap=screen, position=(0, 0,-8), rotation=(-30,15,3)).activate()

    i1 = MatchedTranslationInteractor(target=screen_in_scene).activate()

#    rotator = SimpleRotator(amount=(0.0,0.0,0.5)).activate()
#    rotator.link((rotator,"outbox"), (screen__in_scene,"rel_rotation"))
    return Pipeline(
               DiracDecoder(),
               ToRGB_interleaved(),
               screen,
           )

ServerCore(protocol=player, port=1500).run()
