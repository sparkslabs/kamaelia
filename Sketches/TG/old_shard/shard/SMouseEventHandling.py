# -*- coding: utf-8 -*-

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
import pygame
# uses methods defined in Drawing

class MouseEventHandler:
    """
    Code adapted slightly from MagnaDoodle.py and moved into separate module
    Methods added back to ShardMagnaDoodle using shard wrapper function
    """
    def handleMouseDown(self, event):
        if event.button == 1:
            self.drawing = True
        elif event.button == 3:
            self.oldpos = None
            
            # in Drawing
            self.drawBG()
            self.blitToSurface()
      
    def handleMouseUp(self, event):
        if event.button == 1:
            self.drawing = False
            self.oldpos = None
      
    def handleMouseMotion(self, event):
        if self.drawing and self.innerRect.collidepoint(*event.pos):
            if self.oldpos == None:
                self.oldpos = event.pos
            else:
                pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
                self.oldpos = event.pos
            self.blitToSurface() # in Drawing
      
    def handleMouseEvents(self, fromBox = "inbox"):
        while self.dataReady(fromBox):
            for event in self.recv(fromBox):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleMouseDown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handleMouseUp(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handleMouseMotion(event)
   
    def registerMouseListeners(self):
        self.send( { "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                            "surface" : self.display},
                            "display_signal")
      
        self.send( { "ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                            "surface" : self.display},
                            "display_signal")
      
        self.send( { "ADDLISTENEVENT" : pygame.MOUSEMOTION,
                            "surface" : self.display},
                            "display_signal")
    
    def test(self):
        print repr(self)
        
import shard
shard.requires('blitToSurface', 'drawBG')(MouseEventHandler)