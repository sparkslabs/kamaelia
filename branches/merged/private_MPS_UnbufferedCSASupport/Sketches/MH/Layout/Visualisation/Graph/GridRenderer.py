#!/usr/bin/env python

# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
