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
TODO
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Display3D import Display3D
from Util3D import *
from Object3D import *

class SimpleCube(Object3D):

    def __init__(self, **argd):
        super(SimpleCube, self).__init__(**argd)
        self.grabbed = False
        
    def setup(self):
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])

    def draw(self):
        # draw faces 
        glBegin(GL_QUADS)
        glColor4f(1.0,0.75,0.75,0.5)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)

        glColor4f(0.75,1.0,0.75, 0.5)
        glVertex3f(1.0,1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)
        
        glColor4f(0.75,0.75,1.0, 0.5)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor4f(1.0,0.75,1.0, 0.5)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)

        glColor4f(0.75,1.0,1.0, 0.5)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor4f(1.0,1.0,0.75, 0.5)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glEnd()
    
    
    def handleEvents(self):
        pass
        #while self.dataReady("inbox"):
            #event = self.recv("inbox")
            #if event.type == pygame.MOUSEBUTTONDOWN and self.ogl_name in event.hitobjects:
                #if event.button in [1,3]:
                    #self.grabbed = event.button
                #if event.button == 4:
                    #self.pos.z -= 1
                #if event.button == 5:
                    #self.pos.z += 1
            #if event.type == pygame.MOUSEBUTTONUP:
                #if event.button in [1,3]:
                    #self.grabbed = 0
            #if event.type == pygame.MOUSEMOTION:
                #if self.grabbed == 1:
                    #self.rot.y += float(event.rel[0])
                    #self.rot.x += float(event.rel[1])
                    #self.rot %= 360
                #if self.grabbed == 3:
                    #self.pos.x += float(event.rel[0])/10.0
                    #self.pos.y -= float(event.rel[1])/10.0
                        


if __name__=='__main__':
    class Bunch: pass
        
    class CubeRotator(Axon.Component.component):
        def main(self):
            while 1:
                yield 1
                self.send( (0.1, 0.1, 0.1), "outbox")

    
    from Kamaelia.Util.Graphline import Graphline
    
    CUBEC = SimpleCube(pos=Vector(0, 0,-12), name="Center cube").activate()
    CUBER = SimpleCube(pos=Vector(4,0,-22), name="Right cube").activate()
    CUBEB = SimpleCube(pos=Vector(0,-4,-18), name="Bottom cube").activate()
    ROTATOR = CubeRotator().activate()
    
    ROTATOR.link((ROTATOR, "outbox"), (CUBEC, "rel_rotation"))
        
    Axon.Scheduler.scheduler.run.runThreads()  
