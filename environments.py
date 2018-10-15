

from random import randint

import copy

class Maze:
    def __init__(self, num_size, dataset):
        self.size = num_size
        self.num_score = (num_size - 1) * 2
        self.score = 0
        self.x = 0
        self.y = 0
        self.direction = 0
        self.directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        self.maze = [[0 for i in range(self.size)] for i in range(self.size)]
        self.origin_maze = dataset
        self.step = 0

    def reset(self):
        self.step = self.score = self.x = self.y = self.direction = 0
        self.maze = copy.deepcopy(self.origin_maze)

    def forward(self):
        #self.x = (self.x + self.directions[self.direction][0]) % self.size
        #self.y = (self.y + self.directions[self.direction][1]) % self.size
        self.x = max(0, min(self.size - 1, self.x + self.directions[self.direction][0]))
        self.y = max(0, min(self.size - 1, self.y + self.directions[self.direction][1]))
        if self.maze[self.x][self.y] == 1:
            self.score += 1
            self.maze[self.x][self.y] = 0
        self.step += 1

    def turn_left(self):
        self.direction += 1
        self.direction %= len(self.directions)

    def turn_right(self):
        self.direction += 3
        self.direction %= len(self.directions)

    def up(self):
        self.forward_with_direction(0)

    def down(self):
        self.forward_with_direction(2)

    def left(self):
        self.forward_with_direction(1)

    def right(self):
        self.forward_with_direction(3)

    def forward_with_direction(self, direction):
        self.x = (self.x + self.directions[direction][0]) % self.size
        self.y = (self.y + self.directions[direction][1]) % self.size
        if self.maze[self.x][self.y] == 1:
            self.score += 1
            self.maze[self.x][self.y] = 0
        self.step += 1

    def oracle(self):
        for idx, direction in enumerate(self.directions):
            self.next_x = min(self.size - 1, max(0, self.x + self.directions[self.direction][0]))
            self.next_y = min(self.size - 1, max(0, self.y + self.directions[self.direction][1]))
            if self.maze[self.next_x][self.next_y] == 1:
                return idx % 4
        # return randint(0, 3) there should not be random.
        return 4

    def eval(self):
        return self.score / self.num_score

    def __repr__(self):
        return "(x, y): ({}, {}) score: {}".format(self.x, self.y, self.score)
