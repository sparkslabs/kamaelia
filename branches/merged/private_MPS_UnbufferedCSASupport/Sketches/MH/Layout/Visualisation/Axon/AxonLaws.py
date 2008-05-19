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

import Visualisation
from Visualisation.Graph import TopologyViewerServer, BaseParticle
from Physics import SimpleLaws, MultipleLaws

from pygame.locals import *


_COMPONENT_RADIUS = 32    

class AxonLaws(MultipleLaws):
    """Laws for axon components and postboxes
    """
    def __init__(self, postboxBondLength = 100):
        damp       = 1.0 - 0.8
        dampcutoff = 0.4
        maxvel     = 32
        
        forceScaler = 1.0
        
        component_component = SimpleLaws( bondLength        = postboxBondLength,
                                          maxRepelRadius    = 2.3 * postboxBondLength,
                                          repulsionStrength = 10.0 * forceScaler,
                                          maxBondForce      = 0.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        postbox_postbox     = SimpleLaws( bondLength        = postboxBondLength,
                                          maxRepelRadius    = _COMPONENT_RADIUS * 1.0,
                                          repulsionStrength = 0.05 * forceScaler,
                                          maxBondForce      = 5.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        component_postbox   = SimpleLaws( bondLength        = _COMPONENT_RADIUS*1.2,
                                          maxRepelRadius    = _COMPONENT_RADIUS,
                                          repulsionStrength = 0.0 * forceScaler,
                                          maxBondForce      = 10.0 * forceScaler,
                                          damp              = damp,
                                          dampcutoff        = dampcutoff,
                                          maxVelocity       = maxvel
                                        )
        typesToLaws = { ("component", "component") : component_component,
                        ("postbox",   "postbox")   : postbox_postbox,
                        ("component", "postbox")   : component_postbox,
                        ("postbox",   "component") : component_postbox    }
        
        super(AxonLaws, self).__init__( typesToLaws = typesToLaws )
