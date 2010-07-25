#!/usr/bin/python
# -*- coding: utf-8 -*-
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

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((300,300),OPENGL|DOUBLEBUF)
    pygame.display.set_caption('Simple cube')

    # background
    glClearColor(0.0,0.0,0.0,0.0)
    # enable depth tests
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)

    # projection matrix
    glMatrixMode(GL_PROJECTION)             
    glLoadIdentity()                        
    gluPerspective(45.0, float(300)/float(300), 0.1, 100.0)
    # model matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()                        

    pygame.display.flip()

    angle=0

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        # clear screen
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        angle+=0.1

        # translation and rotation
        glPushMatrix()
        glTranslate(0.0,0.0,-15.0)
        glRotate(angle, 1.0,1.0,1.0)

        # draw faces 
        glBegin(GL_QUADS)
        glColor3f(1.0,0.0,0.0)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)

        glColor3f(0.0,1.0,0.0)
        glVertex3f(1.0,1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)
        
        glColor3f(0.0,0.0,1.0)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor3f(1.0,0.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)

        glColor3f(0.0,1.0,1.0)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor3f(1.0,1.0,0.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glEnd()

        glPopMatrix()
        glFlush()

        pygame.display.flip()


if __name__=='__main__': main()
