

import random
import copy


class Selection:
    def __init__(self):
        pass

    def __call__(self, population):
        pass


class RouletteWheelSelection(Selection):
    def __init__(self):
        pass

    def __call__(self, population):
        select = random.choices(population=population,
                                weights=[c.eval() for c in population],
                                k=len(population))
        #select = [copy.deepcopy(s) for s in select]
        return select


class TournamentSelection(Selection):
    def __init__(self, size=2):
        self._size = size

    def __call__(self, population):
        length = len(population)
        tournaments = [random.choices(population=population, k=self._size)
                       for _ in range(length)]
        select = [self._single_tournament(*t) for t in tournaments]
        #select = [copy.deepcopy(s) for s in select]
        return select

    def _single_tournament(self, *players):
        return max(players, key=lambda x: x.eval())
