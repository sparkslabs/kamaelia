#!/usr/bin/env python

# single character handwriting recognition

# character set similar to that used by graffiti 2 - many characters are
# single stroke; normal letter shapes. Some are multi stroke.
# 
# in this, the diagnostic output is the interpretation of the single stroke only
# grammar rules are post-applied to generate multi-stroke characters (by sending
# a backspace to undo the previous character, and writing a new one instead)


import sys
sys.path.append("../Sketcher")

from Whiteboard.Canvas import Canvas
import pygame

from Pen import *
from PreProcessing import *
from Analyser import *
from Grammar import *

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
    
