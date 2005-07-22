#!/usr/bin/python
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
