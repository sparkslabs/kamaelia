#!/usr/bin/env python
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

# single character handwriting recognition

# character set similar to that used by graffiti 2 - many characters are
# single stroke; normal letter shapes. Some are multi stroke.
# 
# in this, the diagnostic output is the interpretation of the single stroke only
# grammar rules are post-applied to generate multi-stroke characters (by sending
# a backspace to undo the previous character, and writing a new one instead)


import sys
sys.path.append("../Sketcher")

from Kamaelia.Apps.Whiteboard.Canvas import Canvas
import pygame

from .Pen import Pen
from .PreProcessing import QuantiseStroke, Normalise
from .Analyser import Analyse
from .Grammar import StrokeGrammar

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline

def StrokeRecogniser():
    return Graphline( QUANTISE  = QuantiseStroke(),
                      NORMALISE = Normalise(),
                      ANALYSE   = Analyse(),
                      GRAMMAR   = StrokeGrammar(),
                      linkages = {
                          ("self",      "inbox" ) : ("QUANTISE",  "inbox"),
                          ("QUANTISE",  "outbox") : ("NORMALISE", "inbox"),
                          ("NORMALISE", "outbox") : ("ANALYSE",   "inbox"),
                          ("ANALYSE",   "outbox") : ("GRAMMAR",   "inbox"),
                          ("GRAMMAR",   "outbox") : ("self",      "outbox"),
                          
                          ("QUANTISE","drawing")  : ("self", "drawing"),
                          ("ANALYSE", "drawing")  : ("self", "drawing"),
                        }
                    )



if __name__ == "__main__":

    from Kamaelia.UI.Pygame.Display import PygameDisplay
    from Kamaelia.Util.Console import ConsoleEchoer

    width = 1024
    height = 384

    pgd = PygameDisplay( width=width, height=height ).activate()
    PygameDisplay.setDisplayService(pgd)
    
    Graphline( CANVAS  = Canvas( position=(0,0),size=(width,height) ),
               PEN     = Pen(),
               STROKER = StrokeRecogniser(),
               OUTPUT  = ConsoleEchoer(),
        
               linkages = {
                   ("CANVAS",  "eventsOut") : ("PEN", "inbox"),
                   ("PEN", "outbox")        : ("CANVAS", "inbox"),
                   ("PEN", "points")        : ("STROKER", "inbox"),
                   ("STROKER", "outbox")    : ("OUTPUT", "inbox"),
                   ("STROKER", "drawing")   : ("CANVAS", "inbox"),
                   },
            ).run()
    
