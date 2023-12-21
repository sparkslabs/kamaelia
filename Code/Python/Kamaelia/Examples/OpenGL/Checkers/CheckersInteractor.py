#!/usr/bin/env python
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
"""\
=====================
Checkers Interactor
=====================
"""


import pygame

import Axon
from Kamaelia.UI.OpenGL.Intersect import Intersect
from Kamaelia.UI.OpenGL.Interactor import Interactor
from Kamaelia.UI.OpenGL.Vector import Vector

class CheckersInteractor(Interactor):
    
    def __init__(self, **argd):
        super(CheckersInteractor, self).__init__(**argd)

        self.addInbox("position")
        self.addOutbox("movement")

        self.liftheight = argd.get("liftheight", 0.2)
        self.colour = argd.get("colour")
                                         
        self.grabbed = False
        self.position = None
        self.oldpoint = None
        self.lastValidPos = None
            
        if self.nolink == False:
            self.link( (self, "movement"), (self.target, "rel_position") )
            self.link( (self.target, "position"), (self, "position") )


    def setup(self):
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])


    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")
            
            if self.position is not None:
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEMOTION and self.grabbed:
                    p1 = self.position.copy()
                    p1.x += 10
                    p2 = self.position.copy()
                    p2.y += 10
                    z = Intersect.ray_Plane(event.viewerposition, event.direction, [self.position, p1, p2])
                    newpoint = event.direction * z
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                    if event.button == 1:
                        self.grabbed = True
                        self.send((0,0,self.liftheight), "movement")
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.grabbed:
                        self.grabbed = False
                        # place piece in the middle of a black field
                        alignedpos = self.position.copy()
                        alignedpos.x = floor(alignedpos.x)+0.5
                        alignedpos.y = floor(alignedpos.y)+0.5

                        diff = alignedpos - self.position
                        self.send((diff.x,diff.y,-self.liftheight), "movement")
                        
                        self.position = alignedpos

                        fr = (floor(self.lastValidPos.x)+4, floor(self.lastValidPos.y)+4)
                        to = (floor(alignedpos.x)+4, floor(alignedpos.y)+4 )
                        self.send( {"PLACEMENT":True, "from":fr, "to":to, "colour":self.colour, "objectid": id(self)}, "outbox")

                if event.type == pygame.MOUSEMOTION:
                    if self.grabbed == True:
                        if self.oldpoint is not None:
                            diff = newpoint-self.oldpoint
                            diff.z = 0
                            self.send(diff.toTuple(), "movement")

                try:
                    self.oldpoint = newpoint
                except NameError: pass            


    def frame(self):
        while self.dataReady("position"):
            self.position = Vector(*self.recv("position"))
            if self.lastValidPos is None:
                self.lastValidPos = self.position.copy()
            
        while self.dataReady("inbox"):
        
            msg = self.recv("inbox")
            if msg == "ACK":
                self.lastValidPos = self.position.copy()
            elif msg == "INVALID":
                diff = self.lastValidPos - self.position
                diff.z = 0
                self.send(diff.toTuple(), "movement")


if __name__=='__main__':
    pass
# Licensed to the BBC under a Contributor Agreement: THF
