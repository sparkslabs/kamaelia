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

from Physics_server1 import TopologyViewerServer, BaseParticle, Particle
from Physics import SimpleLaws, MultipleLaws

import pygame
from pygame.locals import *

def abbreviate(string):
    """Abbreviates strings to capitals, word starts and numerics and underscores"""
    out = ""
    prev = ""
    for c in string:
        if c.isupper() or c.isdigit() or c == "_" or (c.isalpha() and not prev.isalpha()):
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
        

        

class PComponent(BaseParticle):
    def __init__(self, ID, position, name):
        super(PComponent,self).__init__(position=position, ID = ID )
        self.name = name
        self.ptype = "component"
        self.shortname = abbreviate(name)
        
        font = pygame.font.Font(None, 16)
        self.slabel   = font.render(self.shortname, False, (0,0,0))
        self.slabelxo = - self.slabel.get_width()/2
        self.slabelyo = - self.slabel.get_height()/2
        
        self.radius = _COMPONENT_RADIUS
    
    def render(self, surface):
        yield 1
        for p in self.bondedTo:
            pygame.draw.line(surface, (255,0,0), [int(i) for i in self.pos],  [int(i) for i in p.pos])
        
        yield 2
        pygame.draw.circle(surface, (192,192,192), (int(self.pos[0]), int(self.pos[1])), self.radius)
        surface.blit(self.slabel, ( int(self.pos[0]) + self.slabelxo,
                                    int(self.pos[1]) + self.slabelyo )
                     )
    
class PPostbox(BaseParticle):
    labelangles =  { 0:2, 45:3, 90:0, 135:1, 180:2, 225:3, 270:0, 315:1 } # angles to which label tile

    def __init__(self, ID, position, name):
        super(PPostbox,self).__init__(position=position, ID = ID )
        self.name = name
        self.ptype = "postbox"

        font = pygame.font.Font(None, 12)
        
        self.radius = 16
        from pygame.transform import rotozoom, rotate
        
        label = font.render(self.name, False, (0,0,0), (255,255,255))
        self.label   = []
        self.labelxo = []
        self.labelyo = []
        self.label.append(rotate(label, 90))
        self.label.append(rotozoom(label, 45, 1.0))
        self.label.append(label)
        self.label.append(rotozoom(label, -45, 1.0))

        for l in self.label:
            self.labelxo.append( - l.get_width()  / 2 )
            self.labelyo.append( - l.get_height() / 2 )
        
    def render(self, surface):
        yield 1
        direction = (0,0)
        for p in self.bondedTo:
            start = [int(i) for i in self.pos]
            end   = [int(i) for i in p.pos]
            pygame.draw.line(surface, (0,160,0), start,  end)
            
            # draw a pwetty arrow on the line, showing the direction
            mid   = map(lambda a,b: (a+b*3)/4, start, end)
            
            direction = ( (end[0]-start[0]), (end[1]-start[1]) )
            length    = ( direction[0]**2 + direction[1]**2 )**0.5 / 6
            direction = [ x / length for x in direction ]
            
            norm      = ( -direction[1], direction[0] )
            
            pygame.draw.line(surface, (0,160,0), mid, ( mid[0] - direction[0] - norm[0], mid[1] - direction[1] - norm[1]) )
            pygame.draw.line(surface, (0,160,0), mid, ( mid[0] - direction[0] + norm[0], mid[1] - direction[1] + norm[1]) )
        
        yield 3
        if direction==(0,0):
            for p in self.bondedFrom:
                if p.ptype == self.ptype:
                    start = [int(i) for i in p.pos]
                    end   = [int(i) for i in self.pos]
                    direction = ( (end[0]-start[0]), (end[1]-start[1]) )
        
        i = PPostbox.labelangles[ nearest45DegreeStep(direction) ]
        surface.blit(self.label[i], ( int(self.pos[0]) + self.labelxo[i],
                                      int(self.pos[1]) + self.labelyo[i] )
                    )

                     
                     
                     
class AxonLaws(MultipleLaws):
    """Laws for axon components and postboxes
    """
    def __init__(self, postboxBondLength = 100):
        damp       = 1.0 - 0.8
        dampcutoff = 0.4
        maxvel     = 32
        
        forceScaler = 2.0
        
        component_component = SimpleLaws( bondLength        = postboxBondLength,
                                          maxRepelRadius    = 2.3 * postboxBondLength,
                                          repulsionStrength = 10.0 * forceScaler,
                                          maxBondForce      = 0.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        postbox_postbox     = SimpleLaws( bondLength        = postboxBondLength,
                                          maxRepelRadius    = _COMPONENT_RADIUS * 1.0,
                                          repulsionStrength = 0.25 * forceScaler,
                                          maxBondForce      = 10.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        component_postbox   = SimpleLaws( bondLength        = _COMPONENT_RADIUS,
                                          maxRepelRadius    = _COMPONENT_RADIUS,
                                          repulsionStrength = 0.0 * forceScaler,
                                          maxBondForce      = 10.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        typesToLaws = { ("component", "component") : component_component,
                        ("postbox",   "postbox")   : postbox_postbox,
                        ("component", "postbox")   : component_postbox,
                        ("postbox", "component")   : component_postbox    }
        
        super(AxonLaws, self).__init__( typesToLaws = typesToLaws )
        


        
class ExtraWindowFurniture(object):
   """Rendering for some extra 'furniture' for this 'axon/kamaelia' branded version
      of the TopologyViewer
   """
    def __init__(self):
        self.logo = pygame.image.load("kamaelia_logo.png")
        
        biggest = max( self.logo.get_width(), self.logo.get_height() )
        from pygame.transform import rotozoom
        self.logo = rotozoom(self.logo, 0.0, 64.0 / biggest)
        
    def render(self, surface):
        """Rendering generator, draws kamaelia logo. Awwww!"""
        yield 10
        surface.blit(self.logo, (0,0))

    
    
class AxonVisualiserServer(TopologyViewerServer):

    def __init__(self, **dictArgs):
        particleTypes = { "component" : PComponent,
                          "inbox"     : PPostbox,
                          "outbox"    : PPostbox
                        }
                        
        super(AxonVisualiserServer,self).__init__( particleTypes = particleTypes,
                                                   laws = AxonLaws(),
                                                   simCyclesPerRedraw = 5,
                                                   extraDrawing = ExtraWindowFurniture(),
                                                   **dictArgs
                                                 )


if __name__=="__main__":
    from Axon.Scheduler import scheduler as _scheduler

    a_little_test_script = """
add node 0 MyComponent1 randompos component
add node 1 CSA randompos component
add node i0 inbox randompos inbox
add node i1 inbox randompos inbox
add node o0 outbox randompos outbox
add node o1 outbox randompos outbox
add link 0 i0
add link 0 o0
add link 1 i1
add link 1 o1
add link i0 o1
add link i1 o0
del link i0 o1
add link i0 o1
del link i0 o1
add link i0 o1
add node 2 Fwibble randompos component
del node o1
add node o1
add link o1 1
add node o1 outbox randompos outbox
add link 1 o1
add node i2 inbox randompos inbox
add link 2 i2
add link i2 o1
add node c0 control randompos inbox
add node s0 signal randompos outbox
add link 0 c0
add link 0 s0
add node c1 control randompos inbox
add node s1 signal randompos outbox
add link 1 s1
add link 1 c1
add link s0 c1
add node c2 control randompos inbox
add link 2 c2
add link s1 c2
add node o2 outbox randompos outbox
add link 2 o2
add node s2 signal randompos outbox
add link 2 s2
add link s2 c0
add link i0 o2
add node 3 ABC randompos component
add node 3i inbox randompos inbo
add node 3i inbox randompos inbox
add link 3 3i
add link 3i o0
del link 3i o0
add node t outbox2 randompos outbox
add link 1 t
add link t i3
add link t 3i
"""    
    app = AxonVisualiserServer(caption="Axon / Kamaelia Visualiser")
    app.activate()
    _scheduler.run.runThreads(slowmo=0)
