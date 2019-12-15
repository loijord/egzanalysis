import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import re
from scipy.interpolate import interp1d

class FunctionPlotter:
    def __init__(self, expression, xlim = (-10,10), ylim = (-10,10), step=1, shooting_const=0.5):
        x = sp.symbols('x')
        self.expression = expression
        self.function = sp.lambdify(x, self.expression, "numpy") #pythonic function coverted from symbolic expression
        self.xlim = xlim  #x limits of figure
        self.ylim = ylim  #y limits of figure
        self.step = step  #scaling of coordinates
        self.user_input = '' #input that is typed by keyboard until 'enter' hit
        self.coordinates = [] #numerical points
        self.coordinates_asarray = None
        self.sketches = []
        self.graph = None
        self.points = []
        self.shooting_const = shooting_const
        self.target = None
        self.shooting_direction = None
        self.shoots = 0


    def display(self):
        title = 'FUNKCIJA f(x) =' + str(self.expression)
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
            inp = self.user_input.replace(',', '.')
            if re.match(r'^-?\d+(?:\.\d+)?$', inp) is not None:
                argument = float(inp)
                self.add_point(fig, ax, argument)
            else:
                print(inp, 'is not a number')
            self.user_input = ''
        elif key == 'up':
            self.sketch(fig, ax)
        elif key == 'down':
            self.remove_sketch(fig)
        elif key == 'ctrl+up':
            self.plot(fig, ax)
        elif key == 'ctrl+down':
            self.remove_plot(fig)
        elif key == 'left':
            self.remove_point(fig)
        elif key == 'right':
            self.shoot_the_moon(fig, ax)
        else:
            self.user_input += key

        if key != 'right':
            self.shoots = 0

    def sketch(self, fig, ax):
        if self.coordinates_asarray is not None and self.coordinates_asarray.shape[1] > 1:
            order = np.argsort(self.coordinates_asarray[0])
            x, y = self.coordinates_asarray[:, order]
            if self.coordinates_asarray.shape[1] > 3: f = interp1d(x, y, kind='cubic', fill_value="extrapolate")
            elif self.coordinates_asarray.shape[1] > 2: f = interp1d(x, y, kind='quadratic', fill_value="extrapolate")
            else: f = interp1d(x, y, kind='linear', fill_value="extrapolate")

            arguments = np.arange(min(x)-self.step, max(x)+self.step, self.step/100)
            values = f(arguments)
            sketch = ax.plot(arguments, values)[0]
            self.sketches.append(sketch)
            fig.canvas.draw()

    def plot(self, fig, ax):
        if self.graph is None:
            arguments = np.arange(*self.xlim, step=self.step/100)
            values = np.array([self.function(arg) for arg in arguments])
            self.graph = ax.plot(arguments, values, color='k')[0]
            fig.canvas.draw()

    def add_point(self, fig, ax, argument):
        if self.coordinates_asarray is None or not(np.any(np.isin(self.coordinates_asarray[0], argument))):
            value = self.function(argument)
            if np.isfinite(value):
                self.coordinates.append([argument, value])
                self.coordinates_asarray = np.array(self.coordinates).T
                current_coordinate = np.around(self.coordinates_asarray[:, -1], 3)
                print(current_coordinate[0], '--->', current_coordinate[1])
                self.points.append(ax.scatter(argument, value, color='blue'))
                fig.canvas.draw()
            else:
                print(argument, '--->', value)


    def remove_sketch(self, fig):
        if len(self.sketches) > 0:
            self.sketches[-1].set_visible(False)
            del self.sketches[-1]
            fig.canvas.draw()

    def remove_plot(self, fig):
        if self.graph is not None:
            self.graph.set_visible(False)
            self.graph = None
            fig.canvas.draw()

    def remove_point(self, fig):
        if len(self.points) > 0:
            self.points[-1].set_visible(False)
            del self.points[-1], self.coordinates[-1]
            self.coordinates_asarray = self.coordinates_asarray[:, :-1]
            fig.canvas.draw()

    def shoot_the_moon(self, fig, ax):
        if self.coordinates_asarray is not None and self.coordinates_asarray.shape[1] > 0:
            if self.shoots == 0:
                print('shooting the moon, pew... pew..!')
                self.target = self.coordinates_asarray[:,-1][0]
                self.shooting_direction = 1
                self.shoots += 1
                self.points[-1].set_color('orange')
                fig.canvas.draw()
            else:
                self.add_point(fig, ax, self.target + self.shoots * self.shooting_direction * self.shooting_const)
                self.shooting_direction = - self.shooting_direction
                if self.shooting_direction == 1:
                    self.shoots +=1

class DerivativePlotter(FunctionPlotter):
    def __init__(self, expression, xlim = (-10,10), ylim = (-10,10), step=1, shooting_const=0.5):
        x = sp.symbols('x')
        self.expression = expression
        self.function = sp.lambdify(x, self.expression, "numpy")  # pythonic function coverted from symbolic expression
        self.xlim = xlim  # x limits of figure
        self.ylim = ylim  # y limits of figure
        self.step = step  # scaling of coordinates
        self.user_input = ''  # input that is typed by keyboard until 'enter' hit
        self.coordinates = []  # numerical points
        self.coordinates_asarray = None
        self.sketches = []
        self.graph = None
        self.points = []

    def plot(self, fig, ax):
        if self.graph is None:
            arguments = np.arange(*self.xlim, step=self.step/100)
            values = np.array([self.function(arg) for arg in arguments])
            self.graph = ax.plot(arguments, values, color='k')[0]
            fig.canvas.draw()

    def display(self):
        title = 'FUNKCIJA f(x) =' + str(self.expression)
        fig, ax = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [3, 1]})
        # this draws axis:
        row1, row2 = ax

        plt.sca(row1)
        row1.spines['left'].set_position('center')
        row1.spines['bottom'].set_position('center')
        row1.spines['right'].set_color('none')
        row1.spines['top'].set_color('none')
        row1.xaxis.set_ticks_position('bottom')
        row1.yaxis.set_ticks_position('left')
        plt.xticks(np.arange(self.xlim[0], self.xlim[1], step=self.step))
        plt.yticks(np.arange(self.ylim[0], self.ylim[1], step=self.step))
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)
        plt.grid()

        plt.sca(row2)
        row2.spines['left'].set_position('center')
        row2.spines['bottom'].set_position('center')
        row2.spines['right'].set_color('none')
        row2.spines['top'].set_color('none')
        row2.xaxis.set_ticks_position('bottom')
        row2.yaxis.set_ticks_position('left')
        plt.xticks(np.arange(self.xlim[0], self.xlim[1], step=self.step))
        plt.yticks(np.arange(self.ylim[0], self.ylim[1], step=2 * self.step))
        plt.xlim(*self.xlim)
        plt.ylim(*self.ylim)
        plt.grid()

        fig.canvas.mpl_connect("key_press_event", lambda event: self.refresh_plot(fig, ax, event.key))


        #self.plot(fig, row1)
        #self.plot(fig, row2)
        plt.show()

    def refresh_plot(self, fig, ax, key):
        if key == 'enter':
            inp = self.user_input.replace(',', '.')
            if re.match(r'^-?\d+(?:\.\d+)?$', inp) is not None:
                argument = float(inp)
                self.add_point(fig, ax, argument)
            else:
                print(inp, 'is not a number')
            self.user_input = ''
        elif key == 'up':
            self.sketch(fig, ax)
        elif key == 'down':
            self.remove_sketch(fig)
        elif key == 'ctrl+up':
            self.plot(fig, ax)
        elif key == 'ctrl+down':
            self.remove_plot(fig)
        elif key == 'left':
            self.remove_point(fig)
        elif key == 'right':
            self.shoot_the_moon(fig, ax)
        else:
            self.user_input += key

        if key != 'right':
            self.shoots = 0


functionplotter = FunctionPlotter('1/x', xlim = (-10,10), ylim = (-10,10), step=1)
functionplotter.display()

#derivativeplotter = DerivativePlotter('1/x', xlim = (-10,10), ylim = (-10,10), step=1)
#derivativeplotter.display()
