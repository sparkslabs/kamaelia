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
=============================
Simple Translation Interactor
=============================

A simple interactor for moving OpenGLComponents along th X,Y plane.

SimpleTranslationInteractor is a subclass of Interactor.

Example Usage
-------------
The following example shows four SimpleCubes which can be moved by
dragging your mouse over them::

    o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1)).activate()
    i1 = SimpleTranslationInteractor(target=o1).activate()

    o2 = SimpleCube(position=(0, 0,-20), size=(1,1,1)).activate()
    i2 = SimpleTranslationInteractor(target=o2).activate()

    o3 = SimpleCube(position=(-3, 0,-10), size=(1,1,1)).activate()
    i3 = SimpleTranslationInteractor(target=o3).activate()

    o4 = SimpleCube(position=(15, 0,-40), size=(1,1,1)).activate()
    i4 = SimpleTranslationInteractor(target=o4).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  

How does it work?
-----------------
SimpleTranslationInteractor is a subclass of Interactor (for Interactor
functionality see its documentation). It overrides the __init__(),
setup() and handleEvents() methods.

The amount of movement is determined using the relative 2d movement
which is included in every mouse event and multiplying it by a factor.
This factor must be specified on creation of the component.

"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import Axon
from Interactor import *

class SimpleTranslationInteractor(Interactor):
    """\
    SimpleTranslationInteractor(...) -> A new SimpleTranslationInteractor component.
    
    A simple interactor for moving OpenGLComponents along th X,Y plane.

    Keyword arguments:

    - translationfactor -- factor to translate between 2d and 3d movement (default=10.0)
    """
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleTranslationInteractor, self).__init__(**argd)

        self.translationfactor = argd.get("translationfactor", 10.0)
        
        self.grabbed = False

        if self.nolink == False:
            self.link( (self, "outbox"), (self.target, "rel_position") )


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
                    amount = (float(event.rel[0])/self.translationfactor, -float(event.rel[1])/self.translationfactor)
                    self.send(amount, "outbox")

__kamaelia_components__ = (SimpleTranslationInteractor,)

if __name__=='__main__':
    from SimpleCube import *
    
    o1 = SimpleCube(position=(6, 0,-30), size=(1,1,1), name="center").activate()
    i1 = SimpleTranslationInteractor(target=o1).activate()

    o2 = SimpleCube(position=(0, 0,-20), size=(1,1,1), name="center").activate()
    i2 = SimpleTranslationInteractor(target=o2).activate()

    o3 = SimpleCube(position=(-3, 0,-10), size=(1,1,1), name="center").activate()
    i3 = SimpleTranslationInteractor(target=o3).activate()

    o4 = SimpleCube(position=(15, 0,-40), size=(1,1,1), name="center").activate()
    i4 = SimpleTranslationInteractor(target=o4).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
