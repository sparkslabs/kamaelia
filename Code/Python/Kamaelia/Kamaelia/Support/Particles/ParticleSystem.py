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
"""\
=========================================
Discrete time particle physics simulation
=========================================

A discrete time simulator of a system of bonded and unbonded particles, of
multiple types.

The actual physics calculations are deferred to the particles themselves. You
can have as many, or few, spatial dimensions as you like.



Example Usage
-------------
Create 3 particles, two of which are bonded and move noticeably closer after 5
cycles of simulation::
    
    >>> laws = SimpleLaws(bondLength=5)
    >>> sim = ParticleSystem(laws)
    >>> sim.add( Particle(position=(10,10)) )
    >>> sim.add( Particle(position=(10,20)) )
    >>> sim.add( Particle(position=(30,40)) )
    >>> sim.particles[0].makeBond(sim.particles, 1)   # bond 1st and 2nd particles
    >>> for p in sim.particles: print p.getLoc()
    ...
    (10, 10)
    (10, 20)
    (30, 40)
    >>> sim.run(cycles=5)
    >>> for p in sim.particles: print p.getLoc()
    ...
    [10.0, 13.940067328]
    [10.0, 16.059932671999999]
    [30, 40]
    >>>



How does it work?
-----------------

Set up ParticleSystem by instantiating, specifying the laws to act between
particles and an (optional) set of initial particles.

Particles should be derived from the Particle base class (or have equivalent
functionality).

Particles can be added or removed from the system by reference, or removed by
their ID.

ParticleSystem will work for particles in space with any number of dimensions -
so long as all particles use the same!

Bonds between particles are up to the particles to manage for themselves.

The simulation runs in cycles when the run(...) method is called. Each cycle
advances the 'tick' count by 1. The tick count starts at zero, unless otherwise
specified during initialization.

The following attributes store the particles registered in ParticleSystem:
- particles     -- simple list
- particleDict  -- dictionary, indexed by particle.ID

ParticleSystem uses a SpatialIndexer object to speed up calculations.
SpatialIndexer reduce the search space when determining what particles lie
within a given region (radius of a point).

If your code changes the position of a particle, the simulator must be informed,
so it can update its spatial indexing data, by calling updateLoc(...)

The actual interactions between particles are calculated by the particles
themselves, *not* by ParticleSystem.
 
ParticleSystem calls the doInteractions(...) methods of all particles so they
can influence each other. It then calls the update(...) methods of all particles
so they can all update their positions and velocities ready for the next cycle.

This is a two stage process so that, in a given cycle, all particles see each
other at the same positions, irrespective of which particle's
doInteractions(...) method is called first. Particles should not apply their
velocities to update their position until their update(...) method is called.
"""

from .SpatialIndexer import SpatialIndexer


class ParticleSystem(object):
    """\
    ParticleSystem(laws[,initialParticles][,initialTick]) -> new ParticleSystem object

    Discrete time simulator for a system of particles.

    Keyword arguments:
    
    - initialParticles  -- list of particles (default=[])
    - initialTick       -- start value of the time 'tick' count (default=0)
    """

    def __init__(self, laws, initialParticles = [], initialTick = 0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
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
        """\
        Remove the specified particle(s) from the system.

        Note that this method does not destroy bonds from other particles to
        these ones.
        """
        for particle in oldParticles:
            self.particles.remove(particle)
            del self.particleDict[particle.ID]
        self.indexer.remove(*oldParticles)

        
    def removeByID(self, *ids):
        """\
        Remove particle(s) as specified by id(s) from the system.
        
        Note that this method does not destroy bonds from other particles to
        these ones.
        """
        particles = [self.particleDict[id] for id in ids]
        self.remove( *particles )
            
        
    def updateLoc(self, *particles):
        """\
        Notify this physics system that the specified particle(s)
        have changed position.
           
        Must be called if you change a particle's position,
        before calling run().
        """
        self.indexer.updateLoc(*particles)

        
    def withinRadius(self, centre, radius, filter=(lambda particle:True)):
        """\
        withinRadius(centre,radius[,filter]) -> list of (particle,distSquared)

        Returns a list of zero or more (particle,distSquared) tuples. The
        particles listed are those within the specified radius of the specified
        centre point, and that passed the (optional) filter function:

        filter(particle) -> True if the particle is to be included in the list
        """
        return self.indexer.withinRadius(centre, radius, filter)

            
    def run(self, cycles = 1):
        """Run the simulation for a given number of cycles (default=1)"""

        # optimisation to speed up access to these functions:
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
