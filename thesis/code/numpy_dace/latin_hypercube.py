## This file implements latin hypercube sampling as defined on the wikipedia page, for use selecting initial sample points in k dimensions

import numpy as np
import random

## returns an m-array of k-arrays, describing a k-dimensional latin hypercube of m divisions.
## the arrangement of all the 1s  (or 2s, etc) on a full sudoku board is a special case of a (9,2) latin hypercube.
def latin_hypercube(m, k, bounds=None, rand_sampler=random.random):
    
    #first, set default boundaries to 0,1 in k dimensions
    if bounds==None:
        bounds=[[0,1]for i in range(k)]
        
    # for each dimension, choose randomly (without replacement) which bin each of the m sample points are from
    # bins[i][j]=n says, "in the ith dimension, the jth sample point lands in bin n"
    bins = [random.shuffle(range(m)) for i in range(k)]    
        
    # for each dimension, store the m left-boundaries of
    bin_width = [bounds[dim][1]-bounds[dim][0] for dim in range(k)]
    bin_bound = [[bin_width[dim] * bin_no for bin_no in range(m)] for dim in range(k)]
    
    samples = [
        [
            bin_bound[dim][bins[dim][bin_no]] + rand_sampler()*bin_width[dim] 
            for dim in range(k)
        ] for bin_no in range(m)
    ]
    
        
    return samples
    
#LH = latin_hypercube(3,2)
#print(LH)