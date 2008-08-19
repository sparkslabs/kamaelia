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
"""\
============================================
Particle Physics Laws for multiple particles
============================================

A class implementing laws for interactions between multiple particle types,  in
discrete time simulations. Can be used with the physics ParticleSystem class.
This implementation supports different parameters for interactions between
different particle types.

You specify a mapping between pairs of types of particles and the set of laws
to apply between them.

This class provides the same methods as the SimpleLaws class. It is a drop in
replacement for when you wish to specialise a physics model to apply different
laws depending on the types of particles involved.



Example Usage
-------------

For two types of particle "Entity" and "Attribute":
- Entities only repel each other
- Attributes bond at a distance of 200 units
- Attributes bond to entities at a distance of 50 units
::

    mapping = { ("Entity","Entity") :SimpleLaws(maxBondForce=0, repulsionStrength=10),
                ("Attribute","Attribute") : SimpleLaws(bondLength=200),
                ("Entity","Attribute") : SimpleLaws(bondLength=50),
              }
        
    laws = MultipleLaws( typesToLaws=mapping,
                       )



How does it work?
-----------------

It provides the same method interface as the SimpleLaws class, but applies
different sets of laws depending on the particle types passed when methods are
called (SimpleLaws always applies the same rules irrespective).

The different laws provided are stored with the specified mappings.
If you specify a mapping for (typeA,typeB), then it will also be applied to
(typeB,typeA). You do not need to specify the mappings both ways round, though
you may if you wish.

If you do not specify the complete set of mappings for the particle types to
all of each other, then a default law (if specified) will be used to fill in
the gaps.

Note that the default law does not get applied to particle types not mentioned
when in the mappings you provide. For example, if your mappings only cover
particle types 'A','B', and 'C', then interactions involving a new type 'D' will
cause an exception to be raised.

The 'maximum interaction radius' for a given particle type is set to the maximum
of the interaction radii for all the different interaction laws it is involved
in.
"""



from SpatialIndexer import SpatialIndexer

from operator import sub as _sub
from operator import add as _add
from operator import mul as _mul

class MultipleLaws(object):
    """\
    MultipleLaws(typesToLaws[,defaultLaw]) -> new MultipleLaws object

    Computes forces between specified particle types at specified separation
    distances. Different forces are applied depending on whether they are
    bonded or unbonded and depending on the types of particle interacting.

    Keyword arguments:
    
    - typesToLaws  -- dictionary mapping pairs of particle type names (A,B) to object that will compute the laws acting between them
    - defaultLaw   -- law object applied to pairings missing from the mapping
    """
    def __init__(self, typesToLaws, defaultLaw = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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
        """Returns the maximum distance interactions will occur at for the specified particle type."""
        return self.laws[(ptype,ptype)].maxInteractRadius
    
    
    def unbonded(self, ptype1, ptype2, dist, distSquared):
        """\
        unbonded(ptype1,ptype2,dist,distSquared) -> amount of force between unbonded particles

        Returns the force between two unbonded particles of the specified types.
        Positive values are attraction, negative values are repulsion.

        dist and distSquared should both be specified since you've probably
        already calculated them. (This is an efficiency optimisation)
        """
        law = self.laws[(ptype1, ptype2)]
        return law.unbonded(ptype1, ptype2, dist, distSquared)
    
    
    def bonded(self, ptype1, ptype2, dist, distSquared):
        """\
        bonded(ptype1,ptype2,dist,distSquared) -> amount of force between bonded particles

        Returns the force between two bonded particles of the specified types.
        Positive values are attraction, negative values are repulsion.

        dist and distSquared should both be specified since you've probably
        already calculated them. (This is an efficiency optimisation)
        """
        law = self.laws[(ptype1, ptype2)]
        return law.bonded(ptype1, ptype2, dist, distSquared)
   
    def dampening(self, ptype, velocity):
        """\
        dampening(ptype, velocity) -> damped velocity vector

        Returned the dampened (reduced) velocity vector, for the specified particle
        type.

        velocity is a tuple/list of the vector components comprising the velocity.
        """
        law = self.laws[(ptype, ptype)]
        return law.dampening(ptype, velocity)
