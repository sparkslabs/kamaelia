#!/usr/bin/python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# Simple control window for a looping audio player

import pygame

from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Visualisation.Axon.AxonVisualiserServer import AxonVisualiser
from Kamaelia.Support.Particles import SimpleLaws, Particle
from Kamaelia.Visualisation.Axon.ExtraWindowFurniture import ExtraWindowFurniture

import time

#
# FIXME: How does this relate to the normal particle?
#
class ComponentParticle(Particle):
    """Version of Physics.Particle designed to represent components in a simple pipeline"""

    def __init__(self, ID, position, name):
        super(ComponentParticle,self).__init__(position=position, ID = ID )
        self.radius = 20
        self.labelText = name   # strip up to the first pipe only
        self.name = name

        pygame.font.init()
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
        sx = int(self.pos[0]) - self.left
        sy = int(self.pos[1]) - self.top

        yield 1
        phase = (time.time()*4) % 2.0
        off = phase > 1.0
        phase = phase % 1.0
        for p in self.bondedTo:

            ex = int(p.pos[0] -self.left)
            ey = int(p.pos[1] - self.top)

            # 'make a crawling dotted line' appearance, to give an animated indication
            # directionality of the link
            dx = ex-sx
            dy = ey-sy
            length = (dx*dx + dy*dy)**0.5
            dx = dx/length
            dy = dy/length

            p=0
            while p<length:
                newp = min(length, p+ phase * 10.0 )
                phase = 1.0
                
                if not off:
                    pygame.draw.line( surface,
                                      (128,128,255),
                                      (sx+dx*p,sy+dy*p),
                                      (sx+dx*newp,sy+dy*newp)
                                    )
                off = not off
                p=newp

        
        yield 2

        if self.selected:
            pygame.draw.circle(surface, (255,255,128), (sx,sy), self.radius)
        else:
            pygame.draw.circle(surface, (192,192,192), (sx,sy), self.radius)

        surface.blit(self.label, (sx - self.label.get_width()/2, sy - self.label.get_height()/2))


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

def BuildViewer(screensize = (800,600), fullscreen = False, transparency = None):
    laws = SimpleLaws(bondLength=100)
    return AxonVisualiser( screensize=screensize,
                           fullscreen=fullscreen,
                           caption = "The pipeline",
                           particleTypes = {"component":ComponentParticle},
#                           extraDrawing = ExtraWindowFurniture(),
                            laws = laws
                         )
