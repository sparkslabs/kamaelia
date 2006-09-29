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

import Axon
import pygame
from OpenGL.GL import *
from Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent
from Kamaelia.UI.OpenGL.Vector import Vector

  
class Point(OpenGLComponent):
    def draw(self):
        glBegin(GL_POINTS)
        glColor(1,0,0)
        glVertex(0,0,0)
        glEnd()

class ChangingColourQuad(OpenGLComponent):
    def setup(self):
        self.colour = (0.5,1.0,0.5)
        self.addInbox("colour")
        self.addListenEvents([pygame.MOUSEBUTTONDOWN])
    
    def draw(self):
        glBegin(GL_QUADS)
        glColor(*self.colour)
        glVertex(-1, 1, 0)
        glVertex(1, 1, 0)
        glVertex(1, -1, 0)
        glVertex(-1, -1, 0)
        glEnd()
        
    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")
            if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                self.rotation += Vector(0,0,10)
                self.rotation %= 360
    
    def frame(self):
        while self.dataReady("colour"):
            self.colour = self.recv("colour")
            self.redraw()

Point(position=(-1,0,-10)).activate()
ChangingColourQuad(position=(1,0,-10)).activate()
Axon.Scheduler.scheduler.run.runThreads()  
  # Licensed to the BBC under a Contributor Agreement: THF
