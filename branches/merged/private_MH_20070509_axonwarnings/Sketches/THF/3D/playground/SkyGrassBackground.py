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

from Display3D import Display3D
from Util3D import *
from Object3D import *

class SkyGrassBackground(Object3D):
        
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

if __name__=='__main__':
    pass
