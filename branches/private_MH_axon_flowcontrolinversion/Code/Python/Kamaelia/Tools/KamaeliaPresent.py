#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#

import Axon

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Multiclick import Multiclick
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent import TopologyViewerComponent
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Kamaelia.Data.Experimental import onDemandGraphFileParser_Prefab

import pygame

import os
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "."

GraphsFile = os.path.join(basepath, "Graphs.xml")
path = os.path.join(basepath, "Slides")
path_extra = os.path.join(basepath, "Slides.extra")
extn = ".png"

files = os.listdir(path)
files = [ os.path.join(path,fname) for fname in files if fname[-len(extn):]==extn ]
files.sort()

files2 = os.listdir(path_extra)
files2 = [ os.path.join(path_extra,fname) for fname in files2 if fname[-len(extn):]==extn ]
files2.sort()

class BounceRange(Axon.Component.component):
    def __init__(self, start, stop, step=1):
        super(BounceRange, self).__init__()
        self.start = start
        self.stop = stop
        self.step = step
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                message = self.recv("inbox")
                if message == "TOGGLE":
                    last = None
                    for level in xrange(self.start, self.stop, self.step):
                        self.send(level, "outbox")
                        last = level
                        yield 1
                    if last != self.stop: # GRR at xrange!
                       self.send(self.stop, "outbox")
                       yield 1
                    self.start, self.stop, self.step = self.stop, self.start, -self.step
            else:
                self.pause()
                yield 1

import Axon
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Util.Graphline import Graphline

class LineSplit(Axon.Component.component):
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                lines = data.split("\n")
                for line in lines:
                    self.send(line, "outbox")
                    yield 1

class source(Axon.Component.component):
    def __init__(self,data):
        super(source, self).__init__()
        self.data = data
    def main(self):
        self.send(self.data, "outbox")
        yield 1

silliness = """Play video. Play music. Play a game. Create video. Create games. Do all
the above over the network, and
do it one on one, many to many.
Test protocols on simulated
broken networks. Design the
interface you want, not the GUI,
mix n match all the above.
"""

class NastyHack(Axon.Component.component):
    Outboxes = [
        "tickersignal",
        "image1signal",
        "image2signal",
    ]
    def main(self):
        while not self.dataReady("inbox"):
            self.pause()
            yield 1
        image1 = Image("/home/zathras/Album/KamaeliaSpotting.png", position=(608,160) ).activate()
        tick = Ticker(background_colour=(255,255,255),
                           text_colour=(0,0,0),
                           render_top = 1,
                           render_right = 500,
                           render_bottom = 320,
                           text_height = 39,
                           line_spacing = 7,
                           position = (108, 160),
             )
        Graphline (
             SOURCE = source(silliness),
             LINES = LineSplit(),
             TICK = tick,
             linkages = {
                         ("SOURCE", "outbox"): ("LINES", "inbox"),
                         ("SOURCE", "signal"): ("LINES", "control"),
                         ("LINES", "outbox"): ("TICK", "inbox"),
                         ("LINES", "signal"): ("TICK", "control"),
             }
        ).activate()
        image2 = Image("/home/zathras/Album/ChooseConcurrency.png", position=(115,475) ).activate()
        self.link((self, "tickersignal"), (tick,"control"))
        self.link((self, "image1signal"), (image1,"control"))
        self.link((self, "image2signal"), (image2,"control"))

        while 1:
            yield 1
            if self.dataReady("control"):
                self.send(Axon.Ipc.producerFinished(), "tickersignal")
                self.send(Axon.Ipc.producerFinished(), "image1signal")
                self.send(Axon.Ipc.producerFinished(), "image2signal")
                return


Graphline(

     NASTYHACK = NastyHack().activate(),
     KEYS = KeyEvent(outboxes = { "fadesignal" : "Normal place for message",
                                  "graphfadesignal" : "Normal place for message",
                                  "extrafadesignal" : "Normal place for message",
                                  "graphcontrol" : "Sends a 'next' message to the slide control",
                                  "slidecontrol" : "Keyboard control",
                                  "extraslidecontrol" : "Keyboard control",
                                  "tickeron" : "",
                                  "tickeroff" : "",
                                },
                     key_events = {
                                   103: ("TOGGLE", "fadesignal"),  # Toggle Fade
                                   104: ("TOGGLE", "graphfadesignal"),  # Toggle Fade
                                   106: ("TOGGLE", "extrafadesignal"),  # Toggle Fade
                                   116: ("TICKERON", "tickeron"),  # Toggle Fade
                                   121: ("TICKEROFF", "tickeroff"),  # Toggle Fade
                                   281: ("NEXT", "graphcontrol"),  # Advance "graph slides"
                                   pygame.K_RETURN: ("NEXT", "extraslidecontrol"),  # Advance slides
                                   pygame.K_SPACE: ("NEXT", "slidecontrol"),  # Advance slides
                                   pygame.K_BACKSPACE: ("PREV", "slidecontrol"),  # Advance slides
                                  }),
     MOUSECLICKS = Multiclick(caption="", position=(50,50), transparent=True,
                              msgs = [ "", "", "PREV", "NEXT", "PREV","NEXT" ],
                              size=(700,500)),
     IMAGELIST = Chooser(items = files),
     EXTRAIMAGELIST = Chooser(items = files2),
     DISPLAYFADER = BounceRange(255,0, -10), # Initially we want to fade
     EXTRADISPLAYFADER = BounceRange(255,0, -10), # Initially we want to fade
     GRAPHFADER = BounceRange(255,0, -10), # Initially we want to fade
     DISPLAY = Image(size=(800,600), 
                     position=(0,0),
                     displayExtra={ "transparency" : (255,255,255) },
                    ),
     EXTRADISPLAY = Image(size=(800,600), 
                     position=(0,0),
                     displayExtra={ "transparency" : (255,255,255) },
                    ),
     GRAPHSLIDES = pipeline(
         onDemandGraphFileParser_Prefab(GraphsFile),
         chunks_to_lines(),
         lines_to_tokenlists(),
     ),
     GRAPHVIEWER = TopologyViewerComponent(transparency = (255,255,255), showGrid = False, position=(0,0)),     
     linkages = {
         ("MOUSECLICKS","outbox"): ("IMAGELIST","inbox"),
         ("MOUSECLICKS","signal"): ("IMAGELIST","control"),
         ("KEYS", "slidecontrol"): ("IMAGELIST","inbox"),
         ("KEYS", "extraslidecontrol"): ("EXTRAIMAGELIST","inbox"),

         ("KEYS","tickeron"):("NASTYHACK","inbox"),
         ("KEYS","tickeroff"):("NASTYHACK","control"),
         
         ("KEYS", "fadesignal") : ("DISPLAYFADER", "inbox"),
         ("KEYS", "extrafadesignal") : ("EXTRADISPLAYFADER", "inbox"),
         ("KEYS", "graphfadesignal") : ("GRAPHFADER", "inbox"),
         ("KEYS", "graphcontrol") : ("GRAPHSLIDES", "inbox"),
         
         ("EXTRADISPLAYFADER", "outbox") : ("EXTRADISPLAY", "alphacontrol"),
         ("DISPLAYFADER", "outbox") : ("DISPLAY", "alphacontrol"),
         ("GRAPHFADER", "outbox") : ("GRAPHVIEWER", "alphacontrol"),
         
         ("EXTRAIMAGELIST","outbox"): ("EXTRADISPLAY","inbox"),
         ("EXTRAIMAGELIST","signal"): ("EXTRADISPLAY","control"),

         ("IMAGELIST","outbox"): ("DISPLAY","inbox"),
         ("IMAGELIST","signal"): ("DISPLAY","control"),
         
         ("GRAPHSLIDES","outbox"): ("GRAPHVIEWER","inbox"),
         ("GRAPHSLIDES","signal"): ("GRAPHVIEWER","control"),
     }
).run()













