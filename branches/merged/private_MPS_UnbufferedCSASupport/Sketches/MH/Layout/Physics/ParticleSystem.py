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

# physics code for forces between particles
#
# unbonded force acts between all non bonded particles
# bonded force acts between bonded particles

from SpatialIndexer import SpatialIndexer

from operator import sub as _sub
from operator import add as _add
from operator import mul as _mul

class ParticleSystem(object):
    """System of particles.
    
    Maintains the set of particles and runs the physics simulation over them
    the specified laws.
    """

    def __init__(self, laws, initialParticles = [], initialTick = 0):
        """Initialise the particle system.
           laws             = laws object
           initialParticles = list of particles
           initialTick      = start value for tick counter
        """
        self.indexer = SpatialIndexer(laws.maxInteractRadius)
        
        self.laws         = laws
        self.particles    = []
        self.tick         = initialTick
        self.particleDict = {}
        self.add(*initialParticles)
    
    def add(self, *newParticles):
        """Add the specified particle(s) into the system"""
        self.particles.extend(newParticles)
        for p in newParticles:
           self.particleDict[p.ID] = p
        self.indexer.updateLoc(*newParticles)

        
    def remove(self, *oldParticles):
        """Remove the specified particle(s) from the system.
           Note that this method does not destroy bonds from other particles to these ones.
        """
        for particle in oldParticles:
            self.particles.remove(particle)
            del self.particleDict[particle.ID]
        self.indexer.remove(*oldParticles)

    def removeByID(self, *ids):
        """Remove particle(s) as specified by id(s) from the system.
           Note that this method does not destroy bonds from other particles to these ones.
        """
        particles = [self.particleDict[id] for id in ids]
        self.remove( *particles )
            
        
    def updateLoc(self, *particles):
        """Notify this physics system that the specified particle(s)
           have changed position.
           
           Must be called if you change a particle's position,
           before calling run().
        """
        self.indexer.updateLoc(*particles)

    def withinRadius(self, centre, radius, filter=(lambda particle:True)):
        """Returns a list of zero or more (particle, distSquared) tuples,
           representing those particles within radius distance of the
           specified centre coords.

           distance-squared from the centre coords is returned too to negate
           any need you may have to calculate it again yourself.

           You can specify a filter function that takes a candidate particle
           as an argument and should return True if it is to be included
           (if it is within the radius, of course). This is to allow efficient
           pre-filtering of the particles before the distance test is done.
        """
        return self.indexer.withinRadius(centre, radius, filter)
        
    def run(self, cycles = 1):
        """Run the simulation for a given number of cycles"""
        _indexer = self.indexer
        _laws    = self.laws
        while cycles > 0:
            cycles -= 1
            self.tick += 1
            _tick = self.tick
            for p in self.particles:
                p.doInteractions(_indexer, _laws, _tick)
            for p in self.particles:
                p.update(_laws)
        _indexer.updateAll()
