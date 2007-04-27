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
=============
Grid Renderer
=============

Renderer for the topology viewer framework that renders horizontal and vertical
gridlines on pass -1.



Example Usage
-------------
Already used by Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent.

Rendering a grid in light grey with grid cell size of 100x100::
    grid = GridRenderer(size=100, colour=(200,200,200))
    renderer = grid.render( <pygame surface> )
    for rendering_pass in renderer:
      print "Rendering for pass ", rendering_pass



How does it work?
-----------------
Instances of this class provide a render() generator that renders horizontal
and vertical grid lines to conver the specified pygame surface. The colour and
spacing of the grid lines are specified at initialisation.

Rendering is performed by the generator, returned when the render() method is
called. Its behaviour is that needed for the framework for multi-pass rendering
that is used by TopologyViewerComponent.

The generator yields the number of the rendering pass it wishes to be next on
next. Each time it is subsequently called, it performs the rendering required
for that pass. It then yields the number of the next required pass or completes
if there is no more rendering required.

A setOffset() method is also implemented to allow the rendering position to be
offset. This therefore makes it possible to scroll the grid around the display
surface.

See TopologyViewerComponent for more details.

"""

import pygame

class GridRenderer(object):
    """\
    GridRenderer(size,colour) -> new GridRenderer object.
    
    Renders a grid of horizontal and vertical lines with the specified grid
    square size and colour to cover a pygame surface when the render()
    generator is called.
    """

    def __init__(self, size, colour):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(GridRenderer,self).__init__()
        self.gridSize = int(size)
        self.colour   = colour
        self.left     = 0
        self.top      = 0


    def render(self, surface):
        """\
        Multi-pass rendering generator.

        Renders this particle in multiple passes to the specified pygame surface -
        yielding the number of the next pass to be called on between each. Completes
        once it is fully rendered.
        """
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
        """\
        Set the offset of the top left corner of the rendering area.

        What would be rendered at (px,py) it will be rendered at (px-x,py-y).
        """
        self.left = left
        self.top  = top
