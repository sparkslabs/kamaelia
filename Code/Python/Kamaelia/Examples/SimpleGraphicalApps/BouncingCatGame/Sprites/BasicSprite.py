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
#
#
#

import pygame
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
