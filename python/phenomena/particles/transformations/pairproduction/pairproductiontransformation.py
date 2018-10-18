from phenomena.particles.transformations import Transformation
from phenomena.particles.sources import ParticleDataSource

class PairProduction(Transformation):

    INPUT = ['gamma']
    OUTPUT = ['e-', 'e+', 'p+']

    def __init__(self, particle):
        self._particle = particle
        self._values = {}
        if  self._particle.name in PairProduction.INPUT:
            self._buildTransfValues()

    def _outputParticles(self):
        return [(1.0, map(ParticleDataSource.getPDGId, PairProduction.OUTPUT)) ]
        #return [[ParticleDataSource.getPDGId(part) for part in list] for list in OUTPUT]

    def _transfTime(self):
        return 1
