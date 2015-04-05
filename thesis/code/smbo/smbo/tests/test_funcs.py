"""
.. module:: tests.test_funcs
   :platform: Unix, Windows
   :synopsis: A module containing test functions for optimization

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""
from math import pi, sin

def sinusoparaboloid(ndims=3,period=0.25,minimum_coord=0.5,sin_strength=1.0):
    """
    Args:
        ndims (int): the dimensionality of input space
        period (float): the desired period of the sinusoidal component of the output
        minimum_coord (float): the desired location (roughly) of the global minimum
        sin_strength (float): lets you weight the input of the sin component
    Returns:
        func(list)->float: a function that is a combination of an ndim-dimensional sine wave, which creates a bunch of local minima, and an n-dimensional parabola, creating a global minimum near (minimum_coord,minimum_coord,...,minimum_coord)
    """
    def func(x):
        height=1
        for component in x:
            height+=(component-minimum_coord)**2 + sin_strength*sin(component*2*pi/period)
        return height
    return func
