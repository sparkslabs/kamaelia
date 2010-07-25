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
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.UI.Pygame.Button import Button
from TwoWaySplitter import TwoWaySplitter

from VideoSurface import VideoSurface
from PixFormatConversion import ToRGB_interleaved

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
                  ToRGB_interleaved(),
                 VideoSurface(position=(0,300))
         ),
         linkages = {
             ("SOURCE","outbox") : ("SPLIT","inbox"),
             ("SPLIT", "outbox") : ("OVERLAY","inbox"),
             ("SPLIT", "outbox2") : ("SURFACE","inbox"),
         }
).run()
