import sys
import time
import heapq
import random
import pygame

from queue import PriorityQueue
from utils.Maze import generate_maze


# Initial Game UI
pygame.init()

INF = sys.maxsize
ROWS = 50
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Visualizer")

# Initial Colors
BLACK     = (0, 0, 0)
GREEN     = (0, 100, 0)
DARK      = (49, 49, 49)
DARKER    = (33, 40, 45)
ORANGE    = (255, 165, 0)
RED       = (255, 128, 0)
YELLOW    = (255, 255, 0)
BLUE      = (0, 128, 255)
PURPLE    = (138, 91, 246)
TURQUOISE = (64, 224, 208)
GREY      = (129, 129, 129)
WHITE     = (255, 255, 255)

# Fonts used in UI
LARGE_FONT = pygame.font.SysFont('comicsans', 30)
SMALL_FONT = pygame.font.SysFont('comicsans', 20)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = GREY
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):   # already visited
        return self.color == ORANGE

    def is_open(self):     # will be considered
        return self.color == GREEN

    def is_barrier(self):  # obstacle
        return self.color == BLACK

    def is_start(self):
        return self.color == WHITE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = GREY

    def make_start(self):
        self.color = WHITE

    def make_closed(self):
        self.color = ORANGE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):   # shortest path
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():                    # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():                    # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  # other spot > current
        return False


# draw shortest path that's found by algorithm
def reconstruct_path(came_from, current, draw):
    global length
    while current in came_from:
        if came_from[current].is_start():
            return
        current = came_from[current]
        current.make_path()
        draw()
        length += 1
    length = length + 2


# Breath-First-Search Algorithm
def BFS(draw, grid, start, end):
    global stop, length
    queue = [(0, start)]
    came_from = dict()
    distance = {spot: INF for row in grid for spot in row}
    distance[start] = 0

    # track all items in Queue
    visited = {start}

    while queue:
        # close program before finish BFS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    stop = True
                    return
                if event.key == pygame.K_c:
                    return

        # current node
        dist, current = queue.pop(0)
        visited.remove(current)

        # found shortest path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        # all weights in grid is 1
        for neighbor in current.neighbors:
            temp_dist = distance[current] + 1  

            # find optimal path
            if temp_dist < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_dist
                if neighbor not in visited:
                    queue.append((distance[neighbor], neighbor))
                    visited.add(neighbor)
                    neighbor.make_open()

        # update grid
        draw()

        # close that node off and make it red
        if current != start:
            current.make_closed()

    # no path exist
    return False


# Shortest Path Algorithm
def Dijkstra(draw, grid, start, end):
    global stop, length
    queue = [(0, start)]
    came_from = dict()
    distance = {spot: INF for row in grid for spot in row}
    distance[start] = 0

    # track all items in Queue
    visited = {start}

    while queue:
        # close program before finish Dijkstra
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    stop = True
                    return
                if event.key == pygame.K_c:
                    return

        # current node
        dist, current = heapq.heappop(queue)
        visited.remove(current)
        if distance[current] < dist:
            continue

        # found shortest path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        # all weights in grid is 1
        for neighbor in current.neighbors:
            temp_dist = distance[current] + 1

            # find optimal path
            if temp_dist > distance[neighbor] + dist:
                temp_dist = distance[neighbor] + dist

            if temp_dist < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_dist
                if neighbor not in visited:
                    heapq.heappush(queue, (distance[neighbor], neighbor))
                    visited.add(neighbor)
                    neighbor.make_open()       # green

        # update grid
        draw()

        # close that node off and make it red
        if current != start:
            current.make_closed()

    # no path exist
    return False


# heuristic function: estimate distance from n to end node
def h(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(x1 - x2) + abs(y1 - y2)


# F(n) = h(n) + g(n): heauristic + shortest from start to n
def A_Star(draw, grid, start, end):
    global stop, length
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # (f_score, count, node)
    came_from = dict()
    g_score = {spot: INF for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: INF for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # track all items in PriorityQueue
    open_set_hash = {start}

    while not open_set.empty():
        # close program before finish the algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    stop = True
                    return
                if event.key == pygame.K_c:
                    return

        # current node
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # found shortest path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        # all weights in grid is 1
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            # find optimal path
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                heuristic = h(neighbor.get_pos(), end.get_pos())

                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        # update grid
        draw()

        # close that node off and make it red
        if current != start:
            current.make_closed()

    # no path exist
    return False


# initial grid
def make_grid(rows, width):
    grid = [[] for _ in range(rows)]
    gap = width // rows
    for i in range(rows):
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    for row in range(1, len(grid)):
        grid[row][8].make_barrier()
    return grid


# draw grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


# draw font and list animation
def draw_UI(window, algo_name, time, length):
    pygame.draw.rect(window, DARKER, (0, 0, WIDTH, 145))

    title = LARGE_FONT.render(f"{algo_name} | Shortest Path = {length} | Take {time} seconds", 1, BLUE)
    window.blit(title, (WIDTH / 2 - title.get_width() / 2, 5))

    controls = "R - Reset | SPACE - Show Result | Left Click - Create | Right Click - Delete"
    controls = SMALL_FONT.render(controls, 1, YELLOW)
    window.blit(controls, (WIDTH / 2 - controls.get_width() / 2, 60))

    algo = "A - A* | B - BFS | D - Dijkstra | C - Clear Path | N - Obstacle | M - Maze"
    path = SMALL_FONT.render(algo, 1, RED)
    window.blit(path, (WIDTH / 2 - path.get_width() / 2, 100))


# draw everything
def draw(win, grid, rows, width, name, timeUse, length):
    win.fill(GREY)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    draw_UI(win, name, timeUse, length)
    pygame.display.update()


# draw obstacle randomly
def random_obstacle(grid):
    for row in grid:
        for spot in row:
            rnd = random.randint(1, 4)
            if rnd == 4:
                spot.make_barrier()
    for row in range(len(grid)):
        if row == 0:
            continue
        grid[row][8].make_barrier()
    return grid


# get node position
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    global stop, length
    stop = False
    grid = make_grid(ROWS, width)
    start, end = (None, None)

    command = 'A'
    name = 'A*'

    timeUse = 0
    length = 0

    run = True
    while run:
        draw(win, grid, ROWS, width, name, timeUse, length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:   # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    print(f"start = {start.get_pos()}")

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    print(f"end = {end.get_pos()}")

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # SPACE BAR
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # pass draw function as argument to algorithm function
                    length = 0
                    startTime = time.time()
                    if command == 'A':
                        name = 'A*'
                        A_Star(lambda: draw(win, grid, ROWS, width, name, timeUse, length), grid, start, end)
                    elif command == 'B':
                        name = 'BFS'
                        BFS(lambda: draw(win, grid, ROWS, width, name, timeUse, length), grid, start, end)
                    else:
                        name = "Dijkstra"
                        Dijkstra(lambda: draw(win, grid, ROWS, width, name, timeUse, length), grid, start, end)

                    # display algorihm tme
                    endTime = time.time()
                    timeUse = round(endTime - startTime, 2)
                    print(f"{name} Algorithm took {timeUse} seconds")

                if event.key == pygame.K_r or stop:  # Restart
                    timeUse = 0
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    length = 0
                    stop = False

                if event.key == pygame.K_c:          # Clear path
                    for row in grid:
                        for spot in row:
                            if spot.is_start() or spot.is_end():
                                continue
                            if not spot.is_barrier():
                                spot.reset()

                if event.key == pygame.K_n:          # N - Generate new obstacles
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    grid = random_obstacle(grid)

                if event.key == pygame.K_m:          # M - Generate new Maze
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    maze = generate_maze(ROWS, ROWS)

                    for row in range(len(maze)):
                        for col in range(len(maze[row]) - 2):
                            if maze[row][col] == 1:
                                grid[row][col + 2].make_barrier()

                    # Handle right-side
                    for row in range(len(maze)):
                        if not grid[-3][row].is_barrier():
                            grid[-2][row].reset()

                if event.key == pygame.K_a:          # A - A*
                    command = 'A'
                    name = 'A*'
                    print(f"Now Using {name} Algorithm")

                if event.key == pygame.K_b:          # B - BFS
                    command = 'B'
                    name = 'BFS'
                    print(f"Now Using {name} Algorithm")

                if event.key == pygame.K_d:          # D - Dijkstra
                    command = 'D'
                    name = "Dijkstra"
                    print(f"Now Using {name} Algorithm")

    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH)