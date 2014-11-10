from dace import *
from matplotlib import pyplot as plt
import numpy as np

# for a 1-D function y(x), P,Q-parameter space is 2d, so a heatmap of
# the likelihood of a set of input/output values over P in one dimension
# and Q in the other should make it visually obvious where the maxima are
# resolution is the distance between points where the likelihood function
# is evaluated to create the plot.

# This function maps the concentrated likelihood of X and Y over P*Q parameter space
# and plots it if plot=True, otherwise it returns the likelihood map
def likelihood_map(X, Y, Pmin=1, Pmax=2, P_res=0.1, Qmin=0, Qmax=10, Q_res=1, plot=True):
    
    # each p and q is a 1d vector, so Ps and Qs are np arrays of singleton arrays of P, Q vals
    Ps = np.arange(Pmin, Pmax, P_res)[np.newaxis].T
    Qs = np.arange(Qmin, Qmax, Q_res)[np.newaxis].T
    # np.arange creates an array of intermediate values, [np.newaxis] nests that array in
    # another, then .T transposes it into a column vector.
    
    likelihood_data = [ [conc_likelihood(X,Y,P,Q) for P in Ps] for Q in Qs]
    
    # getting some NaNs; here's a temporary patch
    likelihood_data = np.array([[-1 if np.isnan(datum) else datum for datum in row] for row in likelihood_data])
    
    
    if plot:
        plt.pcolor(likelihood_data)
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(likelihood_data)
        ax.set_xticklabels([p[0] for p in Ps])
        ax.set_yticklabels([q[0] for q in Qs])
        plt.show()
        
    return likelihood_data