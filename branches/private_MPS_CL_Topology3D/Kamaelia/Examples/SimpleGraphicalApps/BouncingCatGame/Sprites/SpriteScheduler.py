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

import pygame
pygame.init()
import time


from Axon.Component import component
from Axon.Ipc import newComponent

class SpriteScheduler(component):
   def __init__(self, cat_args, cat_sprites, background, display_surface, eventHandlerClass=None):
      super(SpriteScheduler,self).__init__()
      self.allsprites = []
      self.cat_args = cat_args
      self.cat_sprites = cat_sprites
      self.background = background
      self.display_surface = display_surface
      self.eventHandlerClass = eventHandlerClass

   def main(self):
      event_handler = self.eventHandlerClass(self.cat_args)
      self.allsprites = pygame.sprite.RenderPlain(self.cat_sprites)
      while 1:
         for event in pygame.event.get():
            event_handler.dispatch(event,self)
         self.allsprites.update() # This forces the "logic" method in BasicSprites to be updated
         self.display_surface.blit(self.background, (0, 0))
         self.allsprites.draw(self.display_surface)
         pygame.display.flip()
         yield 1
