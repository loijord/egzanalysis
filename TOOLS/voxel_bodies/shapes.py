import numpy as np
import matplotlib.pyplot as plt
from itertools import product, starmap

from voxelview import Cubeview

class Shape:
    def get_coordinates(self):
        pass

class Circle(Shape):
    def __init__(self, r, R=None):
        self.r = r
        if R is None: self.R = r + 1
        else: self.R = R

    def get_coordinates(self):
        # return all the integral coordinates of points that preserve distance r from origin; t is for radius of ring
        d = 2*self.R + 1
        X = np.indices((d, d))
        w = (self.R - self.r) / 2
        r = (self.R + self.r) / 2
        distance_array = np.hypot(X[0] - self.R, X[1] - self.R) - r
        bool_array = (distance_array < w) & (distance_array >= -w)
        cells = X.T[bool_array] - self.R
        return [tuple(n) for n in cells] #cells ->np as tuple used in itertools.product

class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_coordinates(self):
        return list(product(range(self.a), range(self.b)))


class Sphere():
    def __init__(self, r):
        self.r = r

    def get_coordinates(self):
        d = 2 * self.r + 1
        X = np.indices((d, d, d))
        bool_array = (X[0]-self.r)**2 + (X[1]-self.r)**2 + (X[2]-self.r)**2 <= self.r**2
        cells = X.T[bool_array] - self.r
        return cells  # cells ->np as tuple used in itertools.product

class Cube():
    def __init__(self, r):
        self.r = r
    def get_coordinates(self):
        d = 2 * self.r + 1
        X = np.indices((d, d, d))
        bool_array = (np.abs(X[0]-self.r)<=self.r) & (np.abs(X[0]-self.r)<=self.r) & (np.abs(X[0]-self.r)<=self.r)
        cells = X.T[bool_array] - self.r
        return cells  # cells ->np as tuple used in itertools.product

class Outshape:
    @staticmethod
    def shape_overz(shape: Shape, zcoords):
        #given shape, outputs negative over zcoords
        temporary_product = list(product(shape.get_coordinates(), zcoords)) #elements are of the form ((a,b),c)
        needed_product = starmap(lambda x, y: x + (y,), temporary_product) #elements are of the form (a,b,c)
        return np.array(list(needed_product)) #tuple as np used in voxplot

def plot(body):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    vvx = Cubeview(body)  # extended form
    vvx.voxplot(ax=ax, facecolors='orange', edgecolors='purple')
    # vvx._fix_view(ax=ax)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

#plot(Outshape.shape_overz(Circle(0, 6), range(1, 9)))
#plot(Outshape.shape_overz(Rectangle(3, 4), range(5)))
#plot(Sphere(8).get_coordinates())
#plot(Cube(4).get_coordinates())

