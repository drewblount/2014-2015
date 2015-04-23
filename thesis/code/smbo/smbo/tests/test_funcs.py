"""
.. module:: tests.test_funcs
   :platform: Unix, Windows
   :synopsis: A module containing test functions for optimization

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""
from math import pi, sin, cos

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
        height=3
        for component in x:
            height+=0.5*(component-minimum_coord)**2 + sin_strength*sin(component*2*pi/period)
        return height
    return func
    
    
def branin(x):
    """
    Args:
        x: two-item list
    Returns:
        Output of the branin test function evaluated at x.
    My reference here is Derek Bingham of Simon Frasier U's page at http://www.sfu.ca/~ssurjano/branin.html 
    """
    a = 1
    b = 5.1/(4*pi**2)
    c = 5/pi
    r = 6
    s = 10
    t = 1/(8*pi)
    return ( a*( x[1] - b*x[0]**2 + c*x[0] - r )**2 + s*(1 - t)*cos( x[0] ) + t )
    
def branin_domain():
    """
    Returns:
        the canonical domain [-5,10] x [0,15] for input to a smb_optimizer initialization
    """
    return [[-5,10],[0,15]]
    
