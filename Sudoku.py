import time
import pygame
pygame.font.init()

from utils.Sudoku_Board import generate_sudoku
from utils.Sudoku_Solver import print_board

INSTRUCTION = """
=== Sudoku GUI : 5 lives ===
1. 'Click' to select the grid
2. '1-9' to sketch number and 'Enter' to confirm
3. 'Del' to delete sketch
4. 'I' to view instruction
5. 'C' to clear all sketch
6. 'R' to reset board
7. 'N' to create new game
8. 'Space Bar' to show solution (sketch)
9. 'Arrow Key' to navigate through grid """

# COLORS
WHITE  = (255, 255, 255)
GREY   = (128, 128, 128)
DARK   = (49, 49, 49)
BLACK  = (0, 0, 0)
ORANGE = (255, 165, 0)
RED    = (255, 0, 0)


# board = initBoard
class Grid:
    solution, board = generate_sudoku()

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            # if valid(self.model, val, (row,col)) and solve(self.model):
            if self.model[row][col] == self.solution[row][col]:
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, window):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 2
            pygame.draw.line(window, BLACK, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(window, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(window)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)
        return (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window):
        fnt = pygame.font.SysFont("comicsans", 35)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # Draw Grid Line
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, GREY)
            window.blit(text, (x + 5, y + 5))
        elif not self.value == 0:
            text = fnt.render(str(self.value), 1, WHITE)
            window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        # Draw Selected
        if self.selected:
            pygame.draw.rect(window, ORANGE, (x, y, gap, gap), 3)

        # Draw Game Over
        FONT = pygame.font.SysFont("comicsans", 70)
        if game_state == -1:
            title = FONT.render("Game Over", 1, RED)
            window.blit(title, (270 - title.get_width() / 2, 220))
        elif game_state == 1:
            title = FONT.render("You Win!!", 1, ORANGE)
            window.blit(title, (270 - title.get_width() / 2, 220))

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(window, board, playtime, strikes):
    window.fill(DARK)

    # Draw playtime
    fnt = pygame.font.SysFont("comicsans", 28)
    text = fnt.render(f"Time:  {format_time(playtime)}", 1, WHITE)
    window.blit(text, (540 - 190, 560))

    # Draw Strikes
    text = fnt.render("X " * strikes, 1, RED)
    window.blit(text, (20, 560))

    # Draw grid and board
    board.draw(window)


# format playtime to be shown in UI
def format_time(secs):
    second = secs % 60
    minute = secs // 60
    hour = minute // 60
    return f"{hour}:{minute}:{second}"


def main():
    global game_state
    game_state = 0
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")

    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    location = (0, 0)

    while run:
        if game_state == 0:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            if board.cubes[i][j].temp == 0:
                                print("Wrong")
                                strikes += 1
                        key = None

                        # Draw Game Over
                        if board.is_finished():
                            game_state = 1
                            print("You Won!!")
                        elif strikes > 5 or board.is_finished():
                            game_state = -1
                            print("Game Over")

                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_c:
                    temp = location
                    for row in range(9):
                        for col in range(9):
                            board.select(row, col)
                            board.clear()
                    location = temp
                    board.select(*temp)
                    key = None
                if event.key == pygame.K_r:
                    game_state = 0
                    key = None
                    run = True
                    strikes = 0
                    location = (0, 0)
                    start = time.time()
                if event.key == pygame.K_n:
                    newSolution, newBoard = generate_sudoku()
                    board.cubes = [[Cube(newBoard[i][j], i, j, 540, 540) for j in range(9)] for i in range(9)]
                    board.model = None
                    board.selected = None
                    board.solution = newSolution
                    game_state = 0
                    key = None
                    run = True
                    strikes = 0
                    location = (0, 0)
                    start = time.time()
                if event.key == pygame.K_SPACE:
                    temp = location
                    for row in range(9):
                        for col in range(9):
                            key = board.solution[row][col]
                            board.select(row, col)
                            board.sketch(key)
                            # board.place(board.cubes[row][col].temp)
                    location = temp
                    board.select(*temp)
                    key = None
                    print_board(board.solution)
                if event.key == pygame.K_i:
                    print(f'\n{INSTRUCTION}\n')

                if event.key == pygame.K_UP:
                    y_pos = (location[0] - 1) % 9
                    location = board.select(y_pos, location[1])
                    key = None
                if event.key == pygame.K_DOWN:
                    y_pos = (location[0] + 1) % 9
                    location = board.select(y_pos, location[1])
                    key = None
                if event.key == pygame.K_RIGHT:
                    x_pos = (location[1] + 1) % 9
                    location = board.select(location[0], x_pos)
                    key = None
                if event.key == pygame.K_LEFT:
                    x_pos = (location[1] - 1) % 9
                    location = board.select(location[0], x_pos)
                    key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    location = board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        # if game_state == 0:
        redraw_window(window, board, play_time, strikes)
        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()