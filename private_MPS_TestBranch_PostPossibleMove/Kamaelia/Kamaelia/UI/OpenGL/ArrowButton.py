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
=============================
Simple Arrow Button component
=============================

A simple arrow shaped button without caption. Implements responsive
button behavoir.

ArrowButton is a subclass of SimpleButton. It only overrides the draw()
method, i.e. it only changes its appearance.

Example Usage
-------------
Two arrow buttons printing to the console::

    Graphline(
        button1 = ArrowButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
        button2 = ArrowButton(size=(2,2,1), position=(5,0,-15), rotation=(0,0,90), msg="BRAIN"),
        echo = ConsoleEchoer(),
        linkages = {
            ("button1", "outbox") : ("echo", "inbox"),
            ("button2", "outbox") : ("echo", "inbox")
        }
    ).run()

"""

import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *

from Vector import Vector
from SimpleButton import SimpleButton


class ArrowButton(SimpleButton):
    """\
    ArrowButton(...) -> A new ArrowButton component.

    A simple arrow shaped button without caption. Implements responsive
    button behavoir.
    """

    def draw(self):    
        hs = self.size/2.0
        # draw faces
        glBegin(GL_QUADS)
        glColor4f(self.sideColour[0]/256.0, self.sideColour[1]/256.0, self.sideColour[2]/256.0, 0.5)
        # right face
        glVertex3f(0,hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(0,hs.y,-hs.z)
        # left face
        glVertex3f(0,hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(0,hs.y,-hs.z)
        # bottom face
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glEnd()

        glBegin(GL_TRIANGLES)
        glColor4f(self.backgroundColour[0]/256.0, self.backgroundColour[1]/256.0, self.backgroundColour[2]/256.0, 0.5)
        # back face
        glVertex3f(0,hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        # front face
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(0,hs.y,hs.z)
        glEnd()

__kamaelia_components__ = ( ArrowButton, )

if __name__=='__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline

    Graphline(
        button1 = ArrowButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
        button2 = ArrowButton(size=(2,2,1), position=(5,0,-15), rotation=(0,0,90), msg="BRAIN"),
        echo = ConsoleEchoer(),
        linkages = {
            ("button1", "outbox") : ("echo", "inbox"),
            ("button2", "outbox") : ("echo", "inbox")
        }
    ).run()
# Licensed to the BBC under a Contributor Agreement: THF
