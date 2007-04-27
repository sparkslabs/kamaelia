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
Checkers Piece
=====================
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.OpenGLComponent import *


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
    
    from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.LiftTranslationInteractor import LiftTranslationInteractor
    from CheckersBoard import *
    from CheckersInteractor import *
    
    display = OpenGLDisplay(viewerposition=(0,-10,0), lookat=(0,0,-15)).activate()
    OpenGLDisplay.setDisplayService(display)

    o1 = CheckersPiece(position=(0,0,-15)).activate()
    i1 = CheckersInteractor(victim=o1, liftheight=0.2).activate()
    board = CheckersBoard(position=(0,0,-15)).activate()

    o1.link( (o1, "position"), (i1, "position"))
    i1.link( (i1, "outbox"), (o1, "rel_position"))

    Axon.Scheduler.scheduler.run.runThreads()
# Licensed to the BBC under a Contributor Agreement: THF
