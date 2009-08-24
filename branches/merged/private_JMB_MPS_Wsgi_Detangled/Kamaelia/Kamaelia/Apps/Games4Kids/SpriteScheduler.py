#!/usr/bin/python
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

