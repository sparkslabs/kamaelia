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
Checkers Board
=====================
"""


import Axon
import pygame
from OpenGL.GL import glBegin, glEnd, glColor, glVertex, GL_QUADS

from Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent


class CheckersBoard(OpenGLComponent):

    def draw(self):
        glBegin(GL_QUADS)
        for i in range(8):
            for j in range(8):
                if (i+j) %2 == 0:
                    glColor(0,0,0)
                else:
                    glColor(0.8, 0.8, 0.8)
                x = i-4
                y = j-4
                glVertex(x, y, 0)
                glVertex(x+1, y, 0)
                glVertex(x+1, y+1, 0)
                glVertex(x, y+1, 0)
        glEnd()        
        
if __name__=='__main__':
    
    o1 = CheckersBoard(position=(0,0,-15)).activate()

    Axon.Scheduler.scheduler.run.runThreads()
# Licensed to the BBC under a Contributor Agreement: THF
