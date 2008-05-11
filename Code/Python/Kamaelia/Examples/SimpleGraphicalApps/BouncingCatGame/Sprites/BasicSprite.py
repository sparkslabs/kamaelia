#!/usr/bin/python
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
#
#
#

import pygame
from pygame.locals import *
import pygame.mixer
import random
import os
pygame.init()

from Axon.Component import component

class BasicSprite(pygame.sprite.Sprite, component):
   Inboxes=["rotator","translation","scaler", "imaging","inbox", "control"]
   def __init__(self, **argd):
      pygame.sprite.Sprite.__init__(self)
      component.__init__(self)

      self.image = argd["image"]
      self.original = self.image
      self.rect = self.image.get_rect()
      self.rect.topleft = argd.get("position",(10,10))
      self.frozen = False
      self.update = self.sprite_logic().next

   def main(self):
      while 1:
         yield 1

   def sprite_logic(self):
      center = list(self.rect.center)
      self.image = self.original
      current = self.image
      scale = 1.0
      angle = 1
      pos = center
      while 1:
         if not self.frozen:
            self.image = current
            if self.dataReady("imaging"):
               self.image = self.recv("imaging")
               current = self.image
            if self.dataReady("scaler"):
               # Scaling
               scale = self.recv("scaler")
            w,h = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (int(w*scale), int(h*scale)))

            if self.dataReady("rotator"):
               # Rotation
               angle = self.recv("rotator")
            self.image = pygame.transform.rotate(self.image, angle)
            if self.dataReady("translation"):
               # Translation
               pos = self.recv("translation")
            self.rect = self.image.get_rect()
            self.rect.center = pos
         yield 1
   def shutdown(self):
      self.send("shutdown", "signal")
   def toggleFreeze(self):
      if self.frozen:
         self.unfreeze()
      else:
         self.freeze()

   def unfreeze(self):
      self.frozen = False
      self.send("unfreeze", "signal")
   def freeze(self):
      self.frozen = True
      self.send("togglefreeze", "signal")
