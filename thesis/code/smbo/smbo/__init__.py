import numpy as np
from matplotlib import pyplot as plt
from scipy import linalg as la
from scipy.optimize import minimize
from scipy.optimize import basinhopping
from scipy.stats import norm


import tests
import smb_optimizer
import samplers
import lazyprop
import models