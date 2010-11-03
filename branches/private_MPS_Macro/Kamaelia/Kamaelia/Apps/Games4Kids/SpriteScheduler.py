#!/usr/bin/python
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

import Axon
from Axon.Component import component
import pygame
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class SpriteScheduler(component):
    Inboxes = ["inbox", "control", "callback"]
    Outboxes= ["outbox", "signal", "display_signal"]
    # This is still non-idiomatic due to it directly handling the display.
    displaysize = (924, 658)
    bgcolour = (32,0,128)
    def __init__(self, sprites, **argd):
        super(SpriteScheduler,self).__init__(**argd)
        self.allsprites = []
        self.sprites = sprites
        self.background = pygame.Surface(self.displaysize)
        self.background.fill(self.bgcolour)
        self.disprequest = { "DISPLAYREQUEST" : True,
                             "callback" : (self,"callback"),
                             "size": self.displaysize,
                             "position" : (50,50)}

    def pygame_display_flip(self):
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def getDisplay(self):
       displayservice = PygameDisplay.getDisplayService()
       self.link((self,"display_signal"), displayservice)
       self.send(self.disprequest, "display_signal")
       while not self.dataReady("callback"):
           self.pause()
           yield 1
       self.display = self.recv("callback")

    def main(self):
        yield Axon.Ipc.WaitComplete(self.getDisplay())
        self.allsprites = pygame.sprite.RenderPlain(self.sprites)
        while 1:
            self.allsprites.update() # This forces the "logic" method in BasicSprites to be updated
            self.display.blit(self.background, (0, 0))
            try:
                self.allsprites.draw(self.display)
            except TypeError:
                pass
            self.pygame_display_flip()
            yield 1

