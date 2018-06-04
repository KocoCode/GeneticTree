

import asyncio
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
    order = [-1, 0]

    def children_size(self):
        return 1

    async def accept(self, visitor):
        visitor.env.forward()

class TurnLeftNode(BaseFunctionNode):
    display = "TurnLeft"
    order = [-1, 0]

    def children_size(self):
        return 1

    async def accept(self, visitor):
        visitor.env.turn_left()

class EndNode(BaseFunctionNode):
    display = "End"
    order = []

    def children_size(self):
        return 0

    async def accept(self, visitor):
        return

class SubFuncCallNode(BaseFunctionNode):
    display = "SubFuncCall"
    order = [-1, 0]

    def children_size(self):
        return 1

    async def accept(self, visitor):
        await visitor.visit(visitor.trees[0])

class NodeFactory:
    node_list = []

    @classmethod
    def random_node(self):
        return random.choice(self.node_list)

class MainFuncNodeFactory(NodeFactory):
    node_list = [ForwardNode, TurnLeftNode, SubFuncCallNode, EndNode]

class SubFuncNodeFactory(NodeFactory):
    node_list = [ForwardNode, TurnLeftNode, EndNode]

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

    async def visit(self):
        for order in self.function_node.order:
            if order == -1:
                yield self
            else:
                async for node in self.children[order].visit():
                    yield node

    async def accept(self, visitor):
        await self.function_node.accept(visitor)

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
    def __init__(self, env, trees):
        self.env = env
        self.trees = trees

    async def visit(self, func):
        async for node in func.root.visit():
#            print(node)
            if node:
                await node.accept(self)

class Environment:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    def reset(self):
        self.x = self.y = self.direction = 0

    def forward(self):
        self.x += self.directions[self.direction][0]
        self.y += self.directions[self.direction][1]

    def turn_left(self):
        self.direction += 1
        self.direction %= len(self.directions)

    def eval(self):
        return math.exp((-(abs(self.x - 20) + abs(self.y - 20)) / 2))

    def __repr__(self):
        return "(x, y): ({}, {})".format(self.x, self.y)

class Chromosome:
    def __init__(self, probability=0, Env=Environment, Visitor=Visitor):
        self.trees = []
        self.trees.append(SubFuncTree(probability=probability))
        self.trees.append(MainFuncTree(probability=probability))
        self.visitor = Visitor(Env(), self.trees)

    def eval(self):
#        print(len(self.trees[0].root.all_node()), len(self.trees[1].root.all_node()))
        self.visitor.env.reset()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.visitor.visit(self.trees[-1]))
        eval_ = self.visitor.env.eval()
        size_penalty =  - (len(self.trees[0].root.all_node()) + len(self.trees[1].root.all_node())) / 30
        if size_penalty < -1:
            return 1e-8
        if eval_ == 1:
            return max(3 + size_penalty, 1)
        elif eval_ > 0.5:
            return max(eval_ + size_penalty, 1e-8)
        else:
            return eval_

    def __repr__(self):
        return "\nMain Func: {}\nSub Func: {}\nEnv: {}".format(self.trees[1].root, self.trees[0].root, self.visitor.env)

if __name__ == '__main__':
    c = Chromosome(probability=0.8, Env=Environment, Visitor=Visitor)
    print(c.trees[1].root, c.trees[0].root)
    c.eval()
    print(c)
