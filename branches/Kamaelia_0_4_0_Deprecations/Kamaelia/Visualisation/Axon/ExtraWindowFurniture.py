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
==========================
Kamaelia Cat logo renderer
==========================

Renderer for the topology viewer framework that renders a Kamaelia cat logo
to the top left corner on rendering pass 10.



Example Usage
-------------
Create a topology viewer component that also renders 'ExtraWindowFurniture' to the
display surface::
   TopologyViewer( extraDrawing = ExtraWindowFurniture(),
                   ...
                 ).activate()

                          
How does it work?
-----------------
Instances of this class provide a render() generator that renders a Kamaelia cat
logo at coordinates (8,8) to the specified pygame surface. The cat logo is scaled
so its longest dimension (width or height) is 64 pixels.

Rendering is performed by the generator, returned when the render() method is
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

import pygame
from pygame.locals import *


class ExtraWindowFurniture(object):
    """\
    ExtraWindowFurniture() -> new ExtraWindowFurniture object.
    
    Renders a Kamaelia cat logo to the top left corner of a pygame surface
    when the render() generator is called.
    """
    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ExtraWindowFurniture,self).__init__()
        
        self.logo = pygame.image.load("kamaelia_logo.png")
        
        biggest = max( self.logo.get_width(), self.logo.get_height() )
        from pygame.transform import rotozoom
        self.logo = rotozoom(self.logo, 0.0, 64.0 / biggest)
        
    def render(self, surface):
        """\
        Generator that yields 10 then renders a Kamaelia cat logo to the 
        specified pygame surface at coordinates (8,8)
        """
        yield 10
        surface.blit(self.logo, (8,8))
        
    def setOffset( self, (x,y) ):
        """Dummy method."""
        pass
