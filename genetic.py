import random
from chromosome import Chromosome
import copy
import math

class Genetic:
    def __init__(self, chromosome_gen_prob=0.2,
                 population_size=10, generation_limit=100,
                 crossover_rate=1, mutation_rate=0.002):
        self._most_fit = []
        self._generation = 0
        self._chromosome_gen_prob = chromosome_gen_prob
        self._population_size = population_size
        self._generation_limit = generation_limit
        self._crossover_rate = crossover_rate
        self._mutation_rate = mutation_rate
        self.init_population()

    def run(self):
        print("Generation {}".format(self._generation))
        self.test_fitness()
        print("Best Chromosome {} with Fitness {}".format(
            self._most_fit[-1][0].root,
            self._most_fit[-1][1]))
        print([x[1] for x in self._fitness])

        for _ in range(self._generation_limit):
            self._generation += 1
            self.reproduce()
            self.mutate()
            self.survival_selection()
            print("Generation {}".format(self._generation))
            self.test_fitness()
            print("Best Chromosome {} with Fitness {}".format(
                self._most_fit[-1][0].root,
                self._most_fit[-1][1]))
            print([x[1] for x in self._fitness])

    def init_population(self):
        self._population = [Chromosome(gen_prob=self._chromosome_gen_prob,
                                       mutation_prob=self._mutation_rate)
                            for _ in range(self._population_size)]

    def test_fitness(self):
        self._fitness = [(c, c.eval()) for c in self._population]
        self._most_fit.append(max(self._fitness, key=lambda x: x[1]))

    def reproduce(self):
        f_min = min([x[1] for x in self._fitness])
        weights=[f[1]-f_min+1 for f in self._fitness]
        weights=[math.exp((100 - abs(f[1] - 100)) / 10) for f in self._fitness]
        mating_pool = random.choices(population=self._population,
                                     weights=weights,
                                     k=self._population_size)
        mating_pool = [copy.deepcopy(i) for i in mating_pool]
        _ = iter(mating_pool)
        offspring = list(zip(_, _))
        for p1, p2 in offspring:
            if random.random() < self._crossover_rate:
                p1.crossover(p2)
        self._offspring = [elem for pair in offspring for elem in pair]

        # mating_pairs = zip(_, _)
        # self._offspring = []
        # for p1, p2 in mating_pairs:
        #     if random.random() < self._crossover_rate:
        #         c1, c2 = Chromosome.crossover(p1, p2)
        #         self._offspring.append(c1)
        #         self._offspring.append(c2)
        #     else:
        #         self._offspring.append(p1)
        #         self._offspring.append(p2)

    def mutate(self):
        for individual in self._offspring:
            individual.mutation()

    def survival_selection(self):
        self._population = self._offspring
