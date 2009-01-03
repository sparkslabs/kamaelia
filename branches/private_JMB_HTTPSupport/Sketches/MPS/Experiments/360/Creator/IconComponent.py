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

import pygame

from Kamaelia.Visualisation.PhysicsGraph import BaseParticle
from pygame.locals import *

"""\
====================================================
"Component" particle for Axon/Kamaelia visualisation
====================================================

This is an implementation of a rendering particle for "Component" particles in
topology visualisation of Axon/Kamaelia systems.



Example Usage
-------------
See Kamaelia.Visualisation.Axon.AxonLaws or 
Kamaelia.Visualisation.Axon.AxonVisualiserServer



How does it work?
-----------------
This object subclasses Kamaelia.Physics.Simple.Particle and adds methods to 
support rendering. Specifically, rendering to represent a component in an 
Axon/Kamaelia system.

At initialisation, provide a unique ID, a starting (x,y) position tuple, and
a name. The name is displayed on the particle. If it is a dot-delimited string
then only the final term is displayed on the actual particle.

If the particle becomes selected, then it will render its full name at the top
of the display surface.

It also renders bonds *from* this particle *to* another. They are rendered as
simple grey lines.

Rendering is performed by a generator, returned when the render() method is 
called. Its behaviour is that needed for the framework for multi-pass rendering 
that is used by TopologyViewer.

The generator yields the number of the rendering pass it wishes to be next on
next. Each time it is subsequently called, it performs the rendering required
for that pass. It then yields the number of the next required pass or completes
if there is no more rendering required.

An setOffset() method is also implemented to allow the particles coordinates
to be offset. This therefore makes it possible to scroll the particles around
the display surface.

See TopologyViewer for more details.

"""


_COMPONENT_RADIUS = 32


def abbreviate(string):
    """Abbreviates dot-delimited string to the final (RHS) term"""
    return string.split(".")[-1]



class IconComponent(BaseParticle):
    """\
    IconComponent(ID,position,name, filename=None, image=None) -> new IconComponent object.
    
    Particle representing an Axon/Kamaelia Component for topology visualisation.
    
    Keyword arguments:
    
    - ID        -- a unique ID for this particle
    - position  -- (x,y) tuple of particle coordinates
    - name      -- The full dot-delimited pathname of the component being represented
    - filename  -- filename of an image to be loaded as display
    - image     -- pygame surface to use as the display
    """
    
    def __init__(self, ID, position, name, filename=None, image=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(IconComponent,self).__init__(position=position, ID = ID )
        self.set_label(name)
        self.ptype = "component"
        self.shortname = abbreviate(name)
        self.left = 0
        self.top = 0
        self.selected = False
        self.image = None
        
        self.radius = _COMPONENT_RADIUS*1.2
        if filename is None:
            import os, random
            assets = [ x for x in os.listdir("assets") if x[-4:] == ".gif" ]
            filename = "assets/"+assets[random.randint(0, len(assets)-1)]
  
        if filename is not None:
            self.image = pygame.image.load(filename)
            self.image = self.image.convert()
            print "size:", self.image.get_width(), self.image.get_height()
            print "largest:", max(self.image.get_width(), self.image.get_height())
            largest = max(self.image.get_width(), self.image.get_height())*1.0
            print "rescale:", largest/_COMPONENT_RADIUS
            from pygame.transform import rotozoom
            self.image = rotozoom(self.image, 0.0, ((_COMPONENT_RADIUS*2)/largest))
            self.imagexo = - self.image.get_width()/2
            self.imageyo = - self.image.get_height()/2
        
    def set_label(self, newname):
        self.name = newname
        self.shortname = abbreviate(newname)
        pygame.font.init()
        font = pygame.font.Font(None, 20)
        self.slabel   = font.render(self.shortname, True, (0,0,0))
        self.slabelxo = - self.slabel.get_width()/2
        self.slabelyo = - self.slabel.get_height()/2
        description = "Component "+self.shortname+" : "+self.name
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
        colour = (192,192,192)
        if self.selected:
            colour = (160,160,255)
        surface.blit(self.image, ( x+self.imagexo, y+self.imageyo ) )

        yield 3
        surface.blit(self.slabel, ( x+self.slabelxo, y-self.imageyo ) )
        if self.selected:
            yield 10
            pygame.draw.rect(surface, colour, (x+self.imagexo, y+self.imageyo, self.image.get_width(), self.image.get_height()),2)
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
        if self.selected:
            self.deselect()
        else:
            self.selected = True

    def deselect( self ):
        """Tell this particle it is deselected"""
        self.selected = False
