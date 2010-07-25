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
