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
Simple Rotation Interactor
=====================
"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from Interactor import *

class SimpleRotationInteractor(Interactor):
    
    def __init__(self, **argd):
        super(SimpleRotationInteractor, self).__init__(**argd)

        self.rotationfactor = argd.get("rotationfactor", 1.0)
        
        self.grabbed = False

        if self.nolink == False:
            self.link( (self, "outbox"), (self.victim, "rel_rotation") )


    def setup(self):
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])


    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")
            if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                if event.button == 1:
                    self.grabbed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.grabbed = False
            if event.type == pygame.MOUSEMOTION:
                if self.grabbed == True:
                    amount = (float(event.rel[1])/self.rotationfactor, float(event.rel[0])/self.rotationfactor, 0)
                    self.send(amount, "outbox")


if __name__=='__main__':
    from SimpleCube import *

    o1 = SimpleCube(position=(6, 0,-30), name="center").activate()
    i1 = SimpleRotationInteractor(victim=o1).activate()

    o2 = SimpleCube(position=(0, 0,-20), name="center").activate()
    i2 = SimpleRotationInteractor(victim=o2).activate()

    o3 = SimpleCube(position=(-3, 0,-10), name="center").activate()
    i3 = SimpleRotationInteractor(victim=o3).activate()

    o4 = SimpleCube(position=(15, 0,-40), name="center").activate()
    i4 = SimpleRotationInteractor(victim=o4).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  
