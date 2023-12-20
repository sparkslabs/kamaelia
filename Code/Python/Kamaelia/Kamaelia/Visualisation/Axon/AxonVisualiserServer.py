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

import Kamaelia.Visualisation.PhysicsGraph
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer as _TopologyViewer
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer import TopologyViewerServer as _TopologyViewerServer

from .PComponent import PComponent
from .PPostbox import PPostbox
from .AxonLaws import AxonLaws
from .ExtraWindowFurniture import ExtraWindowFurniture

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
    particleTypes = { "component" : PComponent,
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
    particleTypes = { "component" : PComponent,
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




__kamaelia_prefabs__  = ( AxonVisualiserServer, AxonVisualiser)
