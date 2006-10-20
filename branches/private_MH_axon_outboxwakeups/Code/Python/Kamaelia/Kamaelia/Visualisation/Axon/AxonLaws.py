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

import Kamaelia.Visualisation
from Kamaelia.Visualisation.PhysicsGraph import TopologyViewerServer, BaseParticle
from Kamaelia.Support.Particles import SimpleLaws, MultipleLaws

from pygame.locals import *

"""\
====================================
Particle Laws for Axon Visualisation
====================================

This class is a specialisation of Kamaelia.Physics.Simple.MultipleLaws that
specifies the laws for particle interactions when visualising Axon/Kamaelia
systems.



Example Usage
-------------
Instantiate a topology viewer using rendering code for each particle type, and the
appropriate laws to govern their interactions::
    visualiser = TopologyViewer( particleTypes={ "component" : PComponent,
                                                 "inbox"     : PPostbox.Inbox,
                                                 "outbox"    : PPostbox.Outbox
                                               },
                                 laws = AxonLaws(),
                               ).activate()



How does it work?
-----------------

AxonLaws is a subclass of MultipleLaws. It sets the bond lengths and strengths 
of forces for two types of particles that represent components and 
inboxes/outboxes respectively. 

These laws are mapped to work for particles identified as being of type
"component" and "postbox".

At initialisation you can specify the length of the postbox to postbox bond
(which represents Axon linkages). The ranges over which forces act (but not their
magnitude) are scaled appropriately.

See MultipleLaws for information on the role of this class for physics
simulation and topology visualisation.
"""

_COMPONENT_RADIUS = 32    

class AxonLaws(MultipleLaws):
    """\
    AxonLaws([postboxBondLength]) -> new AxonLaws object.
    
    Encapsulates laws for interactions between particles of types "Component"
    and "Postbox" in a physics simulation. Subclass of MultipleLaws.
    
    Keyword arguments:
    
    - postboxBondLength  -- length of bond that represents Axon linkages (default=100)
    """
    
    def __init__(self, postboxBondLength = 100):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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
        component_postbox   = SimpleLaws( bondLength        = _COMPONENT_RADIUS*1.5,
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
