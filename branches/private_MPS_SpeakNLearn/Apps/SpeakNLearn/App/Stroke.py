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
