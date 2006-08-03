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
Simple Button component
=====================

A simple cuboid shaped button without caption. Implements responsive button behavoir.

Could be used to inherit differently shaped buttons from. The colours of the front/back and the side faces can be specified.

Example Usage
-------------
    Graphline(
        button1 = SimpleButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
        button2 = SimpleButton(size=(2,2,1), position=(5,0,-15), msg="BRAIN"),
        echo = ConsoleEchoer(),
        linkages = {
            ("button1", "outbox") : ("echo", "inbox"),
            ("button2", "outbox") : ("echo", "inbox")
        }
    ).run()
        

How does it work?
-----------------

SimpleButton is inherited from OpenGLComponent.

It draws a simple cuboid. It is activated on mouse button release over the object
and on key down if a key is assigned. On mouse button down it is shrunk by a small
amount until the button is released.

"""

import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *

from Util3D import *
from OpenGLComponent import OpenGLComponent


class SimpleButton(OpenGLComponent):

    def __init__(self, **argd):
        super(SimpleButton, self).__init__(**argd)

        # Button initialisation
        caption = argd.get("caption", "Button")

        self.backgroundColour = argd.get("bgcolour", (244,244,244))
        self.sideColour = argd.get("sidecolour", (200,200,244))
        self.key = argd.get("key", None)

        self.eventMsg = argd.get("msg", "CLICK")
        
        self.size = Vector(*argd.get("size", (1,1,1)))

        self.grabbed = 0


    def setup(self):
        self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN ])


    def draw(self):
        hs = self.size/2.0
        # draw faces
        glBegin(GL_QUADS)
        glColor4f(self.sideColour[0]/256.0, self.sideColour[1]/256.0, self.sideColour[2]/256.0, 0.5)
        # right face
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)
        # left face
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        # top face
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)
        # bottom face
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)

        glColor4f(self.backgroundColour[0]/256.0, self.backgroundColour[1]/256.0, self.backgroundColour[2]/256.0, 0.5)
        # back face
        glVertex3f(hs.x,hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        # front face
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glEnd()
        

    def handleEvents(self):
        while self.dataReady("events"):
            activate = False
            event = self.recv("events")
            if event.type == pygame.KEYDOWN:
                if event.key == self.key:
                    activate = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.identifier in event.hitobjects:
                    self.grabbed = event.button
                    self.scaling = Vector(0.9,0.9,0.9)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.grabbed = 0
                    self.scaling = Vector(1,1,1)
                    #activate
                    if self.identifier in event.hitobjects:
                        activate = True
                        
            if activate:
                self.send( self.eventMsg, "outbox" )


if __name__=='__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline

    Graphline(
        button1 = SimpleButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
        button2 = SimpleButton(size=(2,2,1), position=(5,0,-15), msg="BRAIN"),
        echo = ConsoleEchoer(),
        linkages = {
            ("button1", "outbox") : ("echo", "inbox"),
            ("button2", "outbox") : ("echo", "inbox")
        }
    ).run()
    
