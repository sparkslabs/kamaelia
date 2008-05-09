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
"""\
============================
Simple Particle Physics Laws
============================

A class implementing laws for interactions between particles in discrete time
simulations. Can be used with the physics ParticleSystem class.
Laws are based on the inverse square law.

Different laws are applied for 'bonded' and 'unbonded' particles. Unbonded
particles repel. Repulsion and attraction forces balance for bonded particles at
a specified "bond length".

There are a range of parameters that can be set at initialisation. All have
sensible defaults.



Example usage
-------------

Laws for particles that bond at a distance of 200 units::

    >>> laws = SimpleLaws(bondLength=200)
    >>> laws.bonded("","", 200, 200**2)
    0.0
    >>> laws.bonded("","", 210, 210**2)
    2.0
    >>> laws.bonded("","", 195, 195**2)
    1.0

Laws for particles that decelerate *fast*::

    >>> laws = SimpleLaws(damp=0.5)
    >>> velocity = [10.0, 5.0]
    >>> laws.dampening("", velocity)
    [5.0, 2.5]

Laws for particles that don't repel much but bond extra strongly::

    >>> laws = SimpleLaws(repulsionStrength = 1.0, maxBondForce = 40.0)
    >>> laws.unbonded("","", 50, 50**2)
    -4.0
    >>> laws.bonded("","", 50, 50**2)
    -20.0



The physics model used
----------------------
    
Instances of this class provide methods for calculating the force that acts
between a pair of particles when bonded or unbonded. It can also calculate any
reduction in velocity due to 'friction'.

Repulsion forces are calculated using the inverse square law
(1 / distance squared).

Bonding attraction and repulsion forces are calculated using Hook's law for
springs. However a cut-off is applied so the force is never greater than when
the bond is stretched to twice its resting length.

There are also other cut-offs (described below) to help prevent a simulation
becoming unstable, and to help speed up simulation.



How does it work?
-----------------

You specify arguments to control the strengths of bonding and repulsion
(unbonded) forces and the distances they act over.

You can also specify friction and cutoffs for maximum and minimum velocities.
These latter arguments are 'fudge factors' that you can use to help stop a
system spiralling out of control. Note that in a discrete time simulation,
if particle velocities/accelerations are too great the simulation can become
unstable and particles will fly everywhere!

You may also specify a 'maximum interaction radius' - the distance at which,
for unbonded particles, a simulator need not bother calculating the forces
acting (because they are too small to worry about). This is to allow simulators
to run faster by reducing the number of calculations performed per cycle.

For unspecified arguments, their defaults are scaled appropriately for
the bondLength you specify, such that behaviour will appear unchanged, just
at a different scaling.
"""

from SpatialIndexer import SpatialIndexer

from operator import sub as _sub
from operator import add as _add
from operator import mul as _mul

class SimpleLaws(object):
    """\
    SimpleLaws([bondlength][,maxRepelRadius][,repulsionStrength][,maxBondForce]
               [,damp][,dampcutoff][,maxVelocity]) -> new SimpleLaws object

    Computes forces between particle at specified separation distances.
    Different forces are applied depending on whether they are bonded or unbonded.
    The same forces are applied irrespective of particle type.

    Keyword arguments:
    
    - bondLength         -- Length of stable bonds between particles (default=100)
    - maxRepelRadius     -- Maximum distance repulsion force acts at (default=200)
    - repulsionStrength  -- Strength of repulsion of unbonded particles at bondLength separation (default=3.2)
    - maxBondForce       -- Max force applied by bond at 0 or 2*bondLength separation (default=20.0)
    - damp               -- amount of friction 0.0 = none, 1.0 = no movement possible (default=0.8)
    - dampcutoff         -- velocity set to zero if below this value (default=0.4)
    - maxVelocity        -- maximum allowed velocity for particles (default=32)

    For unspecified arguments, their defaults are scaled appropriately for
    the bondLength you specify, such that behaviour will appear unchanged, just
    at a different scaling.
    """
    def __init__(self, bondLength        = 100,
                       maxRepelRadius    = None,
                       repulsionStrength = None,
                       maxBondForce      = None,
                       damp              = None,
                       dampcutoff        = None,
                       maxVelocity       = None
                 ):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.bondLength = bondLength

        scale = 100.0 / self.bondLength
        
        def defaultIfNone(value, default):
            if value == None:
                return default
            else:
                return value
        
        self.maxInteractRadius          = defaultIfNone(maxRepelRadius,    200  / scale)
        self.repulsionForceAtBondLength = defaultIfNone(repulsionStrength, 3.2  / scale)
        self.maxBondForce               = defaultIfNone(maxBondForce,      20.0 / scale)
        self.damp                       = 1.0 - defaultIfNone(damp, 0.2)
        self.dampcutoff                 = defaultIfNone(dampcutoff,        0.4  / scale)
        self.maxVelocity                = defaultIfNone(maxVelocity,       32   / scale)
        
        self.bondForce         = self.maxBondForce / self.bondLength
        self.maxRepulsionForce = self.repulsionForceAtBondLength * self.bondLength**2
        
    def particleMaxInteractRadius(self, ptype):
        """Returns the maximum distance interactions will occur. ptype is ignored."""
        return self.maxInteractRadius
        
    def unbonded(self, ptype1, ptype2, dist, distSquared):
        """\
        unbonded(ptype1,ptype2,dist,distSquared) -> amount of force between unbonded particles

        Returns the force between two unbonded particles (types are ignored)
        Positive values are attraction, negative values are repulsion.

        dist and distSquared should both be specified since you've probably
        already calculated them. (This is an efficiency optimisation)
        """
        if distSquared < 1.0:
            return -self.maxRepulsionForce
        else:
            return -self.maxRepulsionForce / distSquared #* (self.particleRadius*self.particleRadius)

    
    def bonded(self, ptype1, ptype2, dist, distSquared):
        """\
        bonded(ptype1,ptype2,dist,distSquared) -> amount of force between bonded particles

        Returns the force between two bonded particles (types are ignored)
        Positive values are attraction, negative values are repulsion.

        dist and distSquared should both be specified since you've probably
        already calculated them. (This is an efficiency optimisation)
        """
        # note, its import that this retains its sign, so the direction of the force is determined
        f = self.bondForce * (dist - self.bondLength)
        if f < -self.maxBondForce:
            return -self.maxBondForce
        elif f > self.maxBondForce:
            return self.maxBondForce
        else:
            return f
    
    
    def dampening(self, ptype, velocity):
        """\
        dampening(ptype, velocity) -> damped velocity vector

        Returned the dampened (reduced) velocity vector. (ptype is ignored)

        velocity is a tuple/list of the vector components comprising the velocity.
        """
        vmag = reduce(lambda a,b:abs(a)+abs(b), velocity)
        if vmag < self.dampcutoff:
            return [0] * len(velocity) #[0 for a in velocity]
        else:
            damp = self.damp
            if damp * vmag > self.maxVelocity:
                damp = self.maxVelocity / vmag
                
            return map(_mul, velocity, [damp] * len(velocity) )

