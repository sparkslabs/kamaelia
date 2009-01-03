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

# physics code for forces between particles
#
# unbonded force acts between all non bonded particles
# bonded force acts between bonded particles

from SpatialIndexer import SpatialIndexer

from operator import sub as _sub
from operator import add as _add
from operator import mul as _mul

class MultipleLaws(object):
    """Laws framework for systems containing multiple particle types
    """
    def __init__(self, typesToLaws, defaultLaw = None):
        """Initialisation.
        typesToLaws = dictionary mapping particle type name pairs (type1, type2) to laws
        
        if you supply a pairing (t1, t2) it will also be applied to the case (t2,t1) without
        you needing to explicitly specify it. If you do, then your choice takes precedence.
        
        If you do not provide enough mappings to build a complete mapping from all types to all types,
        then the gaps will be automatically filled with mappings to defaultLaw.
        """
        
        self.laws = {}

        types = []
        
        # build specified mapping, reversing the pairings if not specified
        for ((type1, type2), law) in typesToLaws.items():
            self.laws[(type1,type2)] = law
            if not (type2,type1) in typesToLaws.keys():
                self.laws[(type2,type1)] = law
                
            # build a list of the different types of particles
            if not type1 in types:
                types.append(type1)
            if not type2 in types:
                types.append(type2)
        
        # go through the built links and check all combinations exist
        for type1 in types:
            for type2 in types:
                if not self.laws.has_key((type1, type2)):
                    self.laws[(type1,type2)] = defaultLaw
        
        # determine the maxInteractRadius        
        self.maxInteractRadius = max( [law.maxInteractRadius for law in self.laws.values()] )
        
        
    def particleMaxInteractRadius(self, ptype):
        return self.laws[(ptype,ptype)].maxInteractRadius
    
    
    def unbonded(self, ptype1, ptype2, dist, distSquared):
        law = self.laws[(ptype1, ptype2)]
        return law.unbonded(ptype1, ptype2, dist, distSquared)
    
    
    def bonded(self, ptype1, ptype2, dist, distSquared):
        law = self.laws[(ptype1, ptype2)]
        return law.bonded(ptype1, ptype2, dist, distSquared)
   
    def dampening(self, ptype, velocity):
        law = self.laws[(ptype, ptype)]
        return law.dampening(ptype, velocity)
