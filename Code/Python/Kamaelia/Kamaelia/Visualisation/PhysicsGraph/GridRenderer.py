#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------

# Checked: 2024/03/24

"""\
=============
Grid Renderer
=============

Renderer for the topology viewer framework that renders horizontal and vertical
gridlines on pass -1.



Example Usage
-------------

Already used by Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.

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
that is used by TopologyViewer.

The generator yields the number of the rendering pass it wishes to be next on
next. Each time it is subsequently called, it performs the rendering required
for that pass. It then yields the number of the next required pass or completes
if there is no more rendering required.

A setOffset() method is also implemented to allow the rendering position to be
offset. This therefore makes it possible to scroll the grid around the display
surface.

See TopologyViewer for more details.

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
        for i in range(int((self.top // self.gridSize) * self.gridSize - self.top),
                       int(surface.get_height()),
                       int(self.gridSize)):
            pygame.draw.line(surface, self.colour,
                             (0,i),
                             (surface.get_width(),i) )


        for i in range( int((self.left // self.gridSize) * self.gridSize - self.left),
                        int(surface.get_width()), 
                        int(self.gridSize)):
            pygame.draw.line(surface, self.colour, 
                             (i, 0                   ), 
                             (i, surface.get_height()) )

    def setOffset( self, offset ):
        """\
        Set the offset of the top left corner of the rendering area.

        What would be rendered at (px,py) it will be rendered at (px-x,py-y).
        """
        left,top = offset
        self.left = left
        self.top  = top
