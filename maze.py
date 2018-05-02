



class Maze:
    def __init__(self, size):
        self._size = size
        self._maze = [[1 for _ in range(size)] for _ in range(self.size)]
        self._position = [0, 0]
        self._maze[self._position[0]][self._position[1]] = 0
        self._score = 0
        self._directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self._direction = 1  # right

    @property
    def size(self):
        return self._size

    @property
    def score(self):
        return self._score

    def reset(self):
        self._maze = [[1 for _ in range(self.size)] for _ in range(self.size)]
        self._position = [0, 0]
        self._maze[self._position[0]][self._position[1]] = 0
        self._score = 0
        self._direction = 1

    def forward(self):
        direction = self._directions[self._direction]
        self._position[0] = (self._position[0] + direction[0]) % self._size
        self._position[1] = (self._position[1] + direction[1]) % self._size
        # print("my position")
        # print(self._position)
        if self._maze[self._position[0]][self._position[1]] == 1:
            self._score += 1
            self._maze[self._position[0]][self._position[1]] = 0
        # return self.score
        return self._position

    def turnRight(self):
        self._direction = (self._direction + 1) % 4
        # return self.score
        return self._position

    def turnLeft(self):
        self._direction = (self._direction - 1) % 4
        # return self.score
        return self._position

    def printMaze(self):
        for i in range(self._size):
            for j in range(self._size):
                if [i, j] == self._position:
                    print('*', end=' ')
                else:
                    print('{}'.format(self._maze[i][j]),
                          end=' ')
            print()
        print('score = {}'.format(self._score))
        print()


def test():
    pass


if __name__ == '__main__':
    test()
