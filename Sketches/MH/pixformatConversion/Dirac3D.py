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
from VideoSurface import VideoSurface
from PixFormatConversion import ToRGB_interleaved

from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper
from Kamaelia.UI.OpenGL.SkyGrassBackground import SkyGrassBackground
from Kamaelia.UI.OpenGL.Movement import SimpleRotator

file = "../../../Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jump-352x288x75.0.5.4.drc"
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
