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

import Kamaelia.Visualisation.PhysicsGraph
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer as _TopologyViewer

_TopologyViewerServer = Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer

from PComponent import PComponent
from IconComponent import IconComponent
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

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists

def AxonVisualiserServer(**dictArgs):
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
    particleTypes = { "component" : IconComponent,
                        "inbox"     : PPostbox.Inbox,
                        "outbox"    : PPostbox.Outbox
                    }
    return _TopologyViewerServer( particleTypes = particleTypes,
                                  laws = AxonLaws(),
                                  simCyclesPerRedraw = 3,
                                  extraDrawing = ExtraWindowFurniture(),
                                  **dictArgs
                                )
def text_to_token_lists():
    return Pipeline( chunks_to_lines(),
                     lines_to_tokenlists()
                   )

def AxonVisualiser( **dictArgs):
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
    #
    # Allow particleTypes to be overridden
    #
    args = dict(dictArgs)
    particleTypes = { "component" : IconComponent,
                      "inbox"     : PPostbox.Inbox,
                      "outbox"    : PPostbox.Outbox
                    }
#    particleTypes.update( (args.get("particleTypes",{})) )
    args["particleTypes"] = particleTypes
    args.pop("laws", None)
    return _TopologyViewer( laws = AxonLaws(),
                            simCyclesPerRedraw = 3,
                            extraDrawing = ExtraWindowFurniture(),
                            **args
                          )




__kamaelia_prefab__  = ( AxonVisualiserServer, AxonVisualiser)
