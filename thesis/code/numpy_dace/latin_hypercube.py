## This file implements latin hypercube sampling as defined on the wikipedia page, for use selecting initial sample points in k dimensions

## returns an m-array of k-arrays, describing a k-dimensional latin hypercube of m divisions.
## the arrangement of all the 1s  (or 2s, etc) on a full sudoku board is a special case of a (9,2) latin hypercube.
def latin_hypercube(m, k):
    # simple: for each dimension, first choose randomly (without replacement) which bin the sample point is from