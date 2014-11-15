## This is a copy of dace.py, but using scipy.linalg instead
## of numpy.matrix. Two reasons for the switch: scipy alwaY
## uses BLAS, numpy not alwaY, and scipy.linalg makes classes
## less ambiguous 
## see: http://docs.scipy.org/doc/scipy-0.14.0/reference/tutorial/linalg.html

## The goal of this file is to build a minimum working model of the
## EGO algorithm as put forth in Jones, Schonlau, Welch 1998

from math import exp, pi
import numpy as np
from scipy import linalg as la
from random import random
import scipy.optimize as op

## X is an array of the input vectors which have been evaluated already
## by the black box function, and Y is the array of corresponding outputs.
## Q and P are regression terms--thetas and P from Jones Eq(1)
## returns the DACE predictor function as defined in Jones etc Eq (7)
## the type of each variable is assumed to
def dace_predictor(X, Y, P, Q, verbose=False):
    
    # include a length check? |X| = |Y|, and |Q| = |P| = dim(elt of X)
    
    # makes X, Y are numpy arraY
    X, Y = np.array(X), np.array(Y)
    
    R = corr_matrix(X, P, Q)
    # R is now a numpy array
    R_inv = la.inv(R)
    
    # naming vars so they aren't computed more than once -- Y is transposed
    # to change it from a row matrix to a vector
    R_inv_y = R_inv.dot(Y)
    ones = np.array( [[ 1 ]for i in range(len(X)) ] )
    # ones is a vector (column matrix)
    
    ones_T_R_inv = ones.T.dot(R_inv)
    
    # Regression term -- Jones Eq 5
    mu_hat = ones.T.dot(R_inv_y) / (ones_T_R_inv.dot(ones))
    ## 2d array -> float
    mu_hat = mu_hat[0][0]
    
    if verbose: print('mu_hat = %.4f' % mu_hat)
    
    corr = corr_func(P, Q)
    
    def pred_func(x_new):
        # vector of correlations between x_new and X
        r = np.array( [ [corr(x_new, x_old)] for x_old in X] )
        # a transcription of Eq 7
        temp = R_inv.dot( ones * mu_hat )
        temp2 = R_inv_y - temp
        temp3 = r.T.dot(temp2)
        t3val = temp3[0][0]
        
        return (mu_hat + t3val)   
    
    return pred_func
    
# returns the predictor's error function
def pred_error(X,Y,P,Q,verbose=False):
    R = corr_matrix(X, P, Q)
    R_inv = la.inv(R)
    m_hat = mu_hat(Y, R_inv)
    sig_hat = stdev_hat(Y, R_inv, m_hat)
    ones = np.array( [[ 1 ]for i in range(len(X)) ] )
    corr = corr_func(P, Q)
    def pred_err_func(x_new):
        r = np.array( [ [corr(x_new, x_old)] for x_old in X] )
        fraction = (ones.T.dot(R_inv).dot(r))**2 / ones.T.dot(R_inv).dot(ones)
        out = sig_hat*(1 - r.T.dot(R_inv).dot(r) + fraction)
        if verbose: print('output type is ' + str(type(out)))
        return out
    return pred_err_func

## Jones Eq(1)--takes vectors of regressors Q (thetas in Jones) and P,
## and returns a dist_funcance function for input vectors
def dist_func(P, Q):
    def dist(x1, x2):
        diff = [ abs( x1[i] - x2[i] ) for i in range( len(x1) ) ]
        return sum( [ Q[i] * (diff[i] ** P[i]) for i in range( len(Q) ) ] )
    return dist
    
## Jones Eq(2)--takes vectors of regression terms, returns a
## correlation function between input vectors
def corr_func(P, Q):
    dist = dist_func(Q,P)
    def corr(x1, x2):
        return np.exp(-dist(x1, x2))
    return corr
    
## Returns R, a matrix whose i,jth entry is the correlation between
## x_i and x_j. First makes a 2d list, then transforms it to a numpy matrix
## according to stackexchange: http://stackoverflow.com/questions/7133885/fastest-way-to-grow-a-numpy-numeric-array
## it's fastest to construct with python lists
def corr_matrix(X, P, Q):
    corr = corr_func(P, Q)
    out_arr = []
    for i in range(len(X)):
        this_row = []
        for j in range(len(X)):
            ## save time by exploiting diagonal symmetry
            if   i > j: this_row.append(out_arr[j][i])
            elif i < j: this_row.append(corr(X[i],X[j]))
            else: this_row.append(1)
        out_arr.append(this_row)
    return np.array(out_arr)

## the best prediction of the mean mu, Jones Eq(5), given the output vect Y
## and the correlation matrix R
def mu_hat(Y, R_inv):
    ones = np.array( [[ 1 ]for i in range(len(Y)) ] )
    ones_T_R_inv = ones.T.dot(R_inv)
    return ones_T_R_inv.dot(Y) / ones_T_R_inv.dot(ones)
    
    
## the best prediction of the stdev, jones Eq(6). Assumes Y is already a
## column matrix in numpy. R is the correlation matrix.
def stdev_hat(Y, R_inv, mu):
    n = len(Y)
    ones = np.array( [[ 1 ]for i in range(len(Y)) ] )
    return ( (Y - ones*mu).T.dot( R_inv.dot(Y - ones*mu) ) ) / n
    



## The concentrated likelihood function, EQ 4-6 from Jones et al.
## takes args X, Y (evaluated inputs and outputs)
## ands P, Q (regression variables) and returns the
## likelihood of observing the X, Y given the
## P, Q. This is the function we wish to optimize when choosing P, Q
## to maximize likelihood.
def conc_likelihood(X, Y, P, Q, verbose=False):
    R = corr_matrix(X, P, Q)
    R_inv = la.inv(R)
    mu = mu_hat(Y, R_inv)
    stdev = stdev_hat(Y, R_inv, mu)
    n = len(Y)
    ones = np.array( [[ 1 ]for i in range(len(X)) ] )
        
    # I've been getting errors when the determinate of R is negative, so:
    # [what do Jones et al mean by |R| in eq. 4?]
    R_det = la.det(R)
    
    if R_det < 0:
        R_det *= -1
        if verbose:
            print("det(R) < 0 for parameters (value will be negated):")
            print("X = " + str(X))
            print("Y = " + str(Y))
            print("P = " + str(P))
            print("Q = " + str(Q))
            print()
        
    # linear term
    lin_term = 1 / ( (2 * pi * stdev)**(n/2.0) * R_det ** (0.5) )
    
    # combining the right half of 4 with 6 gives this simplified expression
    exp_term = exp(n/2.0)
    
    return float(lin_term*exp_term)
  
## for a given X, Y, finds P and Q that optimize the above function
#def max_likelihood_params(X, Y):
    
    
    
    
    
    
    
    
    
