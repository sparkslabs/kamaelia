#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Axon

class angleIncrement(Axon.Component.component):
   def main(self):
      angle = 0
      while 1:
         self.send(angle, "outbox")
         angle += 0.1
         if angle > 360:
            angle -= 360
         yield 1

class bounce3D(Axon.Component.component):
   def main(self):
      position = [ 0.0,0.0,-5.0 ]
      dz = 0.01
      while 1:
         if abs(position[2]+10)>5: dz = -dz
         position[2] += dz
         self.send(position, "outbox")
         yield 1

class rotatingCube(Axon.Component.component):
    Inboxes = {
       "inbox": "not used",
       "control": "ignored",
       "angle" : "We expect to recieve messages telling us the angle of rotation",
       "position" : "We expect to receive messages telling us the new position",
    }
    def main(self):
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
        position = (0.0,0.0,-15.0)

        while 1:
            yield 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            
            # clear screen
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            while self.dataReady("angle"):
                # Use a while loop to ensure we clear the inbox to avoid messages piling up.
                angle = self.recv("angle")

            while self.dataReady("position"):
                position = self.recv("position")

            # translation and rotation
            glPushMatrix()
            glTranslate(*position)
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


if __name__=='__main__':
    from Kamaelia.Util.Graphline import Graphline
    Graphline(
       TRANSLATION = bounce3D(),
       ROTATION = angleIncrement(),
       CUBE = rotatingCube(),
       linkages = {
          ("ROTATION", "outbox") : ("CUBE", "angle"),
          ("TRANSLATION", "outbox") : ("CUBE", "position"),
       }
    ).run()
