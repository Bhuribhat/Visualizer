""" 
You are given an array points representing integer coordinates 
of some points on a 2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: 
|xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. 
All points are connected if there is exactly one simple path between any two points. """

import heapq
import numpy as np
import matplotlib.pyplot as plt

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
YELLOW = "#fece2f"
PURPLE = "#8B5CF6"
DARKER = "#111827"
DARK   = "#1F2937"
GRAY   = "#545454"
WHITE  = "#FFFFFF"

x_points = []
y_points = []

SIZE = 80
last_action = [None, None]

# define function for calculate distance
manhattan = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class CheckList(Checkbutton):
    def __init__(self, *args, **kwargs):
        Checkbutton.__init__(self, *args, **kwargs)
        self["font"] = 5
        self["onvalue"]  = 1
        self["offvalue"] = 0
        self["fg"] = "white"
        self["bg"] = DARKER
        self["cursor"] = "target"
        self["selectcolor"] = DARKER
        self["activeforeground"] = "white"
        self["activebackground"] = DARKER


class HooverButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["borderwidth"] = 0
        self["font"] = 7
        self["width"] = 7
        self["fg"] = "white"
        self["bg"] = GRAY
        self["cursor"] = "hand2"
        self["activeforeground"] = "white"
        self["activebackground"] = DARKER
        self["disabledforeground"] = DARKER

        self.bind('<Enter>', lambda e: self.config(background=PURPLE))
        self.bind('<Leave>', lambda e: self.config(background=GRAY))


# Prim's Algorithm to find cost (Minimum Spanning Tree)
def min_cost_connect_points(points: list[list[int]]) -> int:
    min_cost  = 0
    priorityQ = [(0, tuple(points[0]))]
    to_visit  = set([tuple(pos) for pos in points])

    while priorityQ:
        current_cost, current_node = heapq.heappop(priorityQ)
        if current_node not in to_visit:
            continue

        to_visit.remove(current_node)
        min_cost += current_cost

        if len(to_visit) == 0:
            break
        for neighbor in to_visit:
            cost = manhattan(current_node, neighbor)
            heapq.heappush(priorityQ, (cost, neighbor))

    return min_cost


# Prim's Algorithm to find edges (Minimum Spanning Tree)
def minimum_spanning_tree(points: list[list[int]]) -> list[list[int]]:
    edges = []
    visited = set([tuple(points[0])])

    heap = [
        (manhattan(points[0], pos), tuple(points[0]), tuple(pos)) 
        for pos in points[1:]
    ]
    heapq.heapify(heap)
    
    while heap:
        (cost, node1, node2) = heapq.heappop(heap)
        if node2 not in visited:
            visited.add(node2)
            edges.append([node1, node2])
            for pos in points:
                if tuple(pos) not in visited:
                    neighbor_cost = manhattan(tuple(pos), node2)
                    heapq.heappush(heap, (neighbor_cost, node2, tuple(pos)))
    return edges


# Annotate cost for each edges in MST
def annotate_edges(edges):
    for edge in edges:
        x1, y1 = edge[0]
        x2, y2 = edge[1]

        bbox = dict(
            boxstyle='round,pad=0.3', lw=0.75, 
            fc=DARK, ec='white'
        )

        plt.annotate(
            f"{manhattan(edge[0], edge[1]):.1f}",
            ((x1 + x2) / 2, (y1 + y2) / 2),
            ha = 'center',
            va = 'center',
            bbox = bbox,
            fontsize = 8,
            color = 'white'
        )


# Plot all points and regression line
def plot_graph(x_points, y_points):
    figure.clear()
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')
    print("\nMinimum Spanning Tree:")

    points = list(zip(x_points, y_points))
    edges = minimum_spanning_tree(points)
    for edge in edges:
        cost = manhattan(edge[0], edge[1])
        cost = round(cost) if int(cost) == cost else round(cost, 2)
        print(f"{str(edge[0]):<10} - {str(edge[1]):<10} -> {cost = }")

    minCost = min_cost_connect_points(points)
    minCost = round(minCost) if int(minCost) == minCost else round(minCost, 2)
    AX.set_title(f"Minimum Cost is {minCost}", color = YELLOW)

    # plot edges
    for edge in edges:
        x = [edge[0][0], edge[1][0]]
        y = [edge[0][1], edge[1][1]]
        plt.plot(x, y, color="lightskyblue")

    # plot graph x and y
    size = [SIZE for _ in range(len(x_points))]
    plt.scatter(x_points, y_points, color="orange", s=size)

    # text cost annotate
    annotate_edges(edges)
    canvas.draw_idle()


# Add a Sigle or List of Points
def add_point(x_points, y_points):
    try:
        X = x_value.get()
        Y = y_value.get()
        x_value.delete(0, END)
        y_value.delete(0, END)
        if " " in X and " " in Y:
            add_x = list(map(int, X.split()))
            add_y = list(map(int, Y.split()))
            if len(add_x) == len(add_y):
                x_points += add_x
                y_points += add_y
            else:
                raise ValueError("X and Y must have same dimension")
        elif " " in X or " " in Y:
            raise ValueError("X and Y must have same dimension")
        else:
            x_points.append(int(X))
            y_points.append(int(Y))

        plot_graph(x_points, y_points)
    except Exception as error:
        print(error)


# Clear Graph and Entry
def clear(x_points, y_points):
    x_points.clear()
    y_points.clear()
    x_value.delete(0, END)
    y_value.delete(0, END)

    figure.clear()
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')
    AX.set_title(
        "Minimum Cost to Connect All Points", 
        color = YELLOW, fontsize = 12
    )

    canvas.draw_idle()


# random plot MST
def random_plot():
    global x_points, y_points
    n_points = np.random.randint(5, 15)
    x_points = np.random.randint(0, 100, size=n_points)
    y_points = np.random.randint(0, 100, size=n_points)
    x_points = list(x_points)
    y_points = list(y_points)
    plot_graph(x_points, y_points)


# Pop the last index of array
def pop_last(x_points, y_points):
    global last_action
    if len(x_points) == 0: return
    if len(y_points) == 0: return
    last_action[0] = x_points.pop()
    last_action[1] = y_points.pop()
    plot_graph(x_points, y_points)


# Append last_action element of undo action to array
def redo_action(x_points, y_points):
    if last_action is [None, None]: return
    x_points.append(last_action[0])
    y_points.append(last_action[1])
    plot_graph(x_points, y_points)


if __name__ == '__main__':
    ROOT = Tk()
    ROOT.title("Minimum Spanning Tree")
    ROOT.resizable(0, 0)
    ROOT.configure(background=DARKER)
    ROOT.bind('<Escape>', lambda e: ROOT.quit())

    # Add main menu
    main_menu = Menu(ROOT)

    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label="New", command=lambda: clear(x_points, y_points))
    file_menu.add_command(label="Save", command=lambda: plt.savefig('./assets/MST.png'))
    file_menu.add_separator()
    file_menu.add_command(label="Undo", command=lambda: pop_last(x_points, y_points))
    file_menu.add_command(label="Redo", command=lambda: redo_action(x_points, y_points))

    edit_menu = Menu(main_menu, tearoff=0)
    edit_menu.add_command(label="Random MST", command=lambda: random_plot())

    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Edit", menu=edit_menu)
    ROOT.config(menu=main_menu)

    # Data Points and Graph Canvas
    text = StringVar()
    Label(ROOT, text="Point X", padx=10, pady=20, font=10, fg="white", bg=DARKER).grid(row=0, column=0, sticky="news")
    x_value = Entry(ROOT, font=10, width=60, textvariable=text, fg=YELLOW, bg=DARK)
    x_value.configure(insertbackground="orange")
    x_value.grid(row=0, column=1, pady=20, sticky="news")

    text = StringVar()
    Label(ROOT, text="Point Y", padx=10, pady=5, font=10, fg="white", bg=DARKER).grid(row=1, column=0, sticky="news")
    y_value = Entry(ROOT, font=10, width=60, textvariable=text, fg=YELLOW, bg=DARK)
    y_value.configure(insertbackground="orange")
    y_value.grid(row=1, column=1, pady=5, sticky="news")

    add_button = HooverButton(ROOT, text="Add", command=lambda: add_point(x_points, y_points))
    add_button.grid(row=0, column=2, sticky="ew", padx=10)

    clear_button = HooverButton(ROOT, text="Clear", command=lambda: clear(x_points, y_points))
    clear_button.grid(row=1, column=2, sticky="ew", padx=10)

    # Graph Canvas
    figure = plt.figure(figsize=(8, 6), facecolor=DARKER, dpi=100)
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')
    AX.set_title(
        "Minimum Cost to Connect All Points", 
        color = YELLOW, fontsize = 12
    )

    canvas = FigureCanvasTkAgg(figure, ROOT)
    canvas.get_tk_widget().grid(row=2, columnspan=3, sticky="news")

    ROOT.protocol("WM_DELETE_WINDOW", lambda: ROOT.quit())
    ROOT.mainloop()