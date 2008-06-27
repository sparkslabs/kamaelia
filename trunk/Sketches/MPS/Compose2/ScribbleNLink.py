#!/usr/bin/python

import random
import Axon

from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline

from Kamaelia.File.UnixProcess import UnixProcess

from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader

from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Apps.SpeakNLearn.Gestures.StrokeRecogniser import StrokeRecogniser
from Kamaelia.Apps.SpeakNLearn.Gestures.Pen import Pen

from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiser, text_to_token_lists

pgd = PygameDisplay( width=1024, height=500 ).activate()
PygameDisplay.setDisplayService(pgd)

Backplane("STROKES").activate()
Backplane("CONSOLE").activate()
Backplane("AXONVIS").activate()
Backplane("AXONEVENTS").activate()
bgcolour = (255,255,180)

node_add_template = \
"""ADD NODE %(nodeid)s non_config randompos component
ADD NODE %(nodeid)s.o.outbox "outbox" randompos outbox
ADD NODE %(nodeid)s.o.signal "signal" randompos outbox
ADD NODE %(nodeid)s.i.inbox "inbox" randompos inbox
ADD NODE %(nodeid)s.i.control "control" randompos inbox
ADD LINK %(nodeid)s %(nodeid)s.o.outbox
ADD LINK %(nodeid)s %(nodeid)s.o.signal
ADD LINK %(nodeid)s %(nodeid)s.i.inbox
ADD LINK %(nodeid)s %(nodeid)s.i.control
"""

class NodeAdder(Axon.Component.component):
    def main(self):
        nodeid = 0
        while True:
            for message in self.Inbox("inbox"):
                if message in [ "o", "u" ]:
                     thisid = str(nodeid)
                     nodeid = nodeid +1
                     nodedef = node_add_template % { "nodeid": thisid }
                     self.send(nodedef, "outbox")
                else:
                   print repr(message)
                if message == "\n":
                     nodeid = nodeid -1
                     thisid = str(nodeid)
                     self.send("DEL NODE %s\n" % thisid, "outbox")
                     self.send("DEL NODE %s.i.inbox\n" % thisid, "outbox")
                     self.send("DEL NODE %s.i.control\n" % thisid, "outbox")
                     self.send("DEL NODE %s.o.outbox\n" % thisid, "outbox")
                     self.send("DEL NODE %s.o.signal\n" % thisid, "outbox")
            yield 1

Pipeline(
         ConsoleReader(),
         PublishTo("AXONVIS"),
).activate()

Pipeline(
         SubscribeTo("AXONVIS"),
         text_to_token_lists(),
         AxonVisualiser(caption="Axon / Kamaelia Visualiser",screensize=(1024,500), position=(0,0), transparency=(255,255,255)),
         PublishTo("AXONEVENTS"),
).activate()

Pipeline(
     SubscribeTo("STROKES"),
     NodeAdder(),
     PublishTo("AXONVIS"),
).activate()

Pipeline(
     SubscribeTo("AXONEVENTS"), PublishTo("CONSOLE"),
).activate()

Pipeline(
     SubscribeTo("STROKES"), PublishTo("CONSOLE"),
).activate()

Pipeline(
         SubscribeTo("CONSOLE"),
         ConsoleEchoer(),
).activate()

Graphline(
           CANVAS  = Canvas( position=(0,0),
                             size=(1024,500),
                             bgcolour = bgcolour,
                           ),
           PEN     = Pen(bgcolour = bgcolour),
           STROKER = StrokeRecogniser(),
           OUTPUT  = PublishTo("STROKES"),
           linkages = {
               ("CANVAS",  "eventsOut") : ("PEN", "inbox"),
               ("PEN", "outbox")        : ("CANVAS", "inbox"),
               ("PEN", "points")        : ("STROKER", "inbox"),
               ("STROKER", "outbox")    : ("OUTPUT", "inbox"),
               ("STROKER", "drawing")   : ("CANVAS", "inbox"),
               ("STROKER", "outbox")    : ("OUTPUT", "inbox"),
               },
        ).run()
        
