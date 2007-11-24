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

from Kamaelia.Visualisation.PhysicsGraph import BaseParticle
from pygame.locals import *

_COMPONENT_RADIUS = 32
_COMPONENT_RADIUS_FACTOR = 1.3


def abbreviate(string):
    """Abbreviates dot-delimited string to the final (RHS) term"""
    return string.split(".")[-1]

def acronym(string):
    """Abbreviates strings to capitals, word starts and numerics and underscores"""
    out = ""
    prev = ""
    for c in string:
        if c.isupper() or c == "_" or c == "." or (c.isalpha() and not prev.isalpha()):
            out += c.upper()
        prev = c
    return out

colours = [ (255,128,128),
            (255,192,128),
            (224,224,128),
            (128,255,128),
            (128,255,192),
            (128,224,224),
            (128,128,255),
          ]

class PEntity(BaseParticle):
    def __init__(self, ID, position, name):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PEntity,self).__init__(position=position, ID = ID )
        self.set_label(name)
        self.ptype = "entity"
        self.shortname = abbreviate(name)
        self.left = 0
        self.top = 0
        self.selected = False
        self.radius = _COMPONENT_RADIUS
        self.radius_x = int(_COMPONENT_RADIUS*_COMPONENT_RADIUS_FACTOR)
        self.radius_y = int(_COMPONENT_RADIUS/_COMPONENT_RADIUS_FACTOR)
    def set_label(self, newname):
        self.name = newname
        self.shortname = abbreviate(newname)
        acro = acronym(newname)
        oldhue = []
        for i in xrange(len(acro)):
            factor = acro[:i+1]
            print factor
            hue = list(colours [ factor.__hash__() % len(colours)])
            if oldhue == []:
               oldhue = hue
            else:
               hue[0] = (hue[0] + oldhue[0])/2
               hue[1] = (hue[1] + oldhue[1])/2
               hue[2] = (hue[2] + oldhue[2])/2

        self.colour = hue
        self.bordercolour = [x*.75 for x in hue]

        pygame.font.init()
        font = pygame.font.Font(None, 20)
        self.slabel   = font.render(self.shortname, True, (0,0,0))
        self.slabelxo = - self.slabel.get_width()/2
        self.slabelyo = - self.slabel.get_height()/2
        description = "Entity "+self.shortname+" : "+self.name
        self.desclabel = font.render( description, True, (0,0,0), (255,255,255))

    def render(self, surface):
        """\
        Multi-pass rendering generator.

        Renders this particle in multiple passes to the specified pygame surface - 
        yielding the number of the next pass to be called on between each. Completes
        once it is fully rendered.
        """
        x = int(self.pos[0] - self.left)
        y = int(self.pos[1] - self.top )

        yield 1
        for p in self.bondedTo:
            px = int(p.pos[0] - self.left)
            py = int(p.pos[1] - self.top )
            pygame.draw.line(surface, (192,192,192), (x,y), (px,py))

        yield 2

        colour = self.colour
        bordercolour = self.bordercolour
        if self.selected:
            colour = (160,160,255)
            bordercolour = (224,0,0)

        points = [
                (x-self.radius_x,y-self.radius_y),
                (x-self.radius_x,y+self.radius_y),
                (x+self.radius_x,y+self.radius_y),
                (x+self.radius_x,y-self.radius_y),
        ]
        pygame.draw.polygon(surface, colour, points)
        pygame.draw.polygon(surface, bordercolour, points,3)

        yield 3
        surface.blit(self.slabel, ( x+self.slabelxo, y+self.slabelyo ) )
        if self.selected:
            yield 10
            surface.blit(self.desclabel, (72,16) )

    def setOffset( self, (x,y) ):
        """\
        Set the offset of the top left corner of the rendering area.

        If this particle is at (px,py) it will be rendered at (px-x,py-y).
        """
        self.left = x
        self.top  = y

    def select( self ):
        """Tell this particle it is selected"""
        self.selected = True

    def deselect( self ):
        """Tell this particle it is deselected"""
        self.selected = False

