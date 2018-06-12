

from environments import Maze

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
        return 4

    def order(self, env):
        yield env.oracle()

    def accept(self, visitor, env):
        return

class FakeOracleNode(BaseFunctionNode):
    display = "FakeOracle"

    def children_size(self):
        return 4

    def order(self, env):
        yield random.randint(0, 3)

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
    node_list = [ForwardNode, TurnLeftNode, TurnRightNode, SubFuncCallNode, OracleNode]

class SubFuncNodeFactory(NodeFactory):
    node_list = [ForwardNode, TurnLeftNode, TurnRightNode, OracleNode]

class TreeNode:
    def __init__(self, parent=None, function_node_factory=None, probability=0):
        self.parent = parent
        if self.parent:
            self.depth = self.parent.depth + 1
            self.probability = self.parent.probability
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
        for _ in range(self.children_size):
            self.children.append(TreeNode(parent=self, function_node_factory=function_node_factory))

    def all_node(self):
        res = [self]
        for child in self.children:
            res.extend(child.all_node())
        return res

    def sample(self):
        return random.choice(self.all_node())

    def visit(self, env):
        for order in self.function_node.order(env):
            if order == -1:
                yield self
            else:
                for node in self.children[order].visit(env):
                    yield node

    def accept(self, visitor, env):
        self.function_node.accept(visitor, env)

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
    def __init__(self, trees):
        self.trees = trees

    def visit(self, func, env):
        for node in func.root.visit(env):
#            print(node)
            if node:
                node.accept(self, env)

class Chromosome:
    def __init__(self, probability=0, dataset=None, Env=Maze, Visitor=Visitor):
        self.trees = []
        self.trees.append(SubFuncTree(probability=probability))
        self.trees.append(MainFuncTree(probability=probability))
        self.visitor = Visitor(self.trees)
        self.envs = [Maze(dataset.num_size, maze) for maze in dataset.dataset]
        self.eval_ = 0
        self.step_penalty = 0

    def eval(self):
#        print(len(self.trees[0].root.all_node()), len(self.trees[1].root.all_node()))
        self.eval_ = 0
        self.step_penalty = 0
        for env in self.envs:
            env.reset()
            self.visitor.visit(self.trees[-1], env)
            self.eval_ += env.eval()
            self.step_penalty -= env.step
        self.eval_ /= len(self.envs)
        self.step_penalty /= len(self.envs) * 200
        size_penalty = len(self.trees[0].root.all_node()) + len(self.trees[1].root.all_node())
        if self.step_penalty < -1 or size_penalty >= 400:
            return 1e-12
        if self.eval_ == 1:
            return max(3 + self.step_penalty, 1)
        else:
            return max(self.eval_, 1e-12)

    def __repr__(self):
        return "\nMain Func: {}\nSub Func: {}\nEval: {}\nStep Penalty: {}".format(self.trees[1].root, self.trees[0].root, self.eval_, self.step_penalty)

if __name__ == '__main__':
    c = Chromosome(probability=0.8, Env=Environment, Visitor=Visitor)
    print(c.trees[1].root, c.trees[0].root)
    c.eval()
    print(c)
