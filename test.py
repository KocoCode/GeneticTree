

from chromosome import Chromosome
from genetic import Genetic


def test_chromosome():
    for _ in range(10):
        p1 = Chromosome(gen_prob=0.1, mutation_prob=0)
        p2 = Chromosome(gen_prob=0.1, mutation_prob=0)
        print("{} {}".format(p1.root, p1.eval()))
        print("{} {}".format(p2.root, p2.eval()))
        p1.crossover(p2)
        print("{} {}".format(p1.root, p1.eval()))
        print("{} {}".format(p2.root, p2.eval()))
        print()
        print()


def test_genetic():
    genetic = Genetic(chromosome_gen_prob=0.4,
                      population_size=100,
                      generation_limit=40,
                      crossover_rate=1,
                      mutation_rate=0.1)
    genetic.run()


def main():
    # test_chromosome()
    test_genetic()


if __name__ == '__main__':
    main()
