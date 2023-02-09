import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    YELLOW = 255, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = BLACK

    GRADIENTS = [
        (70, 118, 155),
        (47, 95, 138),
        (23, 73, 120)
    ]

    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    FONT = pygame.font.SysFont('comicsans', 20)
    SMALL_FONT = pygame.font.SysFont('comicsans', 15)

    SIDE_PAD = 75
    TOP_PAD = 145

    def __init__(self, width, height, lst):
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        
        self.height = height
        self.width = width
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

# draw font and list animation
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.YELLOW)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 55))

    algo1 = "I - Insertion Sort | B - Bubble Sort | S - Selection Sort | E - Shell Sort"
    algo2 = "H - Heap Sort | M - Merge Sort | Q - Quick Sort"
    sorting1 = draw_info.SMALL_FONT.render(algo1, 1, draw_info.WHITE)
    sorting2 = draw_info.SMALL_FONT.render(algo2, 1, draw_info.WHITE)
    draw_info.window.blit(sorting1, (draw_info.width / 2 - sorting1.get_width() / 2, 90))
    draw_info.window.blit(sorting2, (draw_info.width / 2 - sorting2.get_width() / 2, 110))

    draw_list(draw_info)
    pygame.display.update()

# draw list animation
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg: pygame.display.update()

# Generate random number for sorting
def generate_starting_list(N, min_val, max_val):
    lst = []
    for _ in range(N):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

""" Time Complexity: O(n * n) worst case if reverse sort | Best Case : O(n) """
def bubble_sort(draw_info, ascending=True):
    data = draw_info.lst

    for i in range(len(data) - 1):
        swapped = False
        for j in range(len(data) - 1 - i):
            num1 = data[j]
            num2 = data[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True  # program will respond even when sorting
        
        if swapped == False: break

    return data

""" Time Complexity: O(n ^ 2) """
def insertion_sort(draw_info, ascending=True):
    data = draw_info.lst

    for i in range(1, len(data)):
        current = data[i]

        while True:
            ascending_sort  = i > 0 and data[i - 1] > current and ascending
            descending_sort = i > 0 and data[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort: break

            data[i] = data[i - 1]
            i = i - 1
            data[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return data

""" Time Complexity: O(n ^ 2) """
def selection_sort(draw_info, ascending=True):
    data = draw_info.lst
    if len(data) == 1: return

    # Find minimum unsorted value
    for i in range(len(data)):
        minVal = data[i]
        minIdx = i
        for j in range(i, len(data)):
            if (data[j] < minVal and ascending) or (data[j] > minVal and not ascending):
                minVal = data[j]
                minIdx = j
            draw_list(draw_info, {j: draw_info.GREEN, minIdx: draw_info.RED}, True)
            yield True
        data[i], data[minIdx] = data[minIdx], data[i]
        draw_list(draw_info, {i: draw_info.GREEN, minIdx: draw_info.RED}, True)
        yield True
    
    return data

""" Time Complexity: O(n log(n)) """
def merge_sort(draw_info, ascending=True):
    data = draw_info.lst
    return mergesort(draw_info, data, 0, len(data) - 1, ascending)

def mergesort(draw_info, data, start, end, ascending):
    if end <= start: return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(draw_info, data, start, mid, ascending)
    yield from mergesort(draw_info, data, mid + 1, end, ascending)
    yield from merge(draw_info, data, start, mid, end, ascending)
    yield data

# Helper function for merge sort
def merge(draw_info, data, start, mid, end, ascending):
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if ascending:
            if data[leftIdx] < data[rightIdx]:
                merged.append(data[leftIdx])
                leftIdx += 1
            else:
                merged.append(data[rightIdx])
                rightIdx += 1
        else:
            if data[leftIdx] > data[rightIdx]:
                merged.append(data[leftIdx])
                leftIdx += 1
            else:
                merged.append(data[rightIdx])
                rightIdx += 1

    while (leftIdx <= mid):
        merged.append(data[leftIdx])
        leftIdx += 1

    while (rightIdx <= end):
        merged.append(data[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        data[start + i] = sorted_val
        draw_list(draw_info, {i: draw_info.GREEN, start + i: draw_info.RED}, True)
        yield True
    
    return merged

""" Time Complexity: O(n ^ 2) """
def quick_sort(draw_info, ascending=True):
    data = draw_info.lst
    return quicksort(draw_info, data, 0, len(data) - 1, ascending)

# helper function for quicksort
def quicksort(draw_info, data, start, end, ascending):
    if start >= end: return

    pivot = data[end]
    pivotIdx = start

    for i in range(start, end):
        if (data[i] < pivot and ascending) or (data[i] > pivot and not ascending):
            data[i], data[pivotIdx] = data[pivotIdx], data[i]
            pivotIdx += 1
        draw_list(draw_info, {i: draw_info.GREEN, pivotIdx: draw_info.RED}, True)
        yield True
    data[end], data[pivotIdx] = data[pivotIdx], data[end]
    draw_list(draw_info, {i: draw_info.GREEN, pivotIdx: draw_info.RED}, True)
    yield True

    yield from quicksort(draw_info, data, start, pivotIdx - 1, ascending)
    yield from quicksort(draw_info, data, pivotIdx + 1, end, ascending)

""" Time Complexity: O(n ^ 2) """
def shell_sort(draw_info, ascending=True):
    data = draw_info.lst
    gap = len(data) // 2
    while gap > 0:
        for i in range(gap, len(data)):
            temp = data[i]
            pos = i
            while True:
                ascending_sort  = pos >= gap and data[pos - gap] > temp and ascending
                descending_sort = pos >= gap and data[pos - gap] < temp and not ascending
                if not ascending_sort and not descending_sort: break
                data[pos] = data[pos - gap]
                pos -= gap
            data[pos] = temp
            draw_list(draw_info, {i: draw_info.GREEN, pos: draw_info.RED}, True)
            yield True
        gap //= 2
    return data

""" Time Complexity: O(n log(n)) """
def heap_sort(draw_info, ascending=True):
    data = draw_info.lst
    N = len(data)
    for i in range((N // 2) - 1, -1, -1):
        heapify(data, N, i, ascending)
        draw_list(draw_info, {i: draw_info.GREEN}, True)
        yield True
    for pos in range(N - 1, -1, -1):
        data[0], data[pos] = data[pos], data[0]
        heapify(data, pos, 0, ascending)
        draw_list(draw_info, {0: draw_info.GREEN, pos: draw_info.RED}, True)
        yield True
    return data

# helper function for heap sort (fix down)
def heapify(data, size, idx, ascending):
    temp = data[idx]
    child = 2 * idx + 1
    while child < size:
        ascending_sort  = child + 1 < size and data[child] < data[child + 1] 
        descending_sort = child + 1 < size and data[child] > data[child + 1] 
        check_order = (ascending_sort and ascending) or (descending_sort and not ascending)
        if (check_order): child += 1
        if (data[child] < temp and ascending): break
        if (data[child] > temp and not ascending): break
        data[idx] = data[child]
        idx = child
        child = 2 * idx + 1
    data[idx] = temp

def main():
    run = True
    clock = pygame.time.Clock()

    N = 50
    MIN_VAL = 1
    MAX_VAL = 100

    data = generate_starting_list(N, MIN_VAL, MAX_VAL)
    draw_info = DrawInformation(800, 600, data)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type != pygame.KEYDOWN: continue
            if event.key == pygame.K_r:
                data = generate_starting_list(N, MIN_VAL, MAX_VAL)
                draw_info.set_list(data)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                sorting = True
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_e and not sorting:
                sorting_algorithm = shell_sort
                sorting_algo_name = "Shell Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

    pygame.quit()

if __name__ == "__main__":
    main()