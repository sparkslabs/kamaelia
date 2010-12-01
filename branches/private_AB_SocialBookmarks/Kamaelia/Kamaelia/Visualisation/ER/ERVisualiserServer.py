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
