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

import Kamaelia.Visualisation
from Kamaelia.Visualisation.PhysicsGraph import TopologyViewerServer, BaseParticle
from Kamaelia.Support.Particles import SimpleLaws, MultipleLaws

_COMPONENT_RADIUS = 32    

class AxonLaws(MultipleLaws):

    def __init__(self, relationBondLength = 100):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        damp       = 1.0 - 0.8
        dampcutoff = 0.4
        maxvel     = 32

        forceScaler = 1.0

        entity_entity = SimpleLaws( bondLength        = relationBondLength,
                                          maxRepelRadius    = 2.3 * relationBondLength,
                                          repulsionStrength = 10.0 * forceScaler,
                                          maxBondForce      = 0.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )

        relation_relation     = SimpleLaws( bondLength        = relationBondLength,
                                          maxRepelRadius    = _COMPONENT_RADIUS * 2.0,
                                          repulsionStrength = 1 * forceScaler,
                                          maxBondForce      = 3.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        entity_attribute   = SimpleLaws( bondLength        = _COMPONENT_RADIUS*2,
                                          maxRepelRadius    = _COMPONENT_RADIUS*2,
                                          repulsionStrength = 2.0 * forceScaler,
                                          maxBondForce      = 10.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        entity_relation   = SimpleLaws( bondLength        = _COMPONENT_RADIUS*3,
                                          maxRepelRadius    = _COMPONENT_RADIUS*3,
                                          repulsionStrength = 2.0 * forceScaler,
                                          maxBondForce      = 10.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )

        typesToLaws = { ("entity", "entity") : entity_entity,
                        ("relation",   "relation")   : relation_relation,
                        ("isa",   "relation")   : relation_relation,
                        ("relation",   "isa")   : relation_relation,
                        ("isa",   "isa")   : relation_relation,
                        ("entity", "relation")   : entity_relation,
                        ("entity", "isa")   : entity_relation,
                        ("relation",   "entity") : entity_relation,
                        ("isa",   "entity") : entity_relation,
                        ("entity", "attribute")   : entity_attribute,
                      }

        super(AxonLaws, self).__init__( typesToLaws = typesToLaws,defaultLaw = entity_relation )
