from math import pi, cos

# The goal of this script is to reproduce the implementation of EGO on the
# so-called branin test function, from Jones et al's original paper.


# reference: http://www.sfu.ca/~ssurjano/branin.html
# parameters of the function set to suggested values from above
def branin(x1, x2):
    a, b, c = 1, 5.1/(4*pi**2), 5/pi
    r, s, t = 6, 10,            1/(8*pi)
    return( (a*x2 - b*x1**2 + c*x1 - r)**2 + s*(1-t)*cos(x1) + s )
    
# from the above citation: the function is usally evaluated on the square,
# [-5, 10]*[0, 15]

# it has three (tied) global minima where f(x1, x2) = 0.397887:
# (-pi, 12.275), (pi, 2.275), (9.42478, 2.475)