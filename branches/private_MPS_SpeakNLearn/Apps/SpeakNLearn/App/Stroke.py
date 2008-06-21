#!/usr/bin/python

from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Apps.SpeakNLearn.Gestures.StrokeRecogniser import StrokeRecogniser

from Kamaelia.Apps.SpeakNLearn.Gestures.Pen import *
from Kamaelia.Apps.SpeakNLearn.Gestures.PreProcessing import *
from Kamaelia.Apps.SpeakNLearn.Gestures.Analyser import *
from Kamaelia.Apps.SpeakNLearn.Gestures.Grammar import *



width = 1024
height = 384

pgd = PygameDisplay( width=width, height=height ).activate()
PygameDisplay.setDisplayService(pgd)

bgcolour = (255,255,180)
Graphline( CANVAS  = Canvas( position=(100,42),
                             size=(824,300),
                             bgcolour = bgcolour,
                           ),
           PEN     = Pen(bgcolour = bgcolour),
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
