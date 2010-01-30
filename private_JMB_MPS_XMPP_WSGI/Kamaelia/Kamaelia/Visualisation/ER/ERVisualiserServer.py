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

from PEntity import PEntity
from PRelation import PRelation
from PISA import PISA
from PAttribute import PAttribute
from ERLaws import AxonLaws
from ExtraWindowFurniture import ExtraWindowFurniture
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists

def ERVisualiserServer(**dictArgs):
    """\
    - particleTypes
    - laws
    - simCyclesPerRedraw
    - extraWindowFurniture
    """
    particleTypes = { "entity" : PEntity,
                      "relation"     : PRelation.Relation,
                      "isa"     : PISA.Isa,
                      "attribute"     : PAttribute.Attribute,
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

def ERVisualiser( **dictArgs):
    """\
    - particleTypes
    - laws
    - simCyclesPerRedraw
    - extraWindowFurniture
    """
    #
    # Allow particleTypes to be overridden
    #
    args = dict(dictArgs)
    particleTypes = { "entity" : PEntity,
                      "relation"     : PRelation.Relation,
                      "isa"     : PISA.Isa,
                      "attribute"     : PAttribute.Attribute,
                    }
#    particleTypes.update( (args.get("particleTypes",{})) )
    args["particleTypes"] = particleTypes
    args.pop("laws", None)
    return _TopologyViewer( laws = AxonLaws(),
                            simCyclesPerRedraw = 3,
                            showGrid           = False,
                            extraDrawing = ExtraWindowFurniture(),
                            **args
                          )

__kamaelia_prefabs__  = ( ERVisualiserServer, ERVisualiser)
