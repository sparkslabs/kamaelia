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
from Physics import Particle as BaseParticle

class RenderingParticle(BaseParticle):
    """Version of Physics.Particle with added rendering functions. """

    def __init__(self, ID, position, name):
        super(RenderingParticle,self).__init__(position=position, ID = ID )
        self.radius = 20
        self.labelText = name
        
        font = pygame.font.Font(None, 24)
        self.label = font.render(self.labelText, False, (0,0,0))
        self.left = 0
        self.top  = 0
        self.selected = False
       
    def render(self, surface):
        """Rendering passes. A generator method that renders in multiple passes.
        Use yields to specify a wait until the pass the next stage of rendering
        should take place at.
        
        Example, that renders bonds 'behind' the blobs.
            def render(self, surface):
                yield 1
                self.renderBonds(surface)        # render bonds on pass 1
                yield 5 
                self.renderSelf(surface)         # render 'blob' on pass 5
        
         If another particle type rendered, for example, on pass 3, then it
         would be rendered on top of the bonds, but behind the blobs.
         
         Use this mechanism to order rendering into layers.
         """
        x = int(self.pos[0]) - self.left
        y = int(self.pos[1]) - self.top
        
        yield 1
        for p in self.bondedTo:
            pygame.draw.line(surface, (128,128,255), (x,y),  (int(p.pos[0] -self.left),int(p.pos[1] - self.top)) )
        
        yield 2
        pygame.draw.circle(surface, (255,128,128), (x,y), self.radius)
        if self.selected:
            pygame.draw.circle(surface, (0,0,0), (x,y), self.radius, 2)
        surface.blit(self.label, (x - self.label.get_width()/2, y - self.label.get_height()/2))
        
        
    def setOffset( self, (left,top) ):
        """Inform of a change to the coords of the top left of the drawing surface,
        so that this entity can render, as if the top left had moved
        """
        self.left = left
        self.top  = top

        
    def select( self ):
        """Tell this particle it is selected"""
        self.selected = True

    def deselect( self ):
        """Tell this particle it is selected"""
        self.selected = False
