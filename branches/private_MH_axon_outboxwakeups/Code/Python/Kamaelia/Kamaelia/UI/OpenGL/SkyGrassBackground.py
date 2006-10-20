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
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGLComponent import *

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
