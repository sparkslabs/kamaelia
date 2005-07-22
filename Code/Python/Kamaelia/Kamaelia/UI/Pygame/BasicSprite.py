#!/usr/bin/python
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
      self.paused = False
      self.update = self.logic().next

   def logic(self):
      center = list(self.rect.center)
      self.image = self.original
      current = self.image
      scale = 1.0
      angle = 1
      pos = center
      while 1:
         if not self.paused:
            self.image = current
            if self.dataReady("imaging"):
               self.image = self.recv("imaging")
               current = self.image

            if self.dataReady("scaler"):
               # Scaling
               scale = self.recv("scaler")
            w,h = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (w*scale, h*scale))

            if self.dataReady("rotator"):
               angle = self.recv("rotator")
               # Rotation
            self.image = pygame.transform.rotate(self.image, angle)

            if self.dataReady("translation"):
               # Translation
               pos = self.recv("translation")
            self.rect = self.image.get_rect()
            self.rect.center = pos

         yield 1
   def shutdown(self):
      self.send("shutdown", "signal")
   def togglePause(self):
      if self.paused:
         self.unpause()
      else:
         self.pause()

   def unpause(self):
      self.paused = False
      self.send("unpause", "signal")
   def pause(self):    
      self.paused = True
      self.send("togglepause", "signal")
