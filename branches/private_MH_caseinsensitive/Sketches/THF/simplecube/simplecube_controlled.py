#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import Axon

class cubeController(Axon.Component.component):
   Outboxes = {
       "outbox": "not used",
       "signal": "not used",
       "rotate" : "The current angle is sent",
       "translate" : "The current distance is sent",
    }
    
   def __init__(self):
      super(cubeController,self).__init__()
      self.rotate = False
      self.angle = 0
      self.lastMM = [0,0]
      
   def main(self):
      angle = [0,0]
      position = [0.0, 0.0, -5.0]
      while 1:
         # Events are now fetched directly from pygame
         # later from the framework like in PyGameDisplay
         events = [ event for event in pygame.event.get() ]
         for event in events:
            # ISSUE: sometimes button up/down events are missed
            if event.type == pygame.MOUSEBUTTONDOWN:
               if event.button == 1:
                  self.rotate = True
               elif event.button == 5:
                  position[2] += 1
               elif event.button ==4:
                  position[2] -= 1
            if event.type == pygame.MOUSEBUTTONUP:
               if event.button == 1:
                  self.rotate = False
            if event.type == pygame.MOUSEMOTION:
               pos = event.pos
               if self.rotate:
                  angle[0] += pos[0]-self.lastMM[0]
                  angle[1] += pos[1]-self.lastMM[1]
               self.lastMM = pos
         self.send(angle, "rotate")
         self.send(position, "translate")
         for x in angle: x = x%360
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
        pygame.display.set_caption('Use your mouse!')

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

        angle=[0,0]
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
            glRotate(angle[0], 0.0,1.0,0.0)
            glRotate(angle[1], 1.0,0.0,0.0)

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
    pygame.init()
    Graphline(
       CUBE = rotatingCube(),
       CUBECONTROL = cubeController(),
       linkages = {
          ("CUBECONTROL", "rotate") : ("CUBE", "angle"),
          ("CUBECONTROL", "translate") : ("CUBE", "position"),
       }
    ).run()
