

import matplotlib.pyplot as plt
from statistics import mean
from genetic import Genetic
from chromosome import Chromosome, EVAL_BIAS
from selection import RouletteWheelSelection, TournamentSelection
#from crossover import SinglePointCrossover, SinglePointCrossoverWithRate
from crossover import TreeCrossover
from reproduction import SimpleGeneticAlgorithmReproduction
#from mutation import BitwiseMutation
from mutation import NullMutation


def test_genetic():
    statistics = []
    chromosome_size = 50
    population_size = 200
    generation_limit = 100
    # EVAL_BIAS is in chromosome.py

    parent_selection_strategy = RouletteWheelSelection()
    # parent_selection_strategy = TournamentSelection(size=2)
    # crossover_strategy = SinglePointCrossoverWithRate(rate=1.0)
    crossover_strategy = TreeCrossover()
    reproduction_strategy = SimpleGeneticAlgorithmReproduction(
        parent_selection_strategy = parent_selection_strategy,
        crossover_strategy = crossover_strategy
    )
#    mutation_strategy = BitwiseMutation(rate=0.0)
    mutation_strategy = NullMutation()

    for _ in range(10):
        genetic = Genetic(chromosome_size=chromosome_size,
                          population_size=population_size,
                          generation_limit=generation_limit,
                          reproduction_strategy=reproduction_strategy,
                          mutation_strategy=mutation_strategy)
        statistics.append(genetic.run())
    result = list(map(mean, zip(*statistics)))
    result[:] = map(lambda x: x - EVAL_BIAS, result)
    # plt.plot(list(map(lambda x: x-1000, result)))
    plt.gca().set_ylim([0,chromosome_size + 0.5])
    plt.plot(result)
    plt.show()


def main():
    test_genetic()


if __name__ == '__main__':
    main()
