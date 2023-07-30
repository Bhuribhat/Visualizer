import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
YELLOW = "#fece2f"
PURPLE = "#8B5CF6"
DARKER = "#111827"
DARK   = "#1F2937"
GRAY   = "#545454"


class HooverButton(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self["borderwidth"] = 0
        self["font"] = 7
        self["width"] = 10
        self["fg"] = "white"
        self["bg"] = GRAY
        self["cursor"] = "hand2"
        self["activeforeground"] = "white"
        self["activebackground"] = DARKER
        self["disabledforeground"] = DARKER

        self.bind('<Enter>', lambda e: self.config(background=PURPLE))
        self.bind('<Leave>', lambda e: self.config(background=GRAY))


# All primes greater than 3 can be written in the form of 6k ± 1
def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    w = 2

    # Primes are in the form of 6k ± 1
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w

    return True


def get_number():
    try:
        number = int(entry.get().strip())
        return number
    except ValueError:
        result_label.config(text="Please enter a number with base 10.", fg="red")
        return False


def format_factors(prime_factors):
    number = get_number()

    primes = []
    exponents = []

    factor_string = ''
    for factor in prime_factors:
        exponent = 1
        while number % (factor ** exponent) == 0:
            exponent += 1
        
        # math_expression = '{' + str(exponent - 1) + '}'
        factor_string += f" ({factor}^{exponent - 1}) x"

        primes.append(factor)
        exponents.append(exponent - 1)

    if factor_string:
        result_label.config(text=f"{number} = {factor_string[1:-1]}", fg=YELLOW)
    elif number >= 1:
        result_label.config(text=f"{number} = 1 x {number}", fg=YELLOW)
    else:
        result_label.config(text="Please Enter a Positive Number!", fg='red')

    return primes, exponents


def plot_factors():
    figure.clear()
    number = get_number()
    if number == False:
        return

    factors = [i for i in range(2, number // 2 + 1) if number % i == 0]
    prime_factors = [i for i in factors if is_prime(i)]

    if is_prime(number):
        print(f"{number} is a prime number")
        result_label.config(text=f"{number} = 1 x {number}", fg=YELLOW)
        primes, exponents = [1, number], [1, 1]
        format_color = "red"
    else:
        print(f'{number} is NOT a prime number')
        primes, exponents = format_factors(prime_factors)
        format_color = "lime"

    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis='x', colors='white')
    AX.tick_params(axis='y', colors='white')
    AX.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.bar(primes, exponents)

    fontsize = 10 - (len(exponents) // 20)
    for x, y in zip(primes, exponents):
        plt.annotate(f"{y}",
            xy=(x, y),
            xytext=(0, 0.3),
            textcoords="offset points",
            ha='center', va='bottom',
            color=PURPLE, fontsize=fontsize
        )

    plt.xlabel('Prime Factors', color='white')
    plt.ylabel('Exponents', color='white')
    plt.title(f"Prime Factors of {number}", color=PURPLE, fontsize=14)
    plt.yticks([])

    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw_idle()


if __name__ == '__main__':
    ROOT = tk.Tk()
    ROOT.title("Prime Factors Visualization")
    ROOT.configure(background=DARKER)
    ROOT.geometry("550x500")
    ROOT.resizable(0, 0)
    ROOT.bind('<Escape>', lambda e: ROOT.quit())

    input_frame = tk.Frame(ROOT, bg=DARKER)
    input_frame.pack(pady=10)

    number_label = tk.Label(input_frame, text="Enter number:", bg=DARKER, fg='white')
    number_label.pack(side=tk.LEFT)

    entry = tk.Entry(input_frame, bg=DARKER, fg='yellow', font=('Arial', 12), width=22)
    entry.configure(insertbackground="orange")
    entry.pack(side=tk.LEFT)

    button = HooverButton(input_frame, text="Plot Factors", command=plot_factors)
    button.pack(side=tk.LEFT, padx=10)

    result_label = tk.Label(ROOT, text="Please enter your number!", bg=DARKER, fg=YELLOW, font=('Arial', 12))
    result_label.pack(pady=10)

    plot_frame = tk.Frame(ROOT, bg=DARKER)
    plot_frame.pack(pady=0)

    # Graph Canvas
    figure = plt.figure(figsize=(5, 4), facecolor=DARKER, dpi=100)
    AX = figure.add_subplot()
    AX.set_facecolor(DARKER)
    AX.tick_params(axis = 'x', colors = 'white')
    AX.tick_params(axis = 'y', colors = 'white')

    plt.xticks([])
    plt.yticks([])

    canvas = FigureCanvasTkAgg(figure, plot_frame)
    canvas.get_tk_widget().grid(row=2, columnspan=3, sticky="news")

    ROOT.protocol("WM_DELETE_WINDOW", lambda: ROOT.quit())
    ROOT.mainloop()
