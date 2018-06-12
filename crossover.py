

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
        parent1 = copy.copy(parent1)
        parent1.trees = copy.copy(parent1.trees)
        parent2 = copy.copy(parent2)
        parent2.trees = copy.copy(parent2.trees)

        for idx in range(len(parent1.trees)):
            parent1.trees[idx] = copy.copy(parent1.trees[idx])
            parent2.trees[idx] = copy.copy(parent2.trees[idx])
            self.crossover(parent1.trees[idx], parent2.trees[idx])

        return parent1, parent2

    def crossover(self, parent1, parent2):
        lsample = parent1.root.sample()
        rsample = parent2.root.sample()
        lsize = rsample[-1][1].size - lsample[-1][1].size
        rsize = -lsize
        lsample[-1][1], rsample[-1][1] = rsample[-1][1], lsample[-1][1]

        # left tree
        prev_node = copy.copy(lsample[-1][1])
        child_idx = lsample[-1][0]
        lsample.pop()

        while lsample:
            node = copy.copy(lsample[-1][1])
            node.children[child_idx] = prev_node
            node.size += lsize
            prev_node = node
            child_idx = lsample[-1][0]
            lsample.pop()

        parent1.root = prev_node

        # right tree
        prev_node = copy.copy(rsample[-1][1])
        child_idx = rsample[-1][0]
        rsample.pop()

        while rsample:
            node = copy.copy(rsample[-1][1])
            node.children[child_idx] = prev_node
            node.size += rsize
            prev_node = node
            child_idx = rsample[-1][0]
            rsample.pop()

        parent2.root = prev_node
