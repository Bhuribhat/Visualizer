""" 
Given n non-negative integers a1, a2, ..., an, 
where each represents a height of each vertical lines (i, ai),
Find 2 lines which together with the x-axis forms a container with the most water """

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tkinter import *
from scipy import stats
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
YELLOW = "#fece2f"
PURPLE = "#8B5CF6"
DARKER = "#111827"
DARK   = "#1F2937"
GRAY   = "#545454"
WHITE  = "#FFFFFF"

y_points = []
last_action = None

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
        self["activebackground"] = DARK
        self["disabledforeground"] = DARK

        self.bind('<Enter>', lambda e: self.config(background=PURPLE))
        self.bind('<Leave>', lambda e: self.config(background=GRAY))


# Time Complexity: O(n)
def find_max_area(heights):
    max_area = 0
    left, right = 0, len(heights) - 1

    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        
        if area > max_area:
            max_area = area
            optimal_left = left
            optimal_right = right
            optimal_height = height

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area, optimal_left ,optimal_right ,optimal_height


# Plot all points and regression line
def plot_graph(y_points, annotate, draw_water):
    if len(y_points):
        figure.clear()

        AX = figure.add_subplot()
        AX.set_facecolor(DARKER)
        AX.tick_params(axis = 'x', colors = 'white')
        AX.tick_params(axis = 'y', colors = 'white')
        AX.xaxis.set_major_locator(MaxNLocator(integer=True))

        # find max area (rectangle)
        area, left, right, height = find_max_area(y_points)
        title = f'Max Area = {right - left} x {height:.0f} = {area:,.0f}'
        print(f"\nMax Area = {area:.2f}, height = {height:.2f}")
        print(f"Start histogram = {left  + 1}")
        print(f"End histogram   = {right + 1}")

        # plot histogram
        data = pd.DataFrame({
            "x": range(1, len(y_points) + 1),
            "y": y_points
        })
        plt.bar(data['x'], data['y'], color='red', alpha=0.6, align='center')

        # draw water in the container
        if draw_water == True:
            AX.add_patch(Rectangle((
                left + 1, 0), right - left, height, 
                color='lightskyblue', alpha=0.3
            ))
            plt.bar(data['x'][left],  data['y'][left],  color='lightskyblue', align='center')
            plt.bar(data['x'][right], data['y'][right], color='lightskyblue', align='center')

        # annotate height for each histogram
        if annotate == True and len(y_points) <= 80:
            x = 1
            fontsize = 10 - (len(y_points) // 20)

            for height in y_points:
                plt.annotate(f"{height:.0f}",
                    xy = (x, height),                # top left corner of the histogram bar
                    xytext = (0, 0.3),               # offsetting label position above its bar
                    textcoords = "offset points",    # offset (in points) from the *xy* value
                    ha = 'center', va = 'bottom', 
                    color = 'white', fontsize = fontsize
                )
                x += 1

        max_height = max(y_points)
        AX.set_title(title, color = YELLOW, fontsize = 14)
        AX.set_ylim(top = max_height + 10 * (len(str(max_height)) - 1))

    canvas.draw_idle()


# Plot random histogram
def random_plot():
    global y_points
    N = np.random.randint(5, 100)
    y_points = np.random.randint(0, 100, size=N)
    y_points = list(y_points)
    plot_graph(y_points, annotate.get(), draw_water.get())


# Plot random normal distribution histogram (law of large number)
def normal_plot():
    figure.clear()

    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')

    N = np.random.randint(1000)

    # mean and standard deviation
    mu = np.random.randint(5, 30)
    sigma = np.random.randint(1, 10) / 10
    data = np.random.normal(mu, sigma, N)

    global y_points
    y_points, bins, _ = plt.hist(data, bins=30, histtype='bar', density=True, ec='k')
    plt.plot(
        bins, 
        1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - mu)**2 / (2 * sigma**2)),
        linewidth=2, color='red'
    )

    y_points = list(y_points)
    title = f"Mean = {np.mean(data):.2f}, STD = {np.std(data):.2f}"
    AX.set_title(title, color=YELLOW, fontsize=14)
    canvas.draw_idle()


# Add a Sigle or List of Points
def add_point(y_points):
    try:
        height = y_value.get()
        y_value.delete(0, END)
        if " " in height:
            add_y = list(map(float, height.split()))
            y_points += add_y
        else:
            y_points.append(int(height))

        plot_graph(y_points, annotate.get(), draw_water.get())
    except Exception as error:
        print(error)


# Clear Graph and Entry
def clear(y_points):
    y_points.clear()
    y_value.delete(0, END)

    figure.clear()
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')
    AX.set_title(f'Histogram', color = YELLOW, fontsize = 14)

    canvas.draw_idle()


# Set annotate to display or not display
def set_annotate(y_points):
    global annotate, draw_water
    print(f"Annotate = {annotate.get()}")
    print(f"Draw Water = {draw_water.get()}")
    plot_graph(y_points, annotate.get(), draw_water.get())


# Pop the last index of height array
def pop_height(y_points):
    global last_action
    if len(y_points) == 0: return
    last_action = y_points.pop()
    plot_graph(y_points, annotate.get(), draw_water.get())


# Append last_action element of undo action to height array
def redo_action(y_points):
    if last_action is None: return
    y_points.append(last_action)
    plot_graph(y_points, annotate.get(), draw_water.get())


if __name__ == '__main__':
    ROOT = Tk()
    ROOT.title("Container with most water")
    ROOT.resizable(0, 0)
    ROOT.configure(background=DARKER)
    ROOT.bind('<Escape>', lambda e: ROOT.quit())

    # Data Points and Graph Canvas
    text = StringVar()
    Label(ROOT, text="Enter Height:", pady=20, font=10, fg="white", bg=DARKER).grid(row=0, column=0, sticky="news")
    y_value = Entry(ROOT, font=10, width=60, textvariable=text, fg=YELLOW, bg=DARK)
    y_value.configure(insertbackground="orange")
    y_value.grid(row=0, column=1, pady=20, sticky="news")

    add_button = HooverButton(ROOT, text="Add", command=lambda: add_point(y_points))
    add_button.grid(row=0, column=2, pady=20, padx=10, sticky="news")

    # Add main menu
    main_menu = Menu(ROOT)

    annotate = BooleanVar()
    draw_water = BooleanVar()

    annotate.set(True)
    draw_water.set(True)

    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label="New", command=lambda: clear(y_points))
    file_menu.add_command(label="Save", command=lambda: plt.savefig('./asstes/Histogram.png'))
    file_menu.add_separator()
    file_menu.add_command(label="Undo", command=lambda: pop_height(y_points))
    file_menu.add_command(label="Redo", command=lambda: redo_action(y_points))

    edit_menu = Menu(main_menu, tearoff=0)
    edit_menu.add_checkbutton(label="Annotate", command=lambda: set_annotate(y_points), variable=annotate)
    edit_menu.add_checkbutton(label="Water", command=lambda: set_annotate(y_points), variable=draw_water)

    random_menu = Menu(main_menu, tearoff=0)
    random_menu.add_command(label="Random Histogram", command=lambda: random_plot())
    random_menu.add_command(label="Normal Distribution", command=lambda: normal_plot())

    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Setting", menu=edit_menu)
    main_menu.add_cascade(label="Random", menu=random_menu)
    ROOT.config(menu=main_menu)

    # Graph Canvas
    figure = plt.figure(figsize=(8, 4), facecolor=DARKER, dpi=100)
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')
    AX.set_title('Histogram', color = YELLOW, fontsize = 14)

    canvas = FigureCanvasTkAgg(figure, ROOT)
    canvas.get_tk_widget().grid(row=2, columnspan=3, sticky="news")

    ROOT.protocol("WM_DELETE_WINDOW", lambda: ROOT.quit())
    ROOT.mainloop()