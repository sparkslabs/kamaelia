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
Simple Cube component
=====================
TODO
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Vector import Vector
from OpenGLComponent import *

class SimpleCube(OpenGLComponent):

    def __init__(self, **argd):
        super(SimpleCube, self).__init__(**argd)
        
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
    
    

if __name__=='__main__':
    class Bunch: pass
        
    class CubeRotator(Axon.Component.component):
        def main(self):
            while 1:
                yield 1
                self.send( (0.1, 0.1, 0.1), "outbox")

    
    from Kamaelia.Util.Graphline import Graphline
    
    CUBEC = SimpleCube(position=(0, 0,-12), size=(1,1,1), name="Center cube").activate()
    CUBER = SimpleCube(position=(4,0,-22), size=(1,1,1), name="Right cube").activate()
    CUBEB = SimpleCube(position=(0,-4,-18), size=(1,1,1), name="Bottom cube").activate()
    ROTATOR = CubeRotator().activate()
    
    ROTATOR.link((ROTATOR, "outbox"), (CUBEC, "rel_rotation"))
        
    Axon.Scheduler.scheduler.run.runThreads()  
