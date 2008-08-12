#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===========================================================================================================
Discrete time particle physics simulation with the support of some particles not subject to physics laws
===========================================================================================================

A discrete time simulator of a system of bonded and unbonded particles, of
multiple types.

The actual physics calculations are deferred to the particles themselves. You
can have as many, or few, spatial dimensions as you like.

This object extends ParticleSystem with the support of some particles 
not subject to physics laws. Otherwise, it is the same with 
Kamaelia.Support.Particles.ParticleSystem.ParticleSystem. See 
ParticleSystem for more information.



References: Kamaelia.Support.Particles.ParticleSystem.ParticleSystem
"""

from Kamaelia.Support.Particles.ParticleSystem import ParticleSystem

class ParticleSystemX(ParticleSystem):
    """\
    ParticleSystemX(laws[,initialParticles][,initialTick]) -> new ParticleSystem object

    Discrete time simulator for a system of particles.

    Keyword arguments:
    
    - initialParticles  -- list of particles (default=[])
    - initialTick       -- start value of the time 'tick' count (default=0)
    """
    
    def __init__(self, laws, initialParticles = [], initialTick = 0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ParticleSystemX, self).__init__(laws=laws, initialParticles = [], initialTick = 0)
    
    def run(self, cycles = 1, avoidedList=[]):
        """\
        Run the simulation for a given number of cycles (default=1);
        use avoidedList argument if you don't want some particles subject to physics laws.
        """
        # optimisation to speed up access to these functions:
        _indexer = self.indexer
        _laws    = self.laws
        while cycles > 0:
            cycles -= 1
            self.tick += 1
            _tick = self.tick
            for p in self.particles:
                if p in avoidedList:
                    pass
                else:
                    p.doInteractions(_indexer, _laws, _tick)
            for p in self.particles:
                if p in avoidedList:
                    pass
                else:
                    p.update(_laws)
        _indexer.updateAll()
