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

from Visualisation.Graph import BaseParticle

import pygame
from pygame.locals import *

def abbreviate(string): # SMELL: Exists in two files and is *used* in both.
    """Abbreviates strings to capitals, word starts and numerics and underscores"""
    out = ""
    prev = ""
    for c in string:
        if c.isupper() or c.isdigit() or c == "_" or c == "." or (c.isalpha() and not prev.isalpha()):
            out += c.upper()
        prev = c
    return out

_COMPONENT_RADIUS = 32    


def nearest45DegreeStep( (dx,dy) ):
    """Returns (in degrees) the nearest 45 degree angle match to the supplied vector.
    
       Returned values are one of 0, 45, 90, 135, 180, 225, 270, 315.       
       If the supplied vector is (0,0), the returned angle is 0.
    """
    if dx == 0 and dy == 0:
        return 0
    
    # rotate dy and dx by +22.5 degrees,
    # so the boundaries between the 45 degree regions now nicely
    # line up with 0, 45, 90, ... instead of 22.5, 67,5 etc
    
    cos = 0.92387953251128674     # math.cos(math.radians(22.5))
    sin = 0.38268343236508978     # math.sin(math.radians(22.5))
    dx, dy = (dx*cos - dy*sin), (dy*cos + dx*sin)
        
    # lookup angle against properties of dy and dx     
    index = ( dy > 0, dx > 0, abs(dy) > abs(dx) )
    return angleMappings[index]

angleMappings = { (True,  True,  False) : 0,
                  (True,  True,  True ) : 45,
                  (True,  False, True ) : 90,
                  (True,  False, False) : 135,
                  (False, False, False) : 180,
                  (False, False, True ) : 225,
                  (False, True,  True ) : 270,
                  (False, True,  False) : 315 }
            
class PPostbox(BaseParticle):
    labelangles =  { 0:2, 45:3, 90:0, 135:1, 180:2, 225:3, 270:0, 315:1 } # angles to which label tile
    
    colours = { ("inbox",  "outbox"):(0,160,0),
                ("outbox", "inbox" ):(0,160,0),
                ("inbox",  "inbox" ):(224,128,0),
                ("outbox", "outbox"):(224,128,0)  }

    def Inbox(ID, position, name):
        return PPostbox(ID=ID, position=position, name=name, boxtype="inbox")
    def Outbox(ID, position, name):
        return PPostbox(ID=ID, position=position, name=name, boxtype="outbox")
    Inbox  = staticmethod(Inbox)
    Outbox = staticmethod(Outbox)
                
    def __init__(self, ID, position, name, boxtype):
        super(PPostbox,self).__init__(position=position, ID = ID )
        self.name   = name
        self.ptype  = "postbox"
        self.postboxtype = boxtype
        self.left   = 0
        self.top    = 0
        self.radius = 16
        self.buildLabels()
        self.selected = False
        
        
    def buildLabels(self):
        from pygame.transform import rotozoom, rotate
        
        font = pygame.font.Font(None, 14)
        
        label = font.render(" "+abbreviate(self.name)+" ", True, (0,0,0), )
        self.label   = []   # 'selected' labels
        self.labelxo = []
        self.labelyo = []
        self.label.append(rotate(label, 90))
        self.label.append(rotozoom(label, 45, 1.0))
        self.label.append(label)
        self.label.append(rotozoom(label, -45, 1.0))

        slabel = font.render(" "+abbreviate(self.name)+" ", True, (96,96,255), )
        self.slabel  = []
        self.slabel.append(rotate(slabel, 90))
        self.slabel.append(rotozoom(slabel, 45, 1.0))
        self.slabel.append(slabel)
        self.slabel.append(rotozoom(slabel, -45, 1.0))
        
        
        for l in self.label:
            self.labelxo.append( - l.get_width()  / 2 )
            self.labelyo.append( - l.get_height() / 2 )

        font = pygame.font.Font(None, 20)
        self.desclabel = font.render(self.postboxtype.upper()+" : "+self.name, True, (0,0,0), (255,255,255))
                    
            
    def render(self, surface):
        direction = (0,0) # default direction for the text label
        
        yield 1
        x = int(self.pos[0] - self.left)
        y = int(self.pos[1] - self.top )
        for p in self.bondedTo:
            endx = int(p.pos[0] - self.left)
            endy = int(p.pos[1] - self.top)
            
            colour = PPostbox.colours[ (self.postboxtype, p.postboxtype) ]
            
            pygame.draw.line(surface, colour, (x,y),  (endx,endy) )
            
            # draw a pwetty arrow on the line, showing the direction
            mid = ( (x+endx*3)/4, (y+endy*3)/4 )
            
            direction = ( (endx-x), (endy-y) )
            length    = ( direction[0]**2 + direction[1]**2 )**0.5
            direction = [ 6*n / length for n in direction ]
            
            norm      = ( -direction[1], direction[0] )
            
            leftarrow  = ( mid[0] - direction[0] - norm[0], mid[1] - direction[1] - norm[1] )
            rightarrow = ( mid[0] - direction[0] + norm[0], mid[1] - direction[1] + norm[1] )
            
            pygame.draw.line(surface, colour, mid, leftarrow  )
            pygame.draw.line(surface, colour, mid, rightarrow )
        
        yield 3
        # if we've not got a 'direction' yet for the text label (from bonds 'from' this node )
        # then look at bonds 'to' this node from other nodes of the same type
        if direction==(0,0):
            for p in self.bondedFrom:
                if p.ptype == self.ptype:
                    endx = int(p.pos[0] - self.left)
                    endy = int(p.pos[1] - self.top)
                    direction = ( (endx-x), (endy-y) )
        
        # render name label, tilted along the 'direction'
        i = PPostbox.labelangles[ nearest45DegreeStep(direction) ]
        if self.selected:
            l = self.slabel[i]
        else:
            l = self.label[i]
        surface.blit(l, ( x + self.labelxo[i], y + self.labelyo[i] ) )

        if self.selected:
            yield 10
            surface.blit(self.desclabel, (72,16) )

                                 
    def setOffset( self, (x,y) ):
        self.left = x
        self.top  = y
                     
    def select( self ):
        self.selected = True

    def deselect( self ):
        self.selected = False
