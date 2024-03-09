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
import sys
import pygame
import Axon

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Multiclick import Multiclick
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Util.Chooser import Chooser
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent

# We should start thinking about how we handle the lines below better:

from Kamaelia.Apps.Show.GraphSlides import onDemandGraphFileParser_Prefab

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "WhatIsShow.show"

GraphsFile = os.path.join(basepath, "Graphs.xml")
path = os.path.join(basepath, "Slides")
path_extra = os.path.join(basepath, "SecondarySlides")
extn = ".png"


def getSlideList(path, extn):
    files = os.listdir(path)
    files = [ os.path.join(path,fname) for fname in files if fname[-len(extn):]==extn ]
    files.sort()
    return files

PrimarySlides = getSlideList(path, extn)
SecondarySlides  = getSlideList(path_extra, extn)

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
                    for level in range(self.start, self.stop, self.step):
                        self.send(level, "outbox")
                        last = level
                        yield 1
                    if last != self.stop: # range can finish before reaching the end of the range.
                       self.send(self.stop, "outbox")
                       yield 1
                    self.start, self.stop, self.step = self.stop, self.start, -self.step
            else:
                self.pause()
                yield 1

print """
Kamaelia: Show - Controls
=========================

General:
    Fullscreen: f
    Quit : q

Primary Slides:
    next slide  : <right click>, spacebar
    prev slide  : <middle click>, backspace
    Fade in/out : g

Secondary Slides:
    next slide  : return
    Fade in/out : j

Graph Slides:
    next slide  : page down
    drag blobs  : left click
    Fade in/out : h

"""

Graphline(
     KEYS = KeyEvent(outboxes = { "primaryslidefadesignal" : "Normal place for message",
                                  "graphfadesignal" : "Normal place for message",
                                  "secondaryslidefadesignal" : "Normal place for message",
                                  "graphcontrol" : "Sends a 'next' message to the slide control",
                                  "primaryslidecontrol" : "Keyboard control",
                                  "secondaryslidecontrol" : "Keyboard control",
                                },

                     key_events = {
                                   pygame.K_g: ("TOGGLE", "primaryslidefadesignal"),  # Toggle Fade
                                   pygame.K_h: ("TOGGLE", "graphfadesignal"),  # Toggle Fade
                                   pygame.K_j: ("TOGGLE", "secondaryslidefadesignal"),  # Toggle Fade
                                   pygame.K_PAGEDOWN: ("NEXT", "graphcontrol"),  # Advance "graph slides"
                                   pygame.K_RETURN: ("NEXT", "secondaryslidecontrol"),  # Advance slides
                                   pygame.K_SPACE: ("NEXT", "primaryslidecontrol"),  # Advance slides
                                   pygame.K_BACKSPACE: ("PREV", "slidecontrol"),  # Advance slides
                                  }),
     MOUSECLICKS = Multiclick(caption="", position=(50,50), transparent=True,
                              msgs = [ "", "", "PREV", "NEXT", "PREV","NEXT" ],
                              size=(700,500)),

     PRIMARYSLIDES = Chooser(items = PrimarySlides),
     PRIMARYDISPLAYFADER = BounceRange(255,0, -10), # Initially we want to fade
     PRIMARYDISPLAY = Image(size=(800,600), 
                     position=(0,0),
                     displayExtra={ "transparency" : (255,255,255) },
                    ),

     SECONDARYSLIDES = Chooser(items = SecondarySlides),
     SECONDARYDISPLAYFADER = BounceRange(255,0, -10), # Initially we want to fade
     SECONDARYDISPLAY = Image(size=(800,600), 
                     position=(0,0),
                     displayExtra={ "transparency" : (255,255,255) },
                    ),

     GRAPHSLIDES = Pipeline(
         onDemandGraphFileParser_Prefab(GraphsFile),
         chunks_to_lines(),
         lines_to_tokenlists(),
     ),
     GRAPHFADER = BounceRange(255,0, -10), # Initially we want to fade
     GRAPHVIEWER = TopologyViewer(transparency = (255,255,255), showGrid = False, position=(0,0)),

     linkages = {
         ("MOUSECLICKS","outbox"): ("PRIMARYSLIDES","inbox"),
         ("MOUSECLICKS","signal"): ("PRIMARYSLIDES","control"),
         ("KEYS", "primaryslidecontrol"): ("PRIMARYSLIDES","inbox"),
         ("KEYS", "secondaryslidecontrol"): ("SECONDARYSLIDES","inbox"),

         ("KEYS", "primaryslidefadesignal") : ("PRIMARYDISPLAYFADER", "inbox"),
         ("KEYS", "secondaryslidefadesignal") : ("SECONDARYDISPLAYFADER", "inbox"),
         ("KEYS", "graphfadesignal") : ("GRAPHFADER", "inbox"),
         ("KEYS", "graphcontrol") : ("GRAPHSLIDES", "inbox"),

         ("SECONDARYDISPLAYFADER", "outbox") : ("SECONDARYDISPLAY", "alphacontrol"),
         ("PRIMARYDISPLAYFADER", "outbox") : ("PRIMARYDISPLAY", "alphacontrol"),
         ("GRAPHFADER", "outbox") : ("GRAPHVIEWER", "alphacontrol"),

         ("SECONDARYSLIDES","outbox"): ("SECONDARYDISPLAY","inbox"),
         ("SECONDARYSLIDES","signal"): ("SECONDARYDISPLAY","control"),

         ("PRIMARYSLIDES","outbox"): ("PRIMARYDISPLAY","inbox"),
         ("PRIMARYSLIDES","signal"): ("PRIMARYDISPLAY","control"),

         ("GRAPHSLIDES","outbox"): ("GRAPHVIEWER","inbox"),
         ("GRAPHSLIDES","signal"): ("GRAPHVIEWER","control"),
     }
).run()
