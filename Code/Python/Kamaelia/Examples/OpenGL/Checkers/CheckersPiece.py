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
Checkers Piece
=====================
"""


import Axon
import pygame
from OpenGL.GL import glBegin, glEnd, GL_QUADS, glColor, glVertex, glColor, glTranslate
from OpenGL.GLU import gluCylinder, gluDisk

from Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent


class CheckersPiece(OpenGLComponent):

    def __init__(self, **argd):
        super(CheckersPiece, self).__init__(**argd)
        
        self.colour = argd.get("colour", (0,0,0))
        
        
    def setup(self):
        self.quadric = gluNewQuadric()
        
        
    def draw(self):
        glColor(0.2,0.2,0.2)
        gluCylinder(self.quadric,0.4,0.4,0.3,16,1);        
        glColor(*self.colour)
        gluDisk(self.quadric,0,0.4,16,1);
        glTranslate(0,0,0.3)
        glColor(*self.colour)
        gluDisk(self.quadric,0,0.4,16,1);
        
        
if __name__=='__main__':
    
    from Kamaelia.UI.OpenGL.LiftTranslationInteractor import LiftTranslationInteractor
    from CheckersBoard import CheckersBoard
    from CheckersInteractor import CheckersInteractor
    
    display = OpenGLDisplay(viewerposition=(0,-10,0), lookat=(0,0,-15)).activate()
    OpenGLDisplay.setDisplayService(display)

    o1 = CheckersPiece(position=(0,0,-15)).activate()
    i1 = CheckersInteractor(victim=o1, liftheight=0.2).activate()
    board = CheckersBoard(position=(0,0,-15)).activate()

    o1.link( (o1, "position"), (i1, "position"))
    i1.link( (i1, "outbox"), (o1, "rel_position"))

    Axon.Scheduler.scheduler.run.runThreads()
# Licensed to the BBC under a Contributor Agreement: THF
