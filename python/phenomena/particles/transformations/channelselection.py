import random
from phenomena.particles.sources import ParticleDataSource

class TransChannelSelector(object):

    def __init__(self, allChannels):
        self._allChannels = allChannels
        self._selectChannel()

    @property
    def value(self):
        return self._selectedChannel

    def _selectChannel(self):
        list_decay = []
        buildWeights = TransChannelSelector.buildWeights(self._allChannels)
        if self._allChannels != {'type':'NoTransformation'}:
            choice = TransChannelSelector.weightedChoice(buildWeights[0],buildWeights[1])
            channel = self._allChannels[choice][1]
            for pdgid in channel:
                list_decay.append(ParticleDataSource.getName(pdgid))
        self._selectedChannel = list_decay

    @staticmethod
    def buildWeights(transformation_channels):
        seq = []
        weights=[]
        for index, item in enumerate(transformation_channels):
            if item[0] != 0.0:           # do not use channels with prob = 0.0
                seq.append(index)
                weights.append(item[0])
        return seq, weights

    @staticmethod
    def weightedChoice(seq, weights):
        assert len(weights) == len(seq)
        #assert abs(1. - sum(weights)) < 1e-6
        x = random.random()
        for i, elmt in enumerate(seq):
            if x <= weights[i]:
                return elmt
            x -= weights[i]
