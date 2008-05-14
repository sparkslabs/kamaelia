#!/usr/bin/env python
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

#
# Acceptance test of classes in this directory
#
"""Test the drag handler and PyGameApp class
"""

import pygame
from pygame.locals import *

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
            self.app.addHandler(MOUSEBUTTONDOWN, lambda event : CircleDragHandler.handle(event, self.app, self))

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
