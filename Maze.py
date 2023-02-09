import random
import numpy as np


ROWS = 50

# binary maze
def binary_maze(size = ROWS // 3):
    N, P = (1, 0.5)
    grid = np.random.binomial(N, P, size=(size, size))
    output_grid = np.empty([ROWS, ROWS], dtype=str)
    output_grid[:] = '#'
    i, j = (0, 0)
    while i < size:
        w = i * 3 + 1
        while j < size:
            k = j * 3 + 1
            toss = grid[j][i]
            output_grid[w, k] = ' '
            if toss == 0 and k + 2 <= ROWS:
                output_grid[w, k + 1] = ' '
                output_grid[w, k + 2] = ' '
            if toss == 1 and w - 2 >= 0:
                output_grid[w - 1, k] = ' '
                output_grid[w - 2, k] = ' '
            j = j + 1
        i = i + 1
        j = 0
    return output_grid


# '1' represents a wall and '0' represents a passageway
def generate_maze(width, height):
    grid = [[0 for _ in range(width)] for _ in range(height)]

    # Fill the grid with walls
    for row in range(height):
        for col in range(width):
            if row == 0 or row == height - 1 or col == 0 or col == width - 1:
                grid[row][col] = 1
            else:
                grid[row][col] = random.choice([0, 1])

    # Randomly carve passages through the walls
    for row in range(1, height - 1, 2):
        for col in range(1, width - 1, 2):
            grid[row][col] = 0
            neighbors = []

            if row > 1:
                neighbors.append((row - 2, col))
            if row < height - 2:
                neighbors.append((row + 2, col))
            if col > 1:
                neighbors.append((row, col - 2))
            if col < width - 2:
                neighbors.append((row, col + 2))

            if neighbors:
                row2, col2 = random.choice(neighbors)
                grid[row2][col2] = 0
                grid[row2 + (row - row2) // 2][col2 + (col - col2) // 2] = 0

    return grid


# '1' represents a wall and '0' represents a passageway
def backtracking(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]

    # Choose a starting point
    start_row = random.randint(0, height - 1)
    start_col = random.randint(0, width - 1)

    # Define the directions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Remove wall between current cell and randomly choose neighbor cell
    def visit(row, col):
        neighbors = []

        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]

            if new_row >= 0 and new_col >= 0 and new_row < height and \
                new_col < width and grid[new_row][new_col] == 1:
                neighbors.append((new_row, new_col))

        if neighbors:
            new_row, new_col = random.choice(neighbors)
            grid[(row + new_row) // 2][(col + new_col) // 2] = 0
            visit(new_row, new_col)

    visit(start_row, start_col)

    return grid


# '#' represents a wall and '.' represents a passageway
def print_maze(grid):
    for row in grid:
        display = ["#" if cell else "." for cell in row]
        print("".join(display))


if __name__ == '__main__':
    grid = generate_maze(50, 50)
    print_maze(grid)