

from chromosome import Chromosome


class Genetic:
    def __init__(self,
                 chromosome_size=20,
                 population_size=10,
                 generation_limit=50,
                 reproduction_strategy=None,
                 mutation_strategy=None):
        self._chromosome_size = chromosome_size
        self._population_size = population_size
        self._generation_limit = generation_limit
        if reproduction_strategy:
            self._reproduction = reproduction_strategy
        if mutation_strategy:
            self._mutation = mutation_strategy

        self._generation_count = 0

        # list of chromosome
        self._population = []

        # list of pair (chromosome, its fitness value)
        # pairs of the current population
        self._fitness = []

        # list of pair (chromosome, its fitness value)
        # best pairs of each generation
        self._most_fit = []

        # list of chromosome
        # children reproduced by population
        self._offspring = []

        self.init_population()

    def init_population(self):
        self._population[:] = [Chromosome(1)
                               for _ in range(self._population_size)]

    def run(self):
        self.test_fitness()
        # self.print_current_info()
        for _ in range(self._generation_limit):
            self._generation_count += 1
            self.reproduce()
            self.mutate()
            self.survival_selection()
            self.test_fitness()
            self.print_current_info()
        return [x[1] for x in self._most_fit]

    def print_current_info(self):
        print("Generation {}".format(self._generation_count))
        #print(self._fitness)
#         print("Best Chromosome {}({}) with Fitness {}".format(
#             self._most_fit[-1][0],
#             self._most_fit[-1][0]._genes.count('1'),
#             self._most_fit[-1][1]))
        print("Best Chromosome {} with Fitness {}".format(self._most_fit[-1][0], self._most_fit[-1][0].eval()))
        #print([x[1] for x in self._fitness])

    def test_fitness(self):
        self._fitness[:] = [(c, c.eval()) for c in self._population]
        self._most_fit.append(max(self._fitness, key=lambda x: x[1]))

    def reproduce(self):
        self._offspring[:] = self._reproduction(self._population)

    def mutate(self):
        self._offspring[:] = map(self._mutation, self._offspring)

    def survival_selection(self):
        self._population[:] = self._offspring
