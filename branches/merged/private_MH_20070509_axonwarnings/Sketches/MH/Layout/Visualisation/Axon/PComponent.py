#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import pygame

from Visualisation.Graph import BaseParticle
from pygame.locals import *
_COMPONENT_RADIUS = 32

def abbreviate(string):
    """Abbreviates strings to capitals, word starts and numerics and underscores"""
    out = ""
    prev = ""
    for c in string:
        if c.isupper() or c.isdigit() or c == "_" or c == "." or (c.isalpha() and not prev.isalpha()):
            out += c.upper()
        prev = c
    return out

class PComponent(BaseParticle):
    def __init__(self, ID, position, name):
        super(PComponent,self).__init__(position=position, ID = ID )
        self.name = name
        self.ptype = "component"
        self.shortname = abbreviate(name)
        self.left = 0
        self.top = 0
        self.selected = False
        
        font = pygame.font.Font(None, 20)
        self.slabel   = font.render(self.shortname, True, (0,0,0))
        self.slabelxo = - self.slabel.get_width()/2
        self.slabelyo = - self.slabel.get_height()/2
        
        self.radius = _COMPONENT_RADIUS
        
        self.desclabel = font.render("Component "+self.shortname+" : "+self.name, True, (0,0,0), (255,255,255))
        
    def render(self, surface):
        x = int(self.pos[0] - self.left)
        y = int(self.pos[1] - self.top )
    
        yield 1
        for p in self.bondedTo:
            px = int(p.pos[0] - self.left)
            py = int(p.pos[1] - self.top )
            pygame.draw.line(surface, (192,192,192), (x,y), (px,py))
        
        yield 2
        colour = (192,192,192)
        if self.selected:
            colour = (160,160,255)
        pygame.draw.circle(surface, colour, (x,y), self.radius)
        surface.blit(self.slabel, ( x+self.slabelxo, y+self.slabelyo ) )
        if self.selected:
            yield 10
            surface.blit(self.desclabel, (72,16) )
                     
    def setOffset( self, (x,y) ):
        self.left = x
        self.top  = y

    def select( self ):
        """Tell this particle it is selected"""
        self.selected = True

    def deselect( self ):
        """Tell this particle it is selected"""
        self.selected = False
        
            
