## an object-oriented EGO algorithm machine


from math import exp, pi
import numpy as np
from scipy import linalg as la

class egoist:
    
    ## The solver is initialized by passing it the starting
    ## inputs and outputs.
    ## X's type: 2d array of input vectors. Y is a 1d array of outputs
    def __init__(self, X0=[[]], Y0=[]):
        
    