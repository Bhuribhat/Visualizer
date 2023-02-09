import copy
from random import sample

base = 3
side = 9

# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s):
    return sample(s, len(s))


# pattern for a baseline valid solution
def pattern(r, c):
    return (base * (r % base) + r // base + c) % side


def generate_sudoku(display=False):
    global solution, board
    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    solution = copy.deepcopy(board)
    if display:
        print("\nSolution")
        for line in board:
            print(line)

    # generate initial board
    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    if display:
        numSize = len(str(side))
        print("\nBoard")
        for line in board:
            print("[" + "  ".join(f"{n or '.':{numSize}}" for n in line) + "]")
    return solution, board


if __name__ == '__main__':
    generate_sudoku()
    print(board)
    print(solution)