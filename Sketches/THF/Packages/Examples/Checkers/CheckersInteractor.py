#!/usr/bin/env python
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
"""\
=====================
Checkers Interactor
=====================
"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.Intersect import *
from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.Interactor import Interactor
from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.Vector import Vector

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
