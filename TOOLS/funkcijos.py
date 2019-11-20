import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

class FunctionPlotter:
    def __init__(self, expression, xlim = (-10,10), ylim = (-10,10), step=1):
        x = sp.symbols('x')
        self.expression = expression
        self.function = sp.lambdify(x, self.expression, "math")
        self.xlim = xlim
        self.ylim = ylim
        self.step = step
        self.input = ''
        self.arguments = []

    def display(self):
        title = str(self.expression)
        fig = plt.figure(title)
        ax = fig.gca()

        #this draws axis:
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        #ax.xaxis.set_ticks_position('bottom')
        #ax.yaxis.set_ticks_position('left')
        plt.xticks(np.arange(self.xlim[0], self.xlim[1], step=self.step))
        plt.yticks(np.arange(self.ylim[0], self.ylim[1], step=self.step))

        fig.canvas.mpl_connect("key_press_event", lambda event: self.refresh_plot(fig, ax, event.key))
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)

        plt.show()

    def refresh_plot(self, fig, ax, key):
        if key == 'enter':
            try: argument = float(self.input.replace(',','.'))
            except ValueError('wrong input'): self.input = ''
            ax.scatter(argument, self.function(argument), color='blue')
            fig.canvas.draw()
            self.input = ''
        else:
            self.input += key

functionplotter = FunctionPlotter('sin(x)', xlim = (-10,10), ylim = (-10,10), step=1)
functionplotter.display()