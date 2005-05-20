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


class ParticleSystem:
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
        while cycles > 0:
            cycles -= 1
            self.tick += 1
            for p in self.particles:
                p.doInteractions(self.indexer, self.laws, self.tick)
            for p in self.particles:
                p.update(self.laws)
        self.indexer.updateAll()



class Particle(object):
    """Particle within a physics system with an arbitrary number of dimensions.
    
    Represents a particle that interacts with other particles. One set of forces are applied for
    those particles that are unbonded. Interactions between bonded particles are controlled by another
    set of forces.
    
    Bonds are bi-directional. Establishing a bond from A to B, will also establish it back from B to A.
    Similarly, breaking the bond will do so in both directions too.
    """
    
    def __init__(self, position, initialTick = 0, ptype = None, velocity = None, ID = None):
        """Initialise particle.
           position    = tuple of coordinates
           initialTick = initial value for tick counter (should be same as for particle system)
           ptype       = particle type identifier
           velocity    = tuple of initial velocity vectors
           ID          = unique identifier
        """
        self.pos    = position
        self.tick   = initialTick
        self.static = False
        self.ptype  = ptype
        self.bondedTo   = []
        self.bondedFrom = []
        self.latestInteractWith = (None,None)
        
        if velocity != None:
            self.velocity = list(velocity)
        else:
            self.velocity = [ 0.0 for xx in self.pos ]
        if ID is None:
           self.ID = str(id(self))
        else:
           self.ID = ID
    
    def getBonded(self):
        """Return list of particles this one is bonded to (outgoing bonds)."""
        return self.bondedTo

    getBondedTo = getBonded
                
    def getBondedFrom(self):
        """Return list of particles that bond to this one (incoming bonds)."""
        return self.bondedFrom

    def makeBond(self,particles, index):
       """Make bond between this particle and another
       Specified by its index into the 'particles' entity you provide.
       
       If the bond already exists, then this method does nothing.
       """
       
       target = particles[index]
       if not target in self.bondedTo:
           self.bondedTo += [particles[index]]
           particles[index].bondedFrom += [self]
         
    def breakBond(self, particles, index):
        """Break bond between this particle and another
        Specified by its index into the 'particles' entity you provide.
        
        If the bond doesnt already exist, this method will fail.
        """
        self.bondedTo.remove( particles[index] )
        particles[index].bondedFrom.remove(self)
       
    def breakAllBonds(self, outgoing=True, incoming=True):
        """Breaks all bonds between this particle to others.
          Default behaviour is to break all bonds both from this node
          to others (outgoing) and from others to this (incoming).
          
          If outgoing or incoming are set to false, then bonds in those
          directions will not be broken
        """
        if outgoing:
            for bondTo in self.bondedTo:
                bondTo.bondedFrom.remove(self)
            self.bondedTo = []
            
        if incoming:
            for bondFrom in self.bondedFrom:
                bondFrom.bondedTo.remove(Self)
            self.bondedFrom = []
        
    def getLoc(self):
        """Return current possition"""
        return self.pos
        
        
    def freeze(self):
        """Lock the particle in place"""
        self.static = True
        
        
    def unFreeze(self):
        """Allow the particle to move freely"""
        self.static = False

        
    def distSquared(self, altpos):
        """Returns the distance squared of this particle from the specified position"""
        return sum(map(lambda x1,x2 : (x1-x2)*(x1-x2), self.pos, altpos))

    def doInteractions(self, particleIndex, laws, tick):
        """Apply laws in relation to this particle with respect to other particles,
        to update the velocity of this particle.
        
        particleIndex is an object with a withinRadius(centre, radius, filter) method that
        returns a list of (particles, distSquared) tuples, listing particles within that distance
        of the specified coordinates. The filter argument is a function that returns true if a
        given particle is to be included in the list.
        
        laws.maxInteractRadius is the max distance at which unbonded interactions are considered
        laws.unbonded(ptype, ptype, dist, distanceSquared) is the velocity change applied to both particles.
        +ve = attraction -ve = repulsion
        laws.bonded(dist, distanceSquared) is the same but for bonded particles
        
        Tick is the current tick counter value. Any particles this one encounters that already
        have reached 'tick' will not be interacted with since it will be assumed that
        that particle has already performed the interaction math.
        
        This code relies on any bonds being registered in both directions (a->b and b->a).
        If you override the bonding code in this class, then make sure you maintain this property.
        """
        self.tick = tick    

        # bonded interactions with bonded particles        
        bonded = self.getBondedTo() + self.getBondedFrom()
        for particle in bonded:
            if particle.tick != self.tick and particle.latestInteractWith != (self.tick, self):
                particle.latestInteractWith != (self.tick, self)
                ds = self.distSquared(particle.pos)
                if ds > 0.0:
                    dist = ds ** 0.5
                    dvelocity = laws.bonded(self.ptype, particle.ptype, dist, ds)
                    deltas = map(lambda x1,x2 : x2-x1, self.pos, particle.pos)
                    self.velocity     = map(lambda delta,v : v + (delta*dvelocity / dist), deltas, self.velocity)
                    particle.velocity = map(lambda delta,v : v - (delta*dvelocity / dist), deltas, particle.velocity)
                else:
                    pass # dunno, ought to have an error i guess

        # repulsion of other particles (not self, or those bonded to)
        filter = lambda particle : (particle.tick != self.tick) and not (particle in (bonded + [self]))

        particles = particleIndex.withinRadius(self.pos, laws.maxInteractRadius, filter)
        for (particle, ds) in particles:
            if ds > 0.0:
                dist = ds ** 0.5
                dvelocity   = laws.unbonded(self.ptype, particle.ptype, dist, ds)
                deltas = map(lambda x1,x2 : x2-x1, self.pos, particle.pos)
                self.velocity     = map(lambda delta,v : v+(+delta*dvelocity / dist), deltas, self.velocity)
                particle.velocity = map(lambda delta,v : v+(-delta*dvelocity / dist), deltas, particle.velocity)
            else:
                pass # dunno, ought to have an error i guess

    
    def update(self, laws):
        """Update this particle's position, also apply dampening to velocity
        
        laws.dampening( ptype, velocity ) should return the new velocity, that is then applied.
        """
        if self.static:
            self.velocity = [0 for x in self.velocity]
        else:
            self.velocity = laws.dampening(self.ptype, self.velocity)
            self.pos      = map(lambda pos,vel: pos+vel, self.pos, self.velocity)
            



class SimpleLaws:
    """Implements a simple set of physics laws for the particle system.
       repulsion force : force proportional to 1/distance_squared 
       bonds : force proportional to extension (Hook's law)
       
       All force strengths etc. are set up to vaguely sensible values on the basis of
       the specified bond length
    """
    def __init__(self, bondLength = 100):
        self.bondLength = bondLength

        scale = 100.0 / self.bondLength
        self.maxInteractRadius          = 200    /scale
        self.repulsionForceAtBondLength = 3.2    /scale
        self.maxBondForce               = 20.0   /scale
        self.damp                       = 0.8
        self.dampcutoff                 = 0.2*2  /scale
        self.maxVelocity                = 32     /scale

        
        self.bondForce         = self.maxBondForce / self.bondLength
        self.maxRepulsionForce = self.repulsionForceAtBondLength * self.bondLength**2
        
        
        
    def unbonded(self, ptype1, ptype2, dist, distSquared):
        """1/distance_squared unbonded repulsion force"""
        if distSquared < 1.0:
            return -self.maxRepulsionForce
        else:
            return -self.maxRepulsionForce / distSquared #* (self.particleRadius*self.particleRadius)

    
    def bonded(self, ptype1, ptype2, dist, distSquared):
        """proportional to extension bond force"""
        # note, its import that this retains its sign, so the direction of the force is determined
        f = self.bondForce * (dist - self.bondLength)
        if f < -self.maxBondForce:
            return -self.maxBondForce
        elif f > self.maxBondForce:
            return self.maxBondForce
        else:
            return f
    
    
    def dampening(self, ptype, velocity):
        """velocity dampening and minimal velocity (friction-like) cutoff"""
        vmag = reduce(lambda a,b:abs(a)+abs(b), velocity)
        if vmag < self.dampcutoff:
            return [0 for a in velocity]
        else:
            damp = self.damp
            if vmag > self.maxVelocity:
                damp = damp * self.maxVelocity / vmag
                
            return [ damp * v for v in velocity ]

