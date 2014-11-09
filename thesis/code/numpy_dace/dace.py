## This is a copy of dace.py, but using scipy.linalg instead
## of numpy.matrix. Two reasons for the switch: scipy always
## uses BLAS, numpy not always, and scipy.linalg makes classes
## less ambiguous 
## see: http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/linalg.html

## The goal of this file is to build a minimum working model of the
## EGO algorithm as put forth in Jones, Schonlau, Welch 1998

from math import exp, pi
import numpy as np
from scipy import linalg as la
from random import random
import scipy.optimize as op

## xs is a vector of the input values which have been evaluated already
## by the black box function, and ys is the vector of corresponding outputs.
## qs and ps are regression terms--thetas and ps from Jones Eq(1)
## returns the DACE predictor function as defined in Jones etc Eq (7)
## the type of each variable is assumed to
def dace_predictor(xs, ys, ps, qs, verbose=False):
    
    # include a length check? |xs| = |ys|, and |qs| = |ps| = dim(elt of xs)
    
    # makes xs, ys are numpy arrays
    xs, ys = np.array(xs), np.array(ys)
    
    R = corr_matrix(xs, ps, qs)
    # R is now a numpy array
    R_inv = la.inv(R)
    
    # naming vars so they aren't computed more than once -- ys is transposed
    # to change it from a row matrix to a vector
    R_inv_y = R_inv.dot(ys)
    ones = np.array( [[ 1 ]for i in range(len(xs)) ] )
    # ones is a vector (column matrix)
    
    ones_T_R_inv = ones.T.dot(R_inv)
    
    # Regression term -- Jones Eq 5
    mu_hat = ones.T.dot(R_inv_y) / (ones_T_R_inv.dot(ones))
    ## 2d array -> float
    mu_hat = mu_hat[0][0]
    
    if verbose: print('mu_hat = %.4f' % mu_hat)
    
    corr = corr_func(ps, qs)
    
    def pred_func(x_new):
        # vector of correlations between x_new and xs
        r = np.array( [ [corr(x_new, x_old)] for x_old in xs] )
        # a transcription of Eq 7
        temp = R_inv.dot( ones * mu_hat )
        temp2 = R_inv_y - temp
        temp3 = r.T.dot(temp2)
        t3val = temp3[0][0]
        
        return (mu_hat + t3val)   
    
    return pred_func
    

## Jones Eq(1)--takes vectors of regressors qs (thetas in Jones) and ps,
## and returns a dist_funcance function for input vectors
def dist_func(ps, qs):
    def dist(x1, x2):
        diff = [ abs( x1[i] - x2[i] ) for i in range( len(x1) ) ]
        return sum( [ qs[i] * (diff[i] ** ps[i]) for i in range( len(qs) ) ] )
    return dist
    
## Jones Eq(2)--takes vectors of regression terms, returns a
## correlation function between input vectors
def corr_func(ps, qs):
    dist = dist_func(qs,ps)
    def corr(x1, x2):
        return np.exp(-dist(x1, x2))
    return corr
    
## Returns R, a matrix whose i,jth entry is the correlation between
## x_i and x_j. First makes a 2d list, then transforms it to a numpy matrix
## according to stackexchange: http://stackoverflow.com/questions/7133885/fastest-way-to-grow-a-numpy-numeric-array
## it's fastest to construct with python lists
def corr_matrix(xs, ps, qs):
    corr = corr_func(ps, qs)
    out_arr = []
    for i in range(len(xs)):
        this_row = []
        for j in range(len(xs)):
            ## save time by exploiting diagonal symmetry
            if   i > j: this_row.append(out_arr[j][i])
            elif i < j: this_row.append(corr(xs[i],xs[j]))
            else: this_row.append(1)
        out_arr.append(this_row)
    return np.array(out_arr)

## the best prediction of the mean mu, Jones Eq(5), given the output vect ys
## and the correlation matrix R
def mu_hat(ys, R_inv):
    ones = np.array( [[ 1 ]for i in range(len(ys)) ] )
    ones_T_R_inv = ones.T.dot(R_inv)
    return ones_T_R_inv.dot(ys) / ones_T_R_inv.dot(ones)
    
    
## the best prediction of the stdev, jones Eq(6). Assumes ys is already a
## column matrix in numpy. R is the correlation matrix.
def stdev_hat(ys, R_inv, mu):
    n = len(ys)
    ones = np.array( [[ 1 ]for i in range(len(ys)) ] )
    return ( (ys - ones*mu).T.dot( R_inv.dot(ys - ones*mu) ) ) / n
    

## The concentrated likelihood function, Eqs 4-6 from Jones et al.
## takes args xs, ys (evaluated inputs and outputs)
## ands ps, qs (regression variables) and returns the
## likelihood of observing the xs, ys given the
## ps, qs. This is the function we wish to optimize when choosing ps, qs
## to maximize likelihood.
def conc_likelihood(xs, ys, ps, qs):
    R = corr_matrix(xs, ps, qs)
    R_inv = la.inv(R)
    mu = mu_hat(ys, R_inv)
    stdev = stdev_hat(ys, R_inv, mu)
    n = len(ys)
    ones = np.array( [[ 1 ]for i in range(len(xs)) ] )
        
    # linear term
    lin_term = 1 / ( (2 * pi * stdev)**(n/2.0) * la.det(R) ** (0.5) )
    
    # combining the right half of 4 with 6 gives this simplified expression
    exp_term = exp(n/2.0)
    
    return lin_term*exp_term
  
## for a given xs, ys, finds ps and qs that optimize the above function
#def max_likelihood_params(xs, ys):
    
    
    
    
    
    
    
    
    
