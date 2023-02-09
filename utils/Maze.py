from random import randint, choice

# 0 = EMPTY, 1 = BLOCK
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [
            [0 for _ in range(width)] 
               for _ in range(height)
        ]

    def random_position(self, x_range, y_range):
        x, y = randint(*x_range), randint(*y_range)
        return x, y

    def reset_map(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.set_map(x, y, value)

    def set_map(self, x, y, value):
        self.map[y][x] = value

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_movable(self, x, y):
        return self.map[y][x] != 1

    def check_adjacent(self, x, y, checklist):
        width = (self.width - 1) // 2
        height = (self.height - 1) // 2
        directions = []
        if x > 0 and not self.is_movable(2 * (x - 1) + 1, 2 * y + 1):
            directions.append("left")
        if y > 0 and not self.is_movable(2 * x + 1, 2 * (y - 1) + 1):
            directions.append("up")
        if x < width - 1 and not self.is_movable(2 * (x + 1) + 1, 2 * y + 1):
            directions.append("right")
        if y < height - 1 and not self.is_movable(2 * x + 1, 2 * (y + 1) + 1):
            directions.append("down")

        if directions:
            direction = choice(directions)
            if direction == "left":
                self.set_map(2 * (x - 1) + 1, 2 * y + 1, 0)
                self.set_map(2 * x, 2 * y + 1, 0)
                checklist.append((x - 1, y))
            elif direction == "up":
                self.set_map(2 * x + 1, 2 * (y - 1) + 1, 0)
                self.set_map(2 * x + 1, 2 * y, 0)
                checklist.append((x, y - 1))
            elif direction == "right":
                self.set_map(2 * (x + 1) + 1, 2 * y + 1, 0)
                self.set_map(2 * x + 2, 2 * y + 1, 0)
                checklist.append((x + 1, y))
            elif direction == "down":
                self.set_map(2 * x + 1, 2 * (y + 1) + 1, 0)
                self.set_map(2 * x + 1, 2 * y + 2, 0)
                checklist.append((x, y + 1))
            return True

        # if not find any unvisited adjacent entry
        return False

    # '#' is wall and '.' is path
    def display_maze(self):
        for row in self.map:
            display = ["#" if cell == 1 else "." for cell in row]
            print("".join(display))
        print()

    # random prim algorithm
    def random_prim(self, width, height):
        x, y = self.random_position((0, width - 1), (0, height - 1))
        self.set_map(2 * x + 1, 2 * y + 1, 0)

        checklist = [(x, y)]
        print(f"start = {checklist[0][0] + 1, checklist[0][1] + 1}")

        # select a random entry from checklist
        while checklist:
            entry = choice(checklist)

            # the entry has no unvisited adjacent entry, so remove it from checklist
            if not self.check_adjacent(entry[0], entry[1], checklist):
                checklist.remove(entry)


def generate_maze(width, height):
    maze = Map(width, height)
    maze.reset_map(1)
    maze.random_prim((width - 1) // 2, (height - 1) // 2)

    # maze.display_maze()
    return maze.map


if __name__ == "__main__":
    width, height = 25, 25
    maze = generate_maze(width, height)