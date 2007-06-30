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
===========================
Simple Pygame drawing board
===========================

A simple drawing board for the pygame display service.

Use your left mouse button to draw to the board and the
right to erase your artwork.

# Shard experimental version: event handling and drawing moved
    out to MouseEventHandling.py, ShutdownHandling.py and Drawing.py
# Original MagnaDoodle in Kamaelia/UI/Pygame
# Shards connected with class decorator-style method

"""

import pygame
import Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.PygameDisplay import PygameDisplay

class ShardMagnaDoodle(Axon.Component.component):
   """\
   MagnaDoodle(...) -> A new MagnaDoodle component.

   A simple drawing board for the pygame display service.

   (this component and its documentation is heaviliy based on Kamaelia.UI.Pygame.Button)

   Keyword arguments:
   
   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - transparent  -- draw background transparent if True (default=False)
   - size         -- None or (w,h) in pixels (default=None)
   
   """
   
   Inboxes = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay"
             }
   Outboxes = { "outbox" : "not used",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
   
   def __init__(self, caption=None, position=None, margin=8, bgcolour = (124,124,124), fgcolour = (0,0,0), msg=None,
                transparent = False, size=(200,200)):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ShardMagnaDoodle,self).__init__()
      
      # in Drawing
      self.displaySetup(bgcolour, fgcolour, margin, size, transparent, position)
            
      if msg is None:
         msg = ("CLICK", self.id)
      self.eventMsg = msg      
      
   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      waiting = True
      while waiting:
         if self.dataReady(boxname): return
         else: yield 1
    
   def main(self):
      """Main loop."""
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")
             
      for _ in self.waitBox("callback"):
         yield 1
      
      self.display = self.recv("callback")
      
      # in Drawing
      self.drawBG()
      self.blitToSurface()
      
      # in MouseEventHandling
      self.registerMouseListeners()
      
      done = False
      while not done:
         done = self.handleShutdown()  # in ShutdownHandling
         self.handleMouseEvents()  # in MouseEventHandling
         self.pause()
         yield 1

__kamaelia_components__  = ( ShardMagnaDoodle, )

# import shards
#from SMouseEventHandling import *
from SMouseSwap import *   # subclassing works using im_func for superclass calls
from SDrawing import *
from SShutdownHandling import *
from shard import *

# add shard methods
shardify = addShards(ClickPrint, Drawing, ShutdownHandler)  # subclass test
#shardify = addShards(MouseEventHandler, Drawing, ShutdownHandler)
shardify(ShardMagnaDoodle)
a = MouseEventHandler.test

if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from pygame.locals import *
   
   SMagna = ShardMagnaDoodle().activate()
   
   Axon.Scheduler.scheduler.run.runThreads()
