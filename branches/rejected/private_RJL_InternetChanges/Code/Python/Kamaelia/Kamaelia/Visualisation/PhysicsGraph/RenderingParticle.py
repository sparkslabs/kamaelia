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

"""\
==================================================
Simple generic particle for Topology visualisation
==================================================

This is an implementation of a simple rendering particle for topology
visualisation.



Example Usage
-------------
A topology viewer where particles of type "-" are rendered by RenderingParticle
instances::
    TopologyViewerComponent( particleTypes = {"-":RenderingParticle},
                             laws = Kamaelia.Support.Particles.SimpleLaws(),
                           ).run()

SimpleLaws are used that apply the same simple physics laws for all particle
types.



How does it work?
-----------------
This object subclasses Kamaelia.Support.Particles.Particle and adds methods to
support rendering.

At initialisation, provide a unique ID, a starting (x,y) position tuple, and
a name. The name is displayed as a label ontop of the particle.

If the particle becomes selected it changes its visual appearance to reflect
this.

It also renders bonds *from* this particle *to* another. They are rendered as
simple lines.

Rendering is performed by a generator, returned when the render() method is
called. Its behaviour is that needed for the framework for multi-pass rendering
that is used by TopologyViewerComponent.

The generator yields the number of the rendering pass it wishes to be next on
next. Each time it is subsequently called, it performs the rendering required
for that pass. It then yields the number of the next required pass or completes
if there is no more rendering required.

An setOffset() method is also implemented to allow the particles coordinates
to be offset. This therefore makes it possible to scroll the particles around
the display surface.

See TopologyViewerComponent for more details.

"""

import pygame
from Kamaelia.Support.Particles import Particle as BaseParticle

class RenderingParticle(BaseParticle):
    """\
    RenderingParticle(ID,position,name) -> new RenderingParticle object.
    
    Simple generic particle for topology visualisation.
    
    Keyword arguments:
    - ID        -- a unique ID for this particle
    - position  -- (x,y) tuple of particle coordinates
    - name      -- A name this particle will be labelled with
    """

    def __init__(self, ID, position, name):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(RenderingParticle,self).__init__(position=position, ID = ID )
        self.radius = 20
        self.labelText = None
        self.label = None
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

        self.set_label(name)
        self.name = name
        
        self.left = 0
        self.top  = 0
        self.selected = False

    def set_label(self, labelText):
        self.labelText = labelText
        self.label = self.font.render(self.labelText, False, (0,0,0))
        self.name = labelText
    
       
    def render(self, surface):
        """\
        Multi-pass rendering generator.

        Renders this particle in multiple passes to the specified pygame surface -
        yielding the number of the next pass to be called on between each. Completes
        once it is fully rendered.
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
        """\
        Set the offset of the top left corner of the rendering area.

        If this particle is at (px,py) it will be rendered at (px-x,py-y).
        """
        self.left = left
        self.top  = top

        
    def select( self ):
        """Tell this particle it is selected"""
        self.selected = True

    def deselect( self ):
        """Tell this particle it is deselected"""
        self.selected = False
