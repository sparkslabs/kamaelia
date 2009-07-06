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

import pygame
from Axon.Component import component

class BasicSprite(pygame.sprite.Sprite, component):
    Inboxes=["translation", "imaging","inbox", "control"]
    allsprites = []
    def __init__(self, imagepath, name, pos = None,border=40):
        pygame.sprite.Sprite.__init__(self)
        component.__init__(self)
        self.imagepath = imagepath
        self.image = None
        self.original = None
        self.rect = None
        self.pos = pos
        if self.pos == None:
            self.pos = [100,100]
        self.dir = ""
        self.name  = name 
        self.update = self.sprite_logic().next
        self.screensize = (924,658)
        self.border = border
        self.__class__.allsprites.append(self)

    def allSprites(klass):
        return klass.allsprites
    allSprites = classmethod(allSprites)

    def sprite_logic(self):
        while 1:
            yield 1

    def main(self):
        self.image = pygame.image.load(self.imagepath)
        self.original = self.image
        self.image = self.original
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        center = list(self.rect.center)
        current = self.image
        pos = center
        dx,dy = 0,0
        d = 10 # Change me to change the velocity of the sprite
        while 1:
            self.image = current

            if self.dataReady("imaging"):
                self.image = self.recv("imaging")
                current = self.image
            if self.dataReady("translation"):
                pos = self.recv("translation")

            if self.dataReady("inbox"):
                event = self.recv("inbox")
                if event == "start_up": dy = dy + d
                if event == "stop_up": dy = dy - d

                if event == "start_down": dy = dy - d
                if event == "stop_down": dy = dy + d

                if event == "start_right": dx = dx + d
                if event == "stop_right": dx = dx - d

                if event == "start_left": dx = dx - d
                if event == "stop_left": dx = dx + d

            if dx !=0 or dy != 0: 
                self.pos[0] += dx
                if self.pos[0] >self.screensize[0]-self.border: self.pos[0] =self.screensize[0]-self.border
                if self.pos[1] >self.screensize[1]-self.border: self.pos[1] =self.screensize[1]-self.border
                if self.pos[0]  <self.border: self.pos[0] = self.border
                if self.pos[1] < self.border: self.pos[1] = self.border
                self.pos[1] -= dy
                self.rect.center = (self.pos)
                self.send(self.pos, "outbox")

            yield 1

