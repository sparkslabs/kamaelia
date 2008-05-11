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
Checkers Board
=====================
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Kamaelia.UI.OpenGL.OpenGLComponent import *


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
