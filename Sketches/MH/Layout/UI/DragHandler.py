#!/usr/bin/env python
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
# -------------------------------------------------------------------------

import pygame
from pygame.locals import *

class DragHandler(object):
    """Dragging Handler framework.
    
    Implement detect() drag() and release() to create a dragging handler.
    Register this handler like this:
       pygameapp.addHandler(MOUSEMOTION, lambda event : MyDragHandler(event, pygameapp, *args, **argsd))
       
    If you add your own constructor, remember to initialise any variables you may need before calling the super
    class constructor.
    """
    
    def __init__(self, event, app):
        self.app     = app
        centre = self.detect(event.pos, event.button)
        if centre:
            self.startx =  centre[0]
            self.starty =  centre[1]
            self.offsetx = centre[0] - event.pos[0]
            self.offsety = centre[1] - event.pos[1]
            
            self.mm_handler = self.app.addHandler(MOUSEMOTION,   lambda event : self._drag(event.pos) )
            self.mu_handler = self.app.addHandler(MOUSEBUTTONUP, lambda event : self._release(event.pos) )
    
    def detect(self, pos, button):
        """Override this method. If you wish to accept the drag event and commence a drag,
        return the starting coordinates of the drag (x,y), otherwise return False
        to abort the drag"""
        return False
        
    def _drag(self, pos):
        self.drag( pos[0] + self.offsetx, pos[1] + self.offsety )
        
    def _release(self, pos):
        self.app.removeHandler(MOUSEMOTION,   self.mm_handler)
        self.app.removeHandler(MOUSEBUTTONUP, self.mu_handler)
        self.release( pos[0] + self.offsetx, pos[1] + self.offsety )

    def drag(self,newx,newy):
        """Override this method to handle whenever the drag moves to a new position"""
        pass
                
    def release(self,newx, newy):
        """Override this method to handle whenever the drag finishes at the final position"""
        pass
