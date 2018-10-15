

from environments import Maze
from dataset import MazeDataset

import math
import random

EVAL_BIAS = 3

class BaseFunctionNode:

    def children_size(self):
        return 0

    def accept(self):
        raise NotImplementedError


class ForwardNode(BaseFunctionNode):
    display = "Forward"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1

    def accept(self, visitor, env):
        env.forward()

class TurnLeftNode(BaseFunctionNode):
    display = "TurnLeft"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1

    def accept(self, visitor, env):
        env.turn_left()

class TurnRightNode(BaseFunctionNode):
    display = "TurnRight"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1

    def accept(self, visitor, env):
        env.turn_right()

class UpNode(BaseFunctionNode):
    display = "Up"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1

    def accept(self, visitor, env):
        env.up()

class DownNode(BaseFunctionNode):
    display = "Down"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1

    def accept(self, visitor, env):
        env.down()

class LeftNode(BaseFunctionNode):
    display = "Left"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1

    def accept(self, visitor, env):
        env.left()

class RightNode(BaseFunctionNode):
    display = "Right"

    def order(self, env):
        yield -1
        yield 0

    def children_size(self):
        return 1
    def accept(self, visitor, env):
        env.right()

class EndNode(BaseFunctionNode):
    display = "End"

    def children_size(self):
        return 0

    def order(self, env):
        yield -1

    def accept(self, visitor, env):
        return

class OracleNode(BaseFunctionNode):
    display = "Oracle"

    def children_size(self):
        return 5

    def order(self, env):
        yield env.oracle()
        yield 4

    def accept(self, visitor, env):
        return

class FakeOracleNode(BaseFunctionNode):
    display = "FakeOracle"

    def children_size(self):
        return 5

    def order(self, env):
        yield random.randint(0, 4)
        yield 4

    def accept(self, visitor, env):
        return

class SubFuncCallNode(BaseFunctionNode):
    display = "SubFuncCall"

    def children_size(self):
        return 1

    def order(self, env):
        yield -1
        yield 0

    def accept(self, visitor, env):
        visitor.visit(visitor.trees[0], env)

class NodeFactory:
    node_list = []

    @classmethod
    def random_node(self):
        return random.choice(self.node_list)

class MainFuncNodeFactory(NodeFactory):
    node_list = [UpNode, DownNode, LeftNode, RightNode, SubFuncCallNode, OracleNode]

class SubFuncNodeFactory(NodeFactory):
    node_list = [UpNode, DownNode, LeftNode, RightNode, OracleNode]

class TreeNode:
    def __init__(self, parent=None, function_node_factory=None, probability=0):
        if parent:
            self.depth = parent.depth + 1
            self.probability = parent.probability
        else:
            self.depth = 0
            self.probability = probability
        self.children = []
        if self.probability > random.random():
            self.function_node = function_node_factory.random_node()()
            self.children_size = self.function_node.children_size()
        else:
            self.function_node = EndNode()
            self.children_size = 0
        self.size = 1
        for _ in range(self.children_size):
            self.children.append(TreeNode(parent=self, function_node_factory=function_node_factory))
            self.size += self.children[-1].size

    def all_node(self):
        res = [self]
        for child in self.children:
            res.extend(child.all_node())
        return res

    def sample(self):
        nodes = [[0, self]]

        while nodes[-1][1].children_size: # if the node has any child
            if 1 / nodes[-1][1].size > random.random():
                return nodes

            weights = []
            for child in nodes[-1][1].children:
                weights.append(child.size)

            idx = random.choices(population=[i for i in range(nodes[-1][1].children_size)],
                           weights=weights,
                           k=1)[0]

            nodes.append([idx, nodes[-1][1].children[idx]])

        return nodes

    def visit(self, env):
        for order in self.function_node.order(env):
            if order == -1:
                yield self
            else:
                for node in self.children[order].visit(env):
                    yield node

    def accept(self, visitor, env):
        self.function_node.accept(visitor, env)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        newone.children = self.children[:]
        return newone

    def __repr__(self):
        res = ""
        res += "({}".format(self.function_node.display)
        for child in self.children:
            res += ", {}".format(child.__repr__())
        res += ")"
        return res

class MainFuncTree:
    def __init__(self, probability=0, function_node_factory=MainFuncNodeFactory):
        self.root = TreeNode(probability=probability, function_node_factory=function_node_factory)

class SubFuncTree:
    def __init__(self, probability=0, function_node_factory=SubFuncNodeFactory):
        self.root = TreeNode(probability=probability, function_node_factory=function_node_factory)

class Visitor:
    def __init__(self):
        self.trees = []

    def visit(self, func, env, trees=None):
        if trees:
            self.trees = trees
        for node in func.root.visit(env):
#            print(node)
            if node:
                node.accept(self, env)

class Chromosome:
    def __init__(self, probability=0, dataset=None, Env=Maze, Visitor=Visitor):
        self.trees = []
        self.trees.append(SubFuncTree(probability=probability))
        self.trees.append(MainFuncTree(probability=probability))
        self.visitor = Visitor()
        if dataset:
            self.envs = [Maze(dataset.num_size, maze) for maze in dataset.dataset]
        self.eval_ = 0
        self.step_penalty = 0

    def eval(self):
#        print(len(self.trees[0].root.all_node()), len(self.trees[1].root.all_node()))
        self.eval_ = 0
        self.step_penalty = 0
        for env in self.envs:
            env.reset()
            self.visitor.visit(self.trees[-1], env, self.trees)
            self.eval_ += env.eval()
            self.step_penalty -= env.step
        self.eval_ /= len(self.envs)
        self.step_penalty /= len(self.envs) * 30
        size_penalty = self.trees[0].root.size + self.trees[1].root.size
        if size_penalty > 50:
            self.eval_ = 1e-12
            return self.eval_
        if self.eval_ == 1:
            self.eval_ = max(3 + self.step_penalty, 1)
            return self.eval_
        else:
            return max(self.eval_, 1e-12)

    def __repr__(self):
        return "\nMain Func: {}\nSub Func: {}\nEval: {}\nStep Penalty: {}".format(self.trees[1].root, self.trees[0].root, self.eval_, self.step_penalty)

if __name__ == '__main__':
    c = Chromosome(probability=0.5, dataset=MazeDataset(), Env=Maze, Visitor=Visitor)
    print(c.trees[1].root, c.trees[0].root)
    c.eval()
    print(c)
