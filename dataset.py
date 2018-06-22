

from random import randint
from random import shuffle


class MazeDataset:
    def __init__(self, num_maze=5, num_size=10):
        self.num_maze = num_maze
        self.num_size = num_size
        self.dataset = [self.random_maze() for _ in range(self.num_maze)]

    def random_maze(self):
        maze = [[0 for _ in range(self.num_size)] for _ in range(self.num_size)]
        directions = [0] * (self.num_size - 1) + [1] * (self.num_size - 1) # 0 represents up, 1 represents right
        shuffle(directions)
        pos = [0, 0]
        for direction in directions:
            if direction == 0:
                pos[1] += 1
            else:
                pos[0] += 1
            maze[pos[0]][pos[1]] = 1
        return maze
