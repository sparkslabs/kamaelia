#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
#

import os
import time
import Axon


from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.PAR import PAR

from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.UI.Pygame.VideoSurface import VideoSurface

from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved

class timedShutdown(Axon.ThreadedComponent.threadedcomponent):
    TTL = 1
    def main(self):
        time.sleep(self.TTL)
        self.send(Axon.Ipc.shutdownMicroprocess(), "signal")


path = "Slides"
extn = ".gif"
allfiles = os.listdir(path)
files = list()
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))

files.sort()

file = "/data/dirac-video/snowboard-jum-352x288x75.dirac.drc"
framerate = 3

Pipeline(
        timedShutdown(TTL=15),
        PAR(
            Pipeline(
                     ReadFileAdaptor(file, readmode="bitrate",
                                     bitrate = 300000*8/5),
                     DiracDecoder(),
                     MessageRateLimit(framerate),
                     VideoOverlay(position=(260,48), size=(200,300)),
            ),
            Pipeline( ReadFileAdaptor(file, readmode="bitrate", bitrate = 2280960*8),
                      DiracDecoder(),
#                      MessageRateLimit(framerate),
                      ToRGB_interleaved(),
                      VideoSurface(size=(200, 300), position=(600,48)),
            ),
            Pipeline(
                PAR(
                    Button(caption="Next",     msg="NEXT", position=(72,8)),
                    Button(caption="Previous", msg="PREV", position=(8,8)),
                    Button(caption="First",    msg="FIRST" ,position=(256,8)),
                    Button(caption="Last",     msg="LAST", position=(320,8)),
                ),
                Chooser(items = files),
                Image(size=(200,300), position=(8,48), maxpect=(200,300)),
            ),
            Pipeline(
                Textbox(size=(200,300), position=(8,360)),
                TextDisplayer(size=(200,300), position=(228,360)),
            ),
            Ticker(size=(200,300), position=(450,360)),
        ),
).run()
