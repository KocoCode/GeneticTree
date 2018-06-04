

import random
import copy
from chromosome import Chromosome


class Crossover:
    def __init__(self):
        pass

    def __call__(self, *parents):
        pass

class TreeCrossover(Crossover):
    def __init__(self):
        pass

    def __call__(self, parent1, parent2):
        for idx in range(len(parent1.trees)):
            self.crossover(parent1.trees[idx], parent2.trees[idx])
        
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    def crossover(self, parent1, parent2):
        lsample = parent1.root.sample()
        rsample = parent2.root.sample()
        lparent = lsample.parent
        rparent = rsample.parent
        if lparent:
            for idx, child in enumerate(lparent.children):
                if child == lsample:
                    lparent.children[idx] = rsample
        else:
            parent1.root = rsample
        rsample.parent = lparent
        if rparent:
            for idx, child in enumerate(rparent.children):
                if child == rsample:
                    rparent.children[idx] = lsample
        else:
            parent2.root = lsample
        lsample.parent = rparent
