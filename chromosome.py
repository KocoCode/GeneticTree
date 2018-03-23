import random

class Tree:
    def __init__(self, parent = None, is_external = False, probability = 0):
        self.is_external = is_external
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
            self.probability = parent.probability
        else:
            self.depth = 0
            self.probability = probability
        self.lc = None
        self.rc = None

        if self.is_external:
            self.num = random.randint(0, 9)
        else:
            self.op = random.randint(0, 2)

    def eval(self):
        if self.is_external:
            return self.num
        else:
            leval = self.lc.eval()
            reval = self.rc.eval()
            if self.op == 0:
                return leval + reval
            elif self.op == 1:
                return leval - reval
            elif self.op == 2:
                return leval * reval

    def init_child(self):
        if random.random() < self.probability and self.depth < 100:
            self.lc = Tree(self) 
            self.lc.init_child()
        else:
            self.lc = Tree(self, True)

        if random.random() < self.probability and self.depth < 100:
            self.rc = Tree(self)
            self.rc.init_child()
        else:
            self.rc = Tree(self, True)

    def mutation(self, mutation_prob):
        if self.is_external:
            return
        if random.random() < mutation_prob:
            if random.random() < 0.5:
                self.lc = Tree(self, probability=self.probability * 0.8)
                self.lc.init_child()
            else:
                self.rc = Tree(self, probability=self.probability * 0.8)
                self.rc.init_child()
        else:
            if random.random() < 0.5:
                self.lc.mutation(mutation_prob)
            else:
                self.rc.mutation(mutation_prob)

    def all_node(self):
        res = [self]
        if self.lc:
            res += self.lc.all_node()
        if self.rc:
            res += self.rc.all_node()
        return res

    def sample(self):
        return random.choice(self.all_node())
    
    def __repr__(self):
        if self.is_external:
            return str(self.num)
        else:
            if self.op == 0:
                display = "+"
            elif self.op == 1:
                display = "-"
            elif self.op == 2:
                display = "*"
        res = ""
        res += "({}, ".format(display)
        lres = self.lc.__repr__()
        res += "{}, ".format(lres)
        rres = self.rc.__repr__()
        res += "{})".format(rres)
        return res

class Chromosome:
    def __init__(self, gen_prob, mutation_prob):
        self.root = Tree(probability=gen_prob)
        self.root.init_child()
        self.mutation_prob = mutation_prob

    def mutation(self):
        self.root.mutation(self.mutation_prob)

    def crossover(self, rhs):
        lsample = self.root.sample()
        rsample = rhs.root.sample()
        lparent = lsample.parent
        rparent = rsample.parent
        if lparent:
            if lparent.lc == lsample:
                lparent.lc = rsample
            else:
                lparent.rc = rsample
        else:
            self.root = rsample
        rsample.parent = lparent
        if rparent:
            if rparent.lc == rsample:
                rparent.lc = lsample
            else:
                rparent.rc = lsample
        else:
            rhs.root = lsample
        lsample.parent = rparent

    def eval(self):
        return self.root.eval()


def main():
    chromosome = Chromosome(0.5, 0.2)

if __name__ == "__main__":
    main()

