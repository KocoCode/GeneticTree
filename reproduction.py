

import random


class Reproduction:
    def __init__(self):
        pass

    def __call__(self, population):
        pass


class SimpleGeneticAlgorithmReproduction(Reproduction):
    def __init__(self,
                 parent_selection_strategy=None,
                 crossover_strategy=None):
        if parent_selection_strategy:
            self._parent_selection = parent_selection_strategy
        if crossover_strategy:
            self._crossover = crossover_strategy

    def __call__(self, population):
        mating_pool = self._parent_selection(population)
        random.shuffle(mating_pool)
        _ = iter(mating_pool)
        mating_pairs = zip(_, _)
        offspring = []
        for p1, p2 in mating_pairs:
            c1, c2 = self._crossover(p1, p2)
            offspring.append(c1)
            offspring.append(c2)
        return offspring
