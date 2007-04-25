#!/usr/bin/env python
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
"""\
========================
Pygame Sprite Scheduling
========================

A component that manages updating and blitting a collection of pygame sprites
and also uses a configurable event dispatch mechanism.

Probably cannot coexist with a Pygame Display service at runtime.



Example Usage
-------------

Five sprites bouncing around the screen, that all freeze/unfreeze when the mouse is
clicked::

    import pygame
    pygame.init()
    from Kamaelia.UI.Pygame.SpriteScheduler import SpriteScheduler
    from Kamaelia.UI.Pygame.BasicSprite import BasicSprite
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.UI.Pygame.EventHandler import EventHandler
    from Kamaelia.Physics.Behaviours import cartesianPingPong
    width, height = (800,600)
    
    width, height = (800,600)
    scr = pygame.display.set_mode((width,height), 0)
    bg  = pygame.image.load("background800x600imagefile")
    bg  = bg.convert()        # renders faster if in same pixformat
    
    sprites = []
    for i in range(0,5):
        img = pygame.image.load("spriteimagefile")
        img = img.convert()
        newSprite = BasicSprite(image=img)
        bouncing = cartesianPingPong(point=[50*i,40*i], width=width, height=height, border=100)
        Graphline(sprite=newSprite, translation=bouncing,
                    linkages={ ("translation","outbox"):("sprite","translation") }
                    ).activate()
        sprites.append(newSprite)
    
    eventargs = {"sprites":sprites}
    
    class MyEvents(EventHandler):
        def __init__(self, args):
            super(MyEvents, self).__init__()
            self.sprites = args['sprites']
        def mousebuttondown(self, pos, button, where):
            for sprite in self.sprites:
                sprite.togglePause()
    
    SpriteScheduler(eventargs, sprites, bg, scr, MyEvents).run()




How does it work?
-----------------

When initialising, you pass it a list of pygame sprite objects, a background
image, the pygame display window surface, and an event handling class.

The sprites are grouped in a pygame sprite Group object which is used to render
and update them. The specified event handler class is instantiated, with the
specified arguments being passed to the initialiser. This is used to respond to
events from pygame such as mouse clicks.

Because this component effectively forms a pygame main loop, it cannot coexist
with a Pygame Display service.

This component ignores any incoming messages on any of its inboxes. It does not
send anything out of any of its outboxes.

This component does not terminate.
"""

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX VOMIT : Does not interoperate with Pygame Display component
#
#             - in particular the event dispatch mechanism will need to be
#               tied to the Pygame Display one.
#
#             - interaction with BasicSprite compoennt (if used) will need
#               improvement as this component calls methods on BasicSprite.
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import pygame
pygame.init()
import time


from Axon.Component import component
from Axon.Ipc import newComponent

class SpriteScheduler(component):
   """\
   SpriteScheduler(cat_args, cat_sprites, background, display_surface, eventHandlerClass) -> new SpriteScheduler component.

   Manages updating and blitting a collection of pygame sprites. Instantiates an
   event handler object to handle dispatching of events from pygame.

   Keyword arguments:
   
   - cat_args           -- arguments for event handler class instantiation
   - cat_sprites        -- Pygame sprite objects to be rendered
   - background         -- Pygame surface to be rendered as a background image
   - display_surface    -- Pygame surface to render sprites onto
   - eventHandlerClass  -- Event handler class, with method: dispatch(event,source)
   """

   Inboxes  = { "inbox"   : "NOT USED",
                "control" : "NOT USED",
              }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "NOT USED",
              }
    
   def __init__(self, cat_args, cat_sprites, background, display_surface, eventHandlerClass=None):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(SpriteScheduler,self).__init__()
      self.allsprites = []
      self.cat_args = cat_args
      self.cat_sprites = cat_sprites
      self.background = background
      self.display_surface = display_surface
      self.eventHandlerClass = eventHandlerClass

   def main(self):
      """Main loop."""
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

__kamaelia_components__  = ( SpriteScheduler, )
