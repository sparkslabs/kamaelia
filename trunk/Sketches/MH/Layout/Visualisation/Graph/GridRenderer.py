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

# Simple topography viewer server - takes textual commands from a single socket
# and renders the appropriate graph

import pygame

class GridRenderer(object):
    def __init__(self, size, colour):
        super(GridRenderer,self).__init__(size, colour)
        self.gridSize = int(size)
        self.colour   = colour
        self.left     = 0
        self.top      = 0

    def render(self, surface):
        yield -1
        for i in range((self.top // self.gridSize) * self.gridSize - self.top,
                       surface.get_height(),
                       self.gridSize):
            pygame.draw.line(surface, self.colour,
                             (0,i),
                             (surface.get_width(),i) )

        for i in range((self.left // self.gridSize) * self.gridSize - self.left,
                       surface.get_width(), 
                       self.gridSize):
            pygame.draw.line(surface, self.colour, 
                             (i, 0                   ), 
                             (i, surface.get_height()) )

    def setOffset( self, (left,top) ):
        """Inform of a change to the coords of the top left of the drawing surface,
        so that this entity can render, as if the top left had moved
        """
        self.left = left
        self.top  = top
