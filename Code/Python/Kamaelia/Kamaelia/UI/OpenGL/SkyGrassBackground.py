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
======================
Sky & Grass background
======================

A very simple component showing a plane with the upper half coloured light blue and the lower half green. Can be used for a background.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.


Example Usage
-------------
Only a background::

    SkyGrassBackground(size=(5000,5000,0), position=(0,0,-100)).activate()
    Axon.Scheduler.scheduler.run.runThreads()

"""


import Axon
import pygame
from OpenGL.GL import GL_QUADS, glBegin, glColor4f, glVertex3f, glEnd

from .OpenGLComponent import OpenGLComponent

class SkyGrassBackground(OpenGLComponent):
    """\
    SkyGrassBackground(...) -> A new SkyGrassBackground component.
    
    A very simple component showing a plane with the upper half coloured
    light blue and the lower half green. Can be used for a background.
    """
        
    def setup(self):
        self.w = self.size.x/2.0
        self.h = self.size.y/2.0

    def draw(self):
        glBegin(GL_QUADS)
        glColor4f(0.85, 0.85, 1.0, 1.0)
        glVertex3f(-self.w, self.h, 0)
        glVertex3f(self.w, self.h, 0)
        glVertex3f(self.w, 0.0, 0)
        glVertex3f(-self.w, 0.0, 0)
        glColor4f(0.75, 1.0, 0.75, 1.0)
        glVertex3f(-self.w, 0.0, 0)
        glVertex3f(self.w, 0.0, 0)
        glVertex3f(self.w, -self.h, -0)
        glVertex3f(-self.w, -self.h, -0)
        glEnd()

__kamaelia_components__ = (SkyGrassBackground,)

if __name__=='__main__':
    SkyGrassBackground(size=(5000,5000,0), position=(0,0,-100)).activate()
    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
