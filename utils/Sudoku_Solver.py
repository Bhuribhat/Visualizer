import copy
import time
import pyautogui as pg 


# return (row, col)
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


# backtracking algorithm
def valid(board, num, pos):

    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


# state space search
def solve(board):
    global SOLUTION
    find = find_empty(board)
    if not find:
        SOLUTION = board[::]
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False


# automatically solver in https://sudoku.com/
# NOTE Place your cursor at Top-Left of the board
def auto_solve(board):
    solution = []
    for row in board:
        for number in row:
            solution.append(str(number))

    counter = 0
    for number in solution:
        pg.press(number)
        pg.hotkey('right')
        counter += 1

        if counter % 9 == 0:
            pg.hotkey('down')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')
            pg.hotkey('left')


# display solution
def print_board(solution):
    count, col = 0, 0
    edge = '+' + '-' * 7
    print('\n' + edge * 3 + '+')
    for row in solution:
        for num in row:
            if count == 9:
                print('|')
                count = 0
                col += 1
                if col % 3 == 0:
                    print(edge * 3 + '+')
            if count % 3 == 0:
                print('|', end=' ')
            count += 1
            print(num, end=' ')
    print('|\n' + edge * 3 + '+')


if __name__ == '__main__':
    initBoard = [
        [3, 0, 0, 0, 1, 0, 4, 0, 0],
        [0, 0, 2, 0, 5, 0, 0, 0, 0],
        [8, 0, 0, 4, 0, 2, 0, 6, 0],
        [0, 3, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 4, 3, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 8, 3, 0, 9, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 7]
    ]
    board = copy.deepcopy(initBoard)
    if solve(board):
        print_board(board)
    else:
        print("There is no solution")
    
    autoSolver = input("Use Auto-Solver (Y/N)? ").upper().strip()
    if autoSolver.startswith('Y'):
        for i in range(5):
            print(f"{5 - i}..")
            time.sleep(1)
        print("Start solving now!")
        auto_solve(board)