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
==============================
Matched Translation Interactor
==============================

An interactor for moving OpenGLComponents corresponding to mouse
movement along the X,Y plane.

MatchedTranslationInteractor is a subclass of Interactor.

Example Usage
-------------
The following example shows four SimpleCubes which can be moved by
dragging your mouse::

    o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1)).activate()
    i1 = MatchedTranslationInteractor(target=o1).activate()

    o2 = SimpleCube(position=(0, 0,-20), size=(1,1,1)).activate()
    i2 = MatchedTranslationInteractor(target=o2).activate()

    o3 = SimpleCube(position=(-3, 0,-10), size=(1,1,1)).activate()
    i3 = MatchedTranslationInteractor(target=o3).activate()

    o4 = SimpleCube(position=(15, 0,-40), size=(1,1,1)).activate()
    i4 = MatchedTranslationInteractor(target=o4).activate()

    Axon.Scheduler.scheduler.run.runThreads()  

How does it work?
-----------------
MatchedTranslationInteractor is a subclass of Interactor. It overrides
the __init__(), setup(), handleEvents() and frame() methods.

The matched movement works by using the position of the controlled
object and determine its X,Y-aligned plane. The amount of mouse movement
is then calculated as if it was on this plane. This is done by
intersecting the direction vector which is included in the mouse event
with the plane to get the point of intersection. Then the distance
between the newly generated point and the last point is calculated. The result
is the actual amount of movement along the X and the Y axis.

The interactor makes all the linkages it needs during initialisation.
Because the interactor needs the actual position of the controlled
component to be accurate all the time, it uses the components "position"
outbox by default. If you don't want the interactor to make the
linkages, you can set nolink=True as constructor argument. The following
linkages are needed for the interactor to work (from the interactors
point of view)::

    self.link( (self, "outbox"), (self.target, "rel_position") )
    self.link( (self.target, "position"), (self, "inbox") )

"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from Intersect import *
from Interactor import *

class MatchedTranslationInteractor(Interactor):
    """\
    MatchedTranslationInteractor(...) -> A new MatchedTranslationInteractor component.
    
    An interactor for moving OpenGLComponents corresponding to mouse
    movement along the X,Y plane.
    """
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(MatchedTranslationInteractor, self).__init__(**argd)

        self.grabbed = False
        self.position = None
        self.oldpoint = None
            
        if self.nolink == False:
            self.link( (self, "outbox"), (self.target, "rel_position") )
            self.link( (self.target, "position"), (self, "inbox") )


    def setup(self):
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])


    def handleEvents(self):
        while self.dataReady("events"):
            event = self.recv("events")

            if self.position is not None:
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEMOTION and self.grabbed:
                    p1 = self.position.copy()
                    p1.x += 10
                    p2 = self.position.copy()
                    p2.y += 10
                    z = Intersect.ray_Plane(Vector(0,0,0), event.direction, [self.position, p1, p2])
                    newpoint = event.direction * z
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.identifier in event.hitobjects:
                    if event.button == 1:
                        self.grabbed = True
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.grabbed = False
                        
                if event.type == pygame.MOUSEMOTION:
                    if self.grabbed == True:
                        if self.oldpoint is not None:
                            diff = newpoint-self.oldpoint
                            amount = (diff.x, diff.y)
                            self.send(amount, "outbox")

                try:
                    self.oldpoint = newpoint
                except NameError: pass            


    def frame(self):
        while self.dataReady("inbox"):
            self.position = Vector(*self.recv("inbox"))

__kamaelia_components__ = ( MatchedTranslationInteractor, )

if __name__=='__main__':
    from SimpleCube import *
    
    o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1), name="center").activate()
    i1 = MatchedTranslationInteractor(target=o1).activate()

    o2 = SimpleCube(position=(0, 0,-20), size=(1,1,1), name="center").activate()
    i2 = MatchedTranslationInteractor(target=o2).activate()

    o3 = SimpleCube(position=(-3, 0,-10), size=(1,1,1), name="center").activate()
    i3 = MatchedTranslationInteractor(target=o3).activate()

    o4 = SimpleCube(position=(15, 0,-40), size=(1,1,1), name="center").activate()
    i4 = MatchedTranslationInteractor(target=o4).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
