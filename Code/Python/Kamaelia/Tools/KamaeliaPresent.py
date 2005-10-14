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

import os
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "."

GraphsFile = os.path.join(basepath, "Graphs.xml")
path = os.path.join(basepath, "Slides")
extn = ".png"

files = os.listdir(path)
files = [ os.path.join(path,fname) for fname in files if fname[-len(extn):]==extn ]
files.sort()

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
                    for level in xrange(self.start, self.stop, self.step):
                        self.send(level, "outbox")
                        yield 1
                    self.start, self.stop, self.step = self.stop, self.start, -self.step
            else:
                self.pause()
                yield 1


Graphline(
     MOUSECLICKS = Multiclick(caption="", position=(50,50), transparent=True,
                              msgs = [ "", "", "PREV", "NEXT", "PREV","NEXT" ],
                              size=(700,500)),
     IMAGELIST = Chooser(items = files),
     KEYS = KeyEvent(outboxes = { "fadesignal" : "Normal place for message",
                                  "graphfadesignal" : "Normal place for message",
                                  "graphcontrol" : "Sends a 'next' message to the slide control",
                                },
                     key_events = {103: ("TOGGLE", "fadesignal"),  # Toggle Fade
                                   104: ("TOGGLE", "graphfadesignal"),  # Toggle Fade
                                   281: ("NEXT", "graphcontrol"),  # Advance "graph slides"
                                  }),
     DISPLAYFADER = BounceRange(255,0, -10), # Initially we want to fade
     GRAPHFADER = BounceRange(255,0, -10), # Initially we want to fade
     DISPLAY = Image(size=(800,600), position=(0,0)),
     GRAPHSLIDES = pipeline(
         onDemandGraphFileParser_Prefab(GraphsFile),
         chunks_to_lines(),
         lines_to_tokenlists(),
     ),
     GRAPHVIEWER = TopologyViewerComponent(transparency = (255,255,255), showGrid = False, position=(0,0)),     
     linkages = {
         ("MOUSECLICKS","outbox"): ("IMAGELIST","inbox"),
         ("MOUSECLICKS","signal"): ("IMAGELIST","control"),
         
         ("KEYS", "fadesignal") : ("DISPLAYFADER", "inbox"),
         ("KEYS", "graphfadesignal") : ("GRAPHFADER", "inbox"),
         ("KEYS", "graphcontrol") : ("GRAPHSLIDES", "inbox"),
         
         ("DISPLAYFADER", "outbox") : ("DISPLAY", "alphacontrol"),
         ("GRAPHFADER", "outbox") : ("GRAPHVIEWER", "alphacontrol"),
         
         ("IMAGELIST","outbox"): ("DISPLAY","inbox"),
         ("IMAGELIST","signal"): ("DISPLAY","control"),
         
         ("GRAPHSLIDES","outbox"): ("GRAPHVIEWER","inbox"),
         ("GRAPHSLIDES","signal"): ("GRAPHVIEWER","control"),
     }
).run()













