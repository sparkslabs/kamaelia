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

class NodeAdder(Axon.Component.component):
    Outboxes = {
        "outbox" : "commands to the visualiser",
        "nodemanip" : "commands to something that understands adding nodes",
    }
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
                if message == "x":
                     nodeid = nodeid -1
                     thisid = str(nodeid)
                     self.send("DEL NODE %s\n" % thisid, "outbox")
                     self.send("DEL NODE %s.i.inbox\n" % thisid, "outbox")
                     self.send("DEL NODE %s.i.control\n" % thisid, "outbox")
                     self.send("DEL NODE %s.o.outbox\n" % thisid, "outbox")
                     self.send("DEL NODE %s.o.signal\n" % thisid, "outbox")
                if message == "\\":
                     self.send("makelink", "nodemanip")
            if not self.anyReady():
                self.pause()
            yield 1

class LinkMaker(Axon.Component.component):
    Inboxes = {
        "inbox" : "recieve messages from the DOODLER/NODE ADDER",
        "control" : "not yet used",
        "nodeevents" : "for info from topology",
    }
    def main(self):
        makinglink = False
        last_selected = None
        while True:
            if not self.anyReady():
                self.pause()

            for message in self.Inbox("inbox"):
                if message == "makelink":
                    makinglink = True
                    last_selected = None

            for message in self.Inbox("nodeevents"):
                print "GOTIT", repr(message)
                if message[0] == "SELECT":
                    if message[1] == "NODE":
                        if message[2] != None:
                            if makinglink and last_selected == None:
                                last_selected = message[2]
                                print "LAST SELECTED", last_selected
                            elif makinglink:
                                print "MAKING LINK BETWEEN", last_selected, message[2]
                                self.send("ADD LINK %s %s\n" % (last_selected, message[2]), "outbox")
                                makinglink = False
                                last_selected = None
                            else:
                                print "selecting", message[2]
                                last_selected = message[2]
                        else:
                            print "deselecting", message[2]
                            last_selected = message[2]
            yield 1
        

Graphline(
     STROKES = SubscribeTo("STROKES"),
     DOODLER = NodeAdder(),
     NODEMANIP = LinkMaker(),
     TOVISUALISER = PublishTo("AXONVIS"),
     NODEEVENTS = SubscribeTo("AXONEVENTS"),
     linkages = {
         ("STROKES","outbox"): ("DOODLER","inbox"),
         ("DOODLER","outbox"): ("TOVISUALISER","inbox"),

         ("DOODLER","nodemanip"): ("NODEMANIP","inbox"),
         ("NODEEVENTS","outbox"): ("NODEMANIP","nodeevents"),

         ("NODEMANIP","outbox"): ("TOVISUALISER","inbox"),
     },
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
                             size=(1024,50),
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
        
