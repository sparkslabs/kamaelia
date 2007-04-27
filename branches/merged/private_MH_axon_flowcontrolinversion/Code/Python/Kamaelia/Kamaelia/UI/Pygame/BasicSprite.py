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
===================
Basic Pygame Sprite
===================

This component implements a basic pygame sprite that can be scaled, moved,
changed and rotated at will.

At present this component must be used in conjunction with a SpriteScheduler
component.



Example Usage
-------------

See SpriteScheduler.


How does it work?
-----------------

This class is both a component and a pygame Sprite.

Supply an initial image (as a pygame surface) and position during initalisation.

The sprite will be transformed or translated in response to messages sent to its
"rotator", "translation" and "scaler" inboxes. Send angles in degrees to the
"rotator" inbox; (x,y) tuples to the "translation" inbox; and scale factors to
its "scaler" inbox.

You can change the sprite image at any time by sending a new one to its
"imaging" inbox.

This compnoent ignores messages on its "inbox" and "control" inboxes. It does
not terminate, event when its shutdown() method is called (see below).

The "signal" outbox is used to output status message strings: "unpause",
"togglepause" and "shutdown".

This component does not register with the PygameDisplay service and does not
actually blit its sprite onto the display itself. It relies on a parent
SpriteScheduler component - to which this component should be passed.

SpriteScheduler calls the update() method of this component. which effectively
supplants the role of the main() method. In addition, there are pause(),
unpause() and togglePause() methods which will cause the component to pause -
by stopping reading incoming messages from inboxes. There is also a shutdown()
method that sends the string "shutdown" out of its "signal" outbox (but does not
actually cause the component to terminate in any way).

Note that these method calls break the decoupling tenets of Kamaelia components.
*It is strongly recommended to not use this component at the present time.*
"""

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX VOMIT : Urrgh, it doesn't use its own main loop. Relies on a central
#             SpriteScheduler component calling its update() method.
#
#             Nonononononononnononooo! Needs to move this code into its own
#             main loop. Remove SpriteScheduler and update example 9 that
#             relies on this! ... or some other form of fix. Anything but this!
#
#             Also the pause/unpause code does a different job to microprocess
#             pausing, but name clashes.
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import pygame
from pygame.locals import *
import pygame.mixer
import random
import os
pygame.init()

from Axon.Component import component

class BasicSprite(pygame.sprite.Sprite, component):
   """\
   BasicSprite(image[,position]) -> new BasicSprite component.

   A sprite for a pygame application. Can be changed, moved, scaled and rotated
   on the fly.

   Does not use the standard component 'main' loop - must be used in conjunction
   with SpriteSheduler.

   Keyword arguments:
   - image     -- pygame surface containing the image
   - position  -- (x,y) pixels position of the top left corner (default=(10,10))
   """
   
   Inboxes = { "inbox"       : "NOT USED",
               "control"     : "NOT USED",
               "rotator"     : "Rotate by 'n' degrees counterclockwise",
               "translation" : "Change position to (x,y) in pixels",
               "scaler"      : "Change size (1.0=original)",
               "imaging"     : "Change the image",
             }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "Diagnostic messages",
              }
   
   def __init__(self, **argd):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      pygame.sprite.Sprite.__init__(self)
      component.__init__(self)

      self.image = argd["image"]
      self.original = self.image
      self.rect = self.image.get_rect()
      self.rect.topleft = argd.get("position",(10,10))
      self.paused = False
      self.update = self.sprite_logic().next

   def main(self):
      """Main loop"""
      while 1:
         yield 1

   def sprite_logic(self):
      """Effectively the main loop. Listens for messages on inboxes and adjusts the sprite accordingly, unless 'paused'."""
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
      """Send shutdown message"""
      self.send("shutdown", "signal")
      
   def togglePause(self):
      """Toggle between paused and unpaused states"""
      if self.paused:
         self.unpause()
      else:
         self.pause()

   def unpause(self):
      """Unset paused flag, and signal "unpause" """
      self.paused = False
      self.send("unpause", "signal")
      
   def pause(self):    
      """Set paused flag, and signal "pause" """
      self.paused = True
      self.send("togglepause", "signal")

__kamaelia_components__  = ( BasicSprite, )
