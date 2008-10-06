#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Vector import Vector
from OpenGLComponent import *

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
