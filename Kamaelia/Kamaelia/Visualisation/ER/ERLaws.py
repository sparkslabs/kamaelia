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

import Kamaelia.Visualisation
from Kamaelia.Visualisation.PhysicsGraph import TopologyViewerServer, BaseParticle
from Kamaelia.Support.Particles import SimpleLaws, MultipleLaws

from pygame.locals import *

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
