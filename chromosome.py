

import math
import random

EVAL_BIAS = 100

def gen_tree(probability=0):
    return random.choice(InternalNode.__subclasses__())(probability=probability)

class BaseNode:
    def __init__(self, parent=None, is_external=False, probability=0,
            children_size=1):
        self.parent = parent
        if self.parent:
            self.depth = self.parent.depth + 1 
            self.probability = self.parent.probability
        else:
            self.depth = 0
            self.probability = probability
        self.is_external = is_external
        self.children_size = children_size
        self.children = []
        self.init_children()

    def eval(self):
        raise NotImplementedError

    def all_node(self):
        res = [self]
        for child in self.children:
            res.extend(child.all_node())
        return res

    def sample(self):
        return random.choice(self.all_node()) 

    def init_children(self):
        for _ in range(self.children_size):
            if random.random() < self.probability:
                self.children.append(random.choice(InternalNode.__subclasses__())(parent=self))
            else:
                self.children.append(random.choice(ExternalNode.__subclasses__())(parent=self))

    def __repr__(self):
        res = ""
        res += "({}".format(self.display)
        for child in self.children:
            res += ", {}".format(child.__repr__())
        res += ")"
        return res 

    def subclasses(self):
        return BaseNode.__subclasses__()

class InternalNode(BaseNode):
    def __init__(self, parent=None, is_external=False, probability=0,
            children_size=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=children_size)

class ExternalNode(BaseNode):
    def __init__(self, parent=None, is_external=False, probability=0,
            children_size=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=children_size)

class AddNode(InternalNode):
    display = "+"

    def __init__(self, parent=None, is_external=False, probability=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=2)

    def eval(self):
        return self.children[0].eval() + self.children[1].eval()

class SubNode(InternalNode):
    display = "-"

    def __init__(self, parent=None, is_external=False, probability=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=2)

    def eval(self):
        return self.children[0].eval() - self.children[1].eval()

class MulNode(InternalNode):
    display = "*"

    def __init__(self, parent=None, is_external=False, probability=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=2)

    def eval(self):
        return self.children[0].eval() * self.children[1].eval()

class NumNode(ExternalNode):
    def __init__(self, parent=None, is_external=False, probability=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=0)
        self.num = random.randint(-9, 9)
        self.display = self.num

    def eval(self):
        return self.num

class IfNode(InternalNode):
    display = "If"

    def __init__(self, parent=None, is_external=False, probability=0):
        super().__init__(parent=parent, is_external=is_external,
                probability=probability, children_size=3)

    def eval(self):
        if self.children[0].eval() > 0:
            return self.children[1].eval()
        else:
            return self.children[2].eval()

class Chromosome:
    def __init__(self, probability=0):
        self.root = gen_tree(probability=probability)

    def eval(self):
        if self.root.eval() ==  EVAL_BIAS:
            return 20 - min(19, math.exp(len(self.root.all_node()) / 5))
        else:
            return math.exp(-abs(self.root.eval() - EVAL_BIAS) - len(self.root.all_node()) / 5)

if __name__ == '__main__':
    c = Chromosome(probability=0.4)
    print(c.root, c.eval())
