#!/usr/bin/env python
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

class CMagnaDoodle(Axon.Component.component):
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
      super(CMagnaDoodle,self).__init__()
      
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

__kamaelia_components__  = ( CMagnaDoodle, )

# import shards
from SMouseEventHandling import *
from SDrawing import *
from SShutdownHandling import *
from shard import *

# add shard methods
shardify = addShards(MouseEventHandler, Drawing, ShutdownHandler)
shardify(FMagnaDoodle)


if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from pygame.locals import *
   
   CMagna = CMagnaDoodle().activate()
   
   Axon.Scheduler.scheduler.run.runThreads()
