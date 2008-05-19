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
                bondFrom.bondedTo.remove(self)
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
        _bonded   = laws.bonded
        _unbonded = laws.unbonded
        __add, __sub, __mul = _add, _sub, _mul

        # bonded interactions with bonded particles        
        bonded = self.getBondedTo() + self.getBondedFrom()
        for particle in bonded:
            if particle.tick != self.tick and particle.latestInteractWith != (self.tick, self):
                particle.latestInteractWith != (self.tick, self)
                ds = self.distSquared(particle.pos)
                if ds > 0.0:
                    dist = ds ** 0.5
                    dvelocity = _bonded(self.ptype, particle.ptype, dist, ds)
                    deltas = map(__sub, particle.pos, self.pos)
                    dv_d = dvelocity / dist
                    scaleddeltas = map(__mul, deltas, [dv_d]*len(deltas))
                    self.velocity     = map(__add, self.velocity,     scaleddeltas)
                    particle.velocity = map(__sub, particle.velocity, scaleddeltas)
#                    self.velocity     = map(lambda delta,v : v + (delta*dv_d), deltas, self.velocity)
#                    particle.velocity = map(lambda delta,v : v - (delta*dv_d), deltas, particle.velocity)
                else:
                    pass # dunno, ought to have an error i guess

        # repulsion of other particles (not self, or those bonded to)
        filter = lambda particle : (particle.tick != self.tick) and not (particle in (bonded + [self]))

        particles = particleIndex.withinRadius(self.pos, laws.particleMaxInteractRadius(self.ptype), filter)
        for (particle, ds) in particles:
            if ds > 0.0:
                dist = ds ** 0.5
                dvelocity   = _unbonded(self.ptype, particle.ptype, dist, ds)
                deltas = map(__sub, particle.pos, self.pos)
                dv_d = dvelocity / dist
                scaleddeltas = map(__mul, deltas, [dv_d]*len(deltas))
                self.velocity     = map(__add, self.velocity,     scaleddeltas)
                particle.velocity = map(__sub, particle.velocity, scaleddeltas)
#                self.velocity     = map(lambda delta,v : v+(+delta*dv_d), deltas, self.velocity)
#                particle.velocity = map(lambda delta,v : v+(-delta*dv_d), deltas, particle.velocity)
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
            self.pos      = map(_add, self.pos, self.velocity)
