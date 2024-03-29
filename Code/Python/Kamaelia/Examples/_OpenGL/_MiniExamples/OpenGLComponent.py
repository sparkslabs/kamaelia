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

import Axon
import pygame
from OpenGL.GL import glBegin, glEnd, GL_QUADS, glColor, glVertex, glColor, glTranslate
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
