## The goal of this file is to build a minimum working model of the
## EGO algorithm as put forth in Jones, Schonlau, Welch 1998

from math import exp
from numpy import matrix




## xs is a vector of the input values which have been evaluated already
## by the black box function, and ys is the vector of corresponding outputs.
## qs and ps are regression terms--θs and ps from Jones Eq(1)
## returns the DACE predictor function as defined in Jones etc Eq (7)
def dace_predictor(xs, ys, qs, ps):
    
    # include a length check? |xs| = |ys|, and |qs| = |ps| = dim(elt of xs)
    
    R = corr_matrix(f)
    R_inv = R.I
    # naming vars so they aren't computed more than once
    R_inv_y = R_inv * matrix(ys)
    ones = matrix([1 for i in range(len(xs))])
    ones_T = ones.T
    ones_T_R_inv = ones_T * R_inv
    
    # Regression term -- Jones Eq 5
    mu_hat = ones_T * R_inv_y / (ones_T_R_inv * ones)
    
    # correlation function
    corr_func = ego_corr(qs, ps)
    
    def pred_func(x_new):
        # vector of correlations between x_new and xs
        r = matrix([corr_func(x_new, x_old) for x_old in xs])
        # a transcription of Eq 7
        return mu_hat + r.T*(R_inv_y - R_inv * (ones * mu_hat))
    
    return pred_func
    


## Jones Eq(1)--takes vectors of regressors qs (θs in Jones) and ps,
## and returns a distance function for input vectors
def ego_dist(qs, ps):
    def dist_func(x1, x2):
        diff = [abs(x1 - x2)
        return sum( qs[i] * [ abs( x1[i]-x2[i] ) ** ps[i] ] )
    return dist_func
    
## Jones Eq(2)--takes vectors of regression terms, returns a
## correlation function between input vectors
def ego_corr(qs, ps):
    dist_func = ego_dist(qs,ps)
    def corr_func(x1, x2):
        return exp(-dist_func(x1, x2))
    return corr_func
    
## Returns R, a matrix whose i,jth entry is the correlation between
## x_i and x_j. First makes a 2d list, then transforms it to a numpy matrix
## according to stackexchange: http://stackoverflow.com/questions/7133885/fastest-way-to-grow-a-numpy-numeric-array
## it's fastest to construct with python lists
def corr_matrix(xs, qs, ps):
    corr_func = ego_corr(qs, ps)
    out_arr = []
    for i in range(len(xs)):
        this_row = []
        for j in range(len(xs)):
            ## save time by exploiting diagonal symmetry
            if   i > j: this_row.append(out_arr[j][i])
            elif i < j: this_row.append(corr_func(xs[i],xs[j]))
            else: this_row.append(0)
        out_arr.append(this_row)
    return matrix(out_arr)

## the overall regression term, Jones Eq(5)
def mu_hat(xs, ys, qs, ps):
    R = corr_matrix(f)
    