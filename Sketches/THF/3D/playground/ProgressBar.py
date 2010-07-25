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
Progress Bar
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


class ProgressBar(Object3D):
    
    def __init__(self, **argd):
        super(ProgressBar, self).__init__(**argd)
        
        # add progress Inbox, used for reception of progress values in the range (0,1)
        self.addInbox("progress")

        # appearance        
        self.edgeColour = argd.get("fgcolour", (0,0,0))
        self.barColour = argd.get("barColour", (200,200,244))

        #progress (1.0 is full)
        self.progress = argd.get("progress", 0.0)
        
        print str(self.size)
                

    def draw(self):
        hs = self.size/2.0

        progw = self.size.x * self.progress
        
        # draw progress
        glBegin(GL_QUADS)
        glColor4f(self.barColour[0]/256.0, self.barColour[1]/256.0, self.barColour[2]/256.0, 0.8)
        
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
   
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # draw envelope
        glBegin(GL_QUADS)
        glColor4f(self.edgeColour[0]/256.0, self.edgeColour[1]/256.0, self.edgeColour[2]/256.0, 0.8)
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

        
    
    def frame(self):
        self.handleProgress()


    def handleProgress(self):
         while self.dataReady("progress"):
            self.progress = self.recv("progress")
            if self.progress < 0.0: self.progress = 0.0
            if self.progress > 1.0: self.progress = 1.0
            

from MatchedTranslationInteractor import *

if __name__=='__main__':

    PROGRESS = ProgressBar(size = Vector(3, 0.5, 0.2), pos=Vector(0,0,-10), progress=0.5).activate()    
    INT = MatchedTranslationInteractor(victim=PROGRESS).activate()
    
    PROGRESS.link( (PROGRESS, "position"), (INT, "position"))
    INT.link( (INT, "outbox"), (PROGRESS, "rel_position"))
            
    Axon.Scheduler.scheduler.run.runThreads()  
