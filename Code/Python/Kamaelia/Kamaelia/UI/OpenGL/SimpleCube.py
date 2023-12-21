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
Simple Cube component
=====================

A simple cube for the OpenGL display service.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
Three cubes in different positions with various rotation and sizes::

    Graphline(    
        CUBEC = SimpleCube(position=(0, 0,-12), rotation=(40,90,0), size=(1,1,1)).activate(),
        CUBER = SimpleCube(position=(4,0,-22), size=(2,2,2)).activate(),
        CUBEB = SimpleCube(position=(0,-4,-18), rotation=(0,180,20), size=(1,3,2)).activate(),
        linkages = {}
    ).run()

How does it work?
-----------------
SimpleButton is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides draw().

In draw() a simple cube made of 6 quads with different colours is drawn.

"""


import Axon
import pygame
from OpenGL.GL import GL_QUADS, glBegin, glColor4f, glVertex3f, glEnd
from .Vector import Vector
from .OpenGLComponent import OpenGLComponent

class SimpleCube(OpenGLComponent):
    """\
    SimpleCube(...) -> new SimpleCube component.
    
    A simple cube for the OpenGL display service.
    """

    def draw(self):
        hs = self.size/2.0
        # draw faces 
        glBegin(GL_QUADS)
        glColor4f(1.0,0.75,0.75,0.5)
        # right face
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)

        glColor4f(0.75,1.0,0.75, 0.5)
        # left face
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        
        glColor4f(0.75,0.75,1.0, 0.5)
        # top face
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)

        glColor4f(1.0,0.75,1.0, 0.5)
        # bottom face
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)

        glColor4f(0.75,1.0,1.0, 0.5)
        # back face
        glVertex3f(hs.x,hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)

        glColor4f(1.0,1.0,0.75, 0.5)
        # front face
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glEnd()
    
__kamaelia_components__ = (SimpleCube,)    

if __name__=='__main__':
    from Kamaelia.Util.Graphline import Graphline

    Graphline(    
        CUBEC = SimpleCube(position=(0, 0,-12), rotation=(225,45,135), size=(1,1,1)).activate(),
        CUBER = SimpleCube(position=(4,0,-22), size=(2,2,2)).activate(),
        CUBEB = SimpleCube(position=(0,-4,-18), rotation=(0,180,20), size=(1,3,2)).activate(),
        linkages = {}
    ).run()
# Licensed to the BBC under a Contributor Agreement: THF
