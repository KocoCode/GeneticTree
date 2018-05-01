

import random
from chromosome import Chromosome


class Mutation:
    def __init__(self):
        pass

    def __call__(self, individual):
        pass

class NullMutation:
    def __init__(self):
        pass

    def __call__(self, individual):
        return individual
