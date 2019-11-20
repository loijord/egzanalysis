import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d

class FunctionPlotter:
    def __init__(self, expression, xlim = (-10,10), ylim = (-10,10), step=1):
        x = sp.symbols('x')
        self.expression = expression
        self.function = sp.lambdify(x, self.expression, "math")
        self.xlim = xlim
        self.ylim = ylim
        self.step = step
        self.input = ''
        self.points = []

    def display(self):
        title = str(self.expression)
        fig = plt.figure(title)
        ax = fig.gca()

        #this draws axis:
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        plt.xticks(np.arange(self.xlim[0], self.xlim[1], step=self.step))
        plt.yticks(np.arange(self.ylim[0], self.ylim[1], step=self.step))

        fig.canvas.mpl_connect("key_press_event", lambda event: self.refresh_plot(fig, ax, event.key))
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)
        plt.grid()
        plt.show()

    def refresh_plot(self, fig, ax, key):
        if key == 'enter':
            try:
                argument = float(self.input.replace(',', '.'))
                format_is_right = True
            except ValueError('not a float'):
                format_is_right = False
            if format_is_right:
                self.points.append([argument, self.function(argument)])
                ax.scatter(*self.points[-1], color='blue')
                fig.canvas.draw()
            self.input = ''
        elif key == 'up':
            self.sketch(fig, ax)
        else:
            self.input += key

    def sketch(self, fig, ax):
        #connects points choosen to interpolate
        if len(self.points) > 1:
            x, y = np.array(self.points).T
            if len(self.points) > 3: f = interp1d(x, y, kind='cubic', fill_value="extrapolate")
            elif len(self.points) > 2: f = interp1d(x, y, kind='quadratic', fill_value="extrapolate")
            elif len(self.points) > 1: f = interp1d(x, y, kind='linear', fill_value="extrapolate")

            arguments = np.arange(min(x)-self.step, max(x)+self.step, self.step/100)
            values = f(arguments)
            ax.plot(arguments, values)
            fig.canvas.draw()


functionplotter = FunctionPlotter('sin(x)', xlim = (-10,10), ylim = (-10,10), step=1)
functionplotter.display()

