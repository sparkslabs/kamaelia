from Kamaelia.Support.Particles.ParticleSystem import ParticleSystem

class ParticleSystemX(ParticleSystem):
    def __init__(self, laws, initialParticles = [], initialTick = 0):
        super(ParticleSystemX, self).__init__(laws=laws, initialParticles = [], initialTick = 0)
    
    def run(self, cycles = 1, avoidedList=[]):
        """Run the simulation for a given number of cycles (default=1)"""

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
