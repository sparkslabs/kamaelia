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
