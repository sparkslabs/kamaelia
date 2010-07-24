#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    return Pipeline(
               DiracDecoder(),
               ToRGB_interleaved(),
               screen,
           )

from Play import AlsaPlayer

def audioplayer(*argv, **argd):
    return AlsaPlayer()

#ServerCore(protocol=audioplayer, port=1501).activate()
ServerCore(protocol=player, port=1500).run()
