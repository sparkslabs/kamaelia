#!/usr/bin/env python
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
# -------------------------------------------------------------------------

#
# Acceptance test of classes in this directory
#
"""Test the drag handler and PyGameApp class
"""

import pygame

import sys; sys.path.append("..")
from PyGameApp import PyGameApp
from DragHandler import DragHandler

if __name__=="__main__":

    class CircleDragHandler(DragHandler):
        """Handler for dragging of the circle"""
        
        def __init__(self, event, app, circle):
            self.circle = circle
            super(CircleDragHandler, self).__init__(event, app)
        
        def detect(self, pos, button):
            if (pos[0] - self.circle.x)**2 + (pos[1] - self.circle.y)**2 < (self.circle.radius**2):
                self.tvx = self.circle.vx
                self.tvy = self.circle.vy
                self.circle.vx = 0
                self.circle.vy = 0
                return (self.circle.x, self.circle.y)
            else:
                return False
                
        def drag(self,newx,newy):
            self.circle.x = newx
            self.circle.y = newy
            
        def release(self,newx, newy):
            self.drag(newx, newy)
            self.circle.vx = self.tvx
            self.circle.vy = self.tvy
            


    class CircleObject(object):
        """Simple draggable, moving, circle object"""
    
        def __init__( self, app, position, velocity, radius):
            """Initialise, registering dragging event handler and setting initial position and velocity"""
            self.app = app
            self.app.addHandler(pygame.MOUSEBUTTONDOWN, lambda event : CircleDragHandler.handle(event, self.app, self))

            (self.x,  self.y)  = position
            (self.vx, self.vy) = velocity
            self.radius        = radius
            
        def move(self, cycles=1):
            """Move the circle"""
            while cycles > 0:
                cycles -= 1

                self.x += self.vx
                if self.x > self.app.screen.get_width()-self.radius or self.x < self.radius:
                    self.vx = - self.vx
                    print "Xboing"
                    
                self.y += self.vy
                if self.y > self.app.screen.get_height()-self.radius or self.y < self.radius:
                    self.vy = - self.vy
                    
        def draw(self):
            """Render the circle at its current location"""
            pygame.draw.circle(self.app.screen, (255,128,128), (self.x, self.y), self.radius)
                                

    class SimpleApp1(PyGameApp):
        """Simple test application - makes a small window containing a blob that bounces around.
           You can drag the blob with the mouse
        """
    
        def __init__(self, screensize):
            super(SimpleApp1, self).__init__(screensize)

        def initialiseComponent(self):
            self.circle = CircleObject( self, (100,100), (1,1), 32 )

            
        def mainLoop(self):
            self.screen.fill( (255,255,255) )
            self.circle.draw()
            self.circle.move()
            return 1

    print "A white window should appear containing a red bouncing circle."
    print "You should be able to drag the circle with the mouse."
    print "The circle should not move of its own accord whilst being dragged."
        
    app = SimpleApp1( (800, 600) ).run()

# RELEASE: MH, MPS
