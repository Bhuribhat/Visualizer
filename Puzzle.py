""" A* search
A class representing an Solver node

Solved when board's numbers are in order from left to right 
and the '0' tile is in the last position on the board

- 'puzzle' is a Puzzle instance
- 'parent' is the preceding node generated by the solver, if any
- 'action' is the action taken to produce puzzle, if any
- 'board'  is a square list of lists with integer entries 0..width^2 - 1 """

import time
import random
import itertools
from collections import deque


class Node:
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        if (self.parent is not None):
            self.g = parent.g + 1
        else:
            self.g = 0

    @property
    def score(self):
        return (self.g + self.h)

    # Return a hashable representation of self
    @property
    def state(self):
        return str(self)

    # Reconstruct a path from to the root 'parent'
    @property
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    # Wrapper to check if 'puzzle' is solved
    @property
    def solved(self):
        return self.puzzle.solved

    # Wrapper for 'actions' accessible at current state
    @property
    def actions(self):
        return self.puzzle.actions

    @property
    def h(self):
        return self.puzzle.manhattan

    @property
    def f(self):
        return self.h + self.g

    def __str__(self):
        return str(self.puzzle)


class Solver:
    def __init__(self, start):
        self.start = start

    # Perform BFS and return a path to the solution, if it exists
    def solve(self):
        queue = deque([Node(self.start)])
        visit = set()
        visit.add(queue[0].state)
        F = lambda node: node.f

        while queue:
            queue = deque(sorted(list(queue), key=F))
            node = queue.popleft()
            if node.solved:
                return node.path

            for move, action in node.actions:
                child = Node(move(), node, action)

                if child.state not in visit:
                    queue.appendleft(child)
                    visit.add(child.state)


class Puzzle:
    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1, N))) + '0'

    # list of 'move' from sliding '0' in the direction of 'action'
    @property
    def actions(self):
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width), range(self.width)):
            direct = {'R': (i, j - 1),
                      'L': (i, j + 1),
                      'D': (i - 1, j),
                      'U': (i + 1, j)}

            for action, (r, c) in direct.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i, j), (r, c)), action
                    moves.append(move)
        return moves

    @property
    def manhattan(self):
        distance = 0
        for i in range(WIDTH):
            for j in range(WIDTH):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j] - 1, WIDTH)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def shuffle(self):
        puzzle = self
        for _ in range(100):
            puzzle = random.choice(puzzle.actions)[0]()
        return puzzle

    def _copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        copy = self._copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def pprint(self):
        represent = "\n"
        PAD = 3 if WIDTH <= 2 else WIDTH
        for i in range(self.width):
            row = ""
            for num in self.board[i]:
                num = str(num)
                row += ' ' * (WIDTH - len(num) - 2) + num + ' | '
            for _ in range(self.width):
                represent += '+' + '-' * PAD
            represent += "+\n"
            represent += "| " + row + "\n"
        for _ in range(self.width):
            represent += '+' + '-' * PAD
        represent += "+\n"
        print(represent)

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row


if __name__ == '__main__':
    print("This program can solve 8-Puzzle and 15-Puzzle")
    print("The puzzle must be a square board\n")

    BOARD = []
    WIDTH = int(input("Enter board's width: ").strip())

    rand_board = input("Random board (Y/N)? ").upper().strip()
    if rand_board.startswith('Y'):
        BOARD = [[i for i in range(j, j + WIDTH)] for j in range(0, WIDTH * WIDTH, WIDTH)]
        puzzle = Puzzle(BOARD)
        puzzle = puzzle.shuffle()
    else:
        for i in range(1, WIDTH + 1):
            row = map(int, input(f"Enter row {i}: ").split())
            BOARD.append(list(row))
        puzzle = Puzzle(BOARD)

    startTime = time.time()
    puzzle.pprint()

    SOLUTION = Solver(puzzle).solve()
    finishTime = time.time()
    command = input("Ready for Solution? ").strip()

    if SOLUTION == None:
        print("There is no solution")
    else:
        moves = []
        steps = 0
        for state in SOLUTION:
            if state.action == None:
                print("\nStart Board")
            else:
                print(state.action)
                moves.append(state.action)
                steps += 1
            state.puzzle.pprint()

        print("Solution:", *moves)
        print(f"Total number of steps: {steps}")
        print(f"Total amount of times: {finishTime - startTime:.3f} second(s)")