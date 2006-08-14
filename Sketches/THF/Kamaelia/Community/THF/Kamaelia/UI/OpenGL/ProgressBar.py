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
Progress Bar
=====================
TODO
"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Util3D import *
from OpenGLComponent import *


class ProgressBar(OpenGLComponent):
    
    def __init__(self, **argd):
        super(ProgressBar, self).__init__(**argd)
        
        # add progress Inbox, used for reception of progress values in the range (0,1)
        self.addInbox("progress")

        # appearance        
        self.edgecolour = argd.get("edgecolour", (0,0,0))
        self.barcolour = argd.get("barcolour", (200,200,244))

        #progress (1.0 is full)
        self.progress = argd.get("progress", 0.0)
                

    def draw(self):
        hs = self.size/2.0

        progw = self.size.x * self.progress
        
        # draw envelope
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_QUADS)
        glColor4f(self.edgecolour[0]/256.0, self.edgecolour[1]/256.0, self.edgecolour[2]/256.0, 0.8)
        # right
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)
        # left
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        # top
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)
        # bottom
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self.progress > 0.0:
            # draw progress
            glEnable(GL_BLEND)
            glDepthMask(GL_FALSE)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glBegin(GL_QUADS)
            glColor4f(self.barcolour[0]/256.0, self.barcolour[1]/256.0, self.barcolour[2]/256.0, 0.5)
            
            # front
            glVertex3f(-hs.x+progw,hs.y,hs.z)
            glVertex3f(-hs.x+progw,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,hs.z)
            glVertex3f(-hs.x,hs.y,hs.z)
            # back
            glVertex3f(-hs.x+progw,hs.y,-hs.z)
            glVertex3f(-hs.x+progw,-hs.y,-hs.z)
            glVertex3f(-hs.x,-hs.y,-hs.z)
            glVertex3f(-hs.x,hs.y,-hs.z)
            # right
            glVertex3f(-hs.x+progw,hs.y,hs.z)
            glVertex3f(-hs.x+progw,-hs.y,hs.z)
            glVertex3f(-hs.x+progw,-hs.y,-hs.z)
            glVertex3f(-hs.x+progw,hs.y,-hs.z)
            # left
            glVertex3f(-hs.x,hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,-hs.z)
            glVertex3f(-hs.x,hs.y,-hs.z)
            # top
            glVertex3f(-hs.x+progw,hs.y,hs.z)
            glVertex3f(-hs.x,hs.y,hs.z)
            glVertex3f(-hs.x,hs.y,-hs.z)
            glVertex3f(-hs.x+progw,hs.y,-hs.z)
            # bottom
            glVertex3f(-hs.x+progw,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,hs.z)
            glVertex3f(-hs.x,-hs.y,-hs.z)
            glVertex3f(-hs.x+progw,-hs.y,-hs.z)
            glEnd()
            glDepthMask(GL_TRUE)
            glEnable(GL_BLEND)

        
    
    def frame(self):
        self.handleProgress()


    def handleProgress(self):
         while self.dataReady("progress"):
            self.progress = self.recv("progress")
            if self.progress < 0.0: self.progress = 0.0
            if self.progress > 1.0: self.progress = 1.0
            self.redraw()
            

from MatchedTranslationInteractor import *

if __name__=='__main__':

    PROGRESS = ProgressBar(size = (3, 0.5, 0.2), position=(0,0,-10), progress=0.5).activate()    
    INT = MatchedTranslationInteractor(victim=PROGRESS).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  
