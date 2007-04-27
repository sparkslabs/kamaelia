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

import Kamaelia.Visualisation.PhysicsGraph

_TopologyViewerServer = Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer

from PComponent import PComponent
from PPostbox import PPostbox
from AxonLaws import AxonLaws
from ExtraWindowFurniture import ExtraWindowFurniture

"""\
----------------------------------
Axon/Kamaelia Visualisation Server
----------------------------------

A specialisation of TopologyViewerServer for visualising Axon/Kamaelia systems.



Example Usage
-------------
Visualiser that listens on its default port for a TCP connection through which
it receives Introspection topology data to render::
    AxonVisualiserServer().run()



How does it work?
-----------------
AxonVisualiserServer is a subclass of TopologyViewerServer, where the following
are already specified:
- types of particles
- their laws of interaction
- the number of simulation cycles per redraw
- extra window furniture

The remaining keyword arguments of the TopologyviewerServer component can all
be specified when initialising AxonVisualiserServer.

The particles used are:
- Kamaelia.Visualisation.Axon.PComponent
- Kamaelia.Visualisation.Axon.PPostbox

The laws used are Kamaelia.Visualisation.Axon.AxonLaws.

The extra window furniture is supplied by 
Kamaelia.Visualisation.Axon.ExtraWindowFurniture.
"""


class AxonVisualiserServer(_TopologyViewerServer):
    """\
    AxonVisualiserServer(...) -> new AxonVisualiserServer component.
    
    A specialisation of the TopologyViewerServer component for viewing
    Axon/Kamaelia systems.
    
    Keyword arguments are those for TopologyViewerServer, excluding:
    - particleTypes
    - laws
    - simCyclesPerRedraw
    - extraWindowFurniture
    """

    def __init__(self, **dictArgs):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        particleTypes = { "component" : PComponent,
                          "inbox"     : PPostbox.Inbox,
                          "outbox"    : PPostbox.Outbox
                        }
                        
        super(AxonVisualiserServer,self).__init__( particleTypes = particleTypes,
                                                   laws = AxonLaws(),
                                                   simCyclesPerRedraw = 3,
                                                   extraDrawing = ExtraWindowFurniture(),
                                                   **dictArgs
                                                 )
__kamaelia_components__  = ( AxonVisualiserServer, )
