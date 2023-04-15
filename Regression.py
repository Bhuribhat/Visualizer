import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tkinter import *
from sklearn.metrics import r2_score
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
YELLOW = "#fece2f"
PURPLE = "#8B5CF6"
DARKER = "#111827"
DARK   = "#1F2937"
GRAY   = "#545454"

x_points = []
y_points = []


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


# Choose Regression Model
def choose_linear():
    if linear_check.get() == 1:
        logistic.deselect()
        polynomial.deselect()

        figure.clear()
        AX = figure.add_subplot()
        AX.set_facecolor(DARKER)
        AX.tick_params(axis = 'x', colors = 'white')
        AX.tick_params(axis = 'y', colors = 'white')
        AX.set_title('Linear Regression', color = YELLOW, fontsize = 14)

        N = len(x_points)
        colors = np.random.randint(100, size=(N))
        plt.scatter(x_points, y_points, c = colors, cmap = 'viridis')
        if N >= 2:
            A, B = leastRegLine(x_points, y_points, N)
            x = np.linspace(min(x_points), max(x_points), 100)
            y = A + B * x
            plt.plot(x, y, color = 'deepskyblue')
            AX.set_title(f'Y = {A:.2f} + {B:.2f}X', color = YELLOW, fontsize = 14)

        canvas.draw_idle()


def choose_logistic():
    if logistic_check.get() == 1:
        linear.deselect()
        polynomial.deselect()

        figure.clear()
        AX = figure.add_subplot()
        AX.set_facecolor(DARKER)
        AX.tick_params(axis = 'x', colors = 'white')
        AX.tick_params(axis = 'y', colors = 'white')
        AX.set_title('Logistic Regression', color = YELLOW, fontsize = 14)

        try:
            if any(i > 1 for i in y_points) or any(i < 0 for i in y_points):
                raise Exception("Wrong Y values")
            N = len(x_points)
            plt.ylim(0, 1)
            data = pd.DataFrame(list(zip(x_points, y_points)), columns=["X", "Y"])
            if N >= 2:
                sns.regplot(x=x_points, y=y_points, data=data, logistic=True, ci=None, marker="+",
                            scatter_kws={'color': 'orange'}, line_kws={'color': 'deepskyblue'})
        except Exception as error:
            print("Error:", error)
            AX.set_title(f'Y must be between 0 and 1', color = 'red', fontsize = 14)

        canvas.draw_idle()


def choose_polynomial():
    if polynomial_check.get() == 1:
        linear.deselect()
        logistic.deselect()

        figure.clear()
        AX = figure.add_subplot()
        AX.set_facecolor(DARKER)
        AX.tick_params(axis = 'x', colors = 'white')
        AX.tick_params(axis = 'y', colors = 'white')
        AX.set_title('Polynomial Regression', color = YELLOW, fontsize = 14)

        N = len(x_points)
        colors = np.random.randint(100, size=(N))
        plt.scatter(x_points, y_points, c = colors, cmap = 'viridis')
        if N >= 2:
            model = np.poly1d(np.polyfit(x_points, y_points, 3))
            line = np.linspace(min(x_points), max(x_points), 100)
            r2 = r2_score(y_points, model(x_points))
            AX.set_title(f'R-Squared = {r2:.2f}', color = YELLOW, fontsize = 14)
            plt.plot(line, model(line), color = 'deepskyblue')

        canvas.draw_idle()


# Function to calculate B
def coefficientB(x, y, n):
    sum_X = sum(x)
    sum_Y = sum(y)
    product_XY = 0
    sum_X2 = 0
    for i in range(n):
        product_XY += x[i] * y[i]
        sum_X2 += x[i] * x[i]
    return (n * product_XY - sum_X * sum_Y) / \
           (n * sum_X2 - sum_X * sum_X)


# Function to find the least regression line
def leastRegLine(X, Y, n):
    B = coefficientB(X, Y, n)
    meanX = sum(X) / n
    meanY = sum(Y) / n
    A = meanY - B * meanX
    print(f"Y = {A:.3f} + {B:.3f}X")
    return A, B


# Plot all points and regression line
def plot_graph(x_points, y_points):
    figure.clear()
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')

    if linear_check.get() == 1:
        AX.set_title('Linear Regression', color = YELLOW, fontsize = 14)
    elif logistic_check.get() == 1:
        AX.set_title('Logistic Regression', color = YELLOW, fontsize = 14)
    else:
        AX.set_title('Polynomial Regression', color = YELLOW, fontsize = 14)

    # plot data and regression line
    N = len(x_points)
    if linear_check.get() == 1 or polynomial_check.get() == 1:
        colors = np.random.randint(100, size=(N))
        plt.scatter(x_points, y_points, c = colors, cmap = 'viridis')

    if N >= 2:
        if linear_check.get() == 1:
            A, B = leastRegLine(x_points, y_points, N)
            x = np.linspace(min(x_points), max(x_points), 100)
            y = A + B * x
            plt.plot(x, y, color = 'deepskyblue')
            AX.set_title(f'Y = {A:.2f} + {B:.2f}X', color = YELLOW, fontsize = 14)

        elif logistic_check.get() == 1:
            try:
                if any(i > 1 for i in y_points) or any(i < 0 for i in y_points):
                    raise Exception("Wrong Y values")
                plt.ylim(0, 1)
                data = pd.DataFrame(list(zip(x_points, y_points)), columns=["X", "Y"])
                sns.regplot(x=x_points, y=y_points, data=data, logistic=True, ci=None, marker="+",
                            scatter_kws={'color': 'orange'}, line_kws={'color': 'deepskyblue'})
            except Exception as error:
                print("Error:", error)
                AX.set_title(f'Y must be between 0 and 1', color = 'red', fontsize = 14)

        else:
            model = np.poly1d(np.polyfit(x_points, y_points, 3))
            line = np.linspace(min(x_points), max(x_points), 100)
            r2 = r2_score(y_points, model(x_points))
            AX.set_title(f'R-Squared = {r2:.2f}', color = YELLOW, fontsize = 14)
            plt.plot(line, model(line), color = 'deepskyblue')

    canvas.draw_idle()


# Add a Sigle or List of Points
def add_point(x_points, y_points):
    try:
        X = x_value.get()
        Y = y_value.get()
        x_value.delete(0, END)
        y_value.delete(0, END)
        if " " in X and " " in Y:
            add_x = list(map(float, X.split()))
            add_y = list(map(float, Y.split()))
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

    if linear_check.get() == 1:
        AX.set_title('Linear Regression', color = YELLOW, fontsize = 14)
    elif logistic_check.get() == 1:
        AX.set_title('Logistic Regression', color = YELLOW, fontsize = 14)
    else:
        AX.set_title('Polynomial Regression', color = YELLOW, fontsize = 14)

    canvas.draw_idle()


if __name__ == '__main__':
    ROOT = Tk()
    ROOT.title("Regression")
    ROOT.configure(background=DARKER)
    ROOT.bind('<Escape>', lambda e: ROOT.quit())

    # Model Selection and Save Button
    top_frame = LabelFrame(ROOT, text="Select", padx=5, pady=10, bg=DARKER, fg="orange", font=15)
    top_frame.grid(row=0, padx=10, pady=10)

    linear_check = IntVar()
    linear = CheckList(top_frame, text='Linear Model', variable=linear_check, command=choose_linear)
    linear.grid(row=0, column=0, padx=15, sticky="W")
    linear.select()

    logistic_check = IntVar()
    logistic = CheckList(top_frame, text='Logistic Model', variable=logistic_check, command=choose_logistic)
    logistic.grid(row=0, column=1, padx=15, sticky="W")

    polynomial_check = IntVar()
    polynomial = CheckList(top_frame, text='Polynomial Model', variable=polynomial_check, command=choose_polynomial)
    polynomial.grid(row=0, column=2, padx=15, sticky="W")

    save_button = HooverButton(top_frame, text="Save", command=lambda: plt.savefig('./assets/Regression.png'))
    save_button.grid(row=0, column=3, padx=15, sticky="news")

    # Data Points and Graph Canvas
    bottom_frame = LabelFrame(ROOT, text="Graph", padx=20, pady=10, bg=DARKER, fg="orange", font=15)
    bottom_frame.grid(row=1, columnspan=4, padx=10, pady=10)

    text = StringVar()
    Label(bottom_frame, text="Point X", padx=10, font=10, fg="white", bg=DARKER).grid(row=0, column=0, sticky="news")
    x_value = Entry(bottom_frame, font=10, width=46, textvariable=text, fg=YELLOW, bg=DARK)
    x_value.configure(insertbackground="orange")
    x_value.grid(row=0, column=1, sticky="news")

    text = StringVar()
    Label(bottom_frame, text="Point Y", padx=10, font=10, fg="white", bg=DARKER).grid(row=1, column=0, sticky="news")
    y_value = Entry(bottom_frame, font=10, width=46, textvariable=text, fg=YELLOW, bg=DARK)
    y_value.configure(insertbackground="orange")
    y_value.grid(row=1, column=1, sticky="news")

    add_button = HooverButton(bottom_frame, text="Add", command=lambda: add_point(x_points, y_points))
    add_button.grid(row=0, column=2, sticky="news", padx=10)

    clear_button = HooverButton(bottom_frame, text="Clear", command=lambda: clear(x_points, y_points))
    clear_button.grid(row=1, column=2, sticky="news", padx=10)

    # Graph Canvas
    figure = plt.figure(figsize=(5, 4), facecolor=DARKER, dpi=100)
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')
    AX.set_title('Linear Regression', color = YELLOW, fontsize = 14)

    canvas = FigureCanvasTkAgg(figure, bottom_frame)
    canvas.get_tk_widget().grid(row=2, columnspan=3, sticky="news")

    ROOT.protocol("WM_DELETE_WINDOW", lambda: ROOT.quit())
    ROOT.mainloop()