"""
.. module:: samplers
   :platform: Unix, Windows
   :synopsis: A module used to select initial sample points from a latin hypercube sample of the input domain

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""
import smbo, random


## returns an m-array of k-arrays, describing a k-dimensional latin hypercube of m divisions.
## the arrangement of all the 1s  (or 2s, etc) on a full sudoku board is a special case of a (9,2) latin hypercube.
def latin_hypercube(m, k, bounds=None, rand_sampler=random.random):
    """
    Args:
        m (int): the number of desired sample points
        k (int): the dimension of input space
        bounds (list): the :math:`k` min-max tuples describing the function domain as a :math:`k`-rectangle. Defaults to the unit :math:`k`-cube.
        rand_sampler (function): used to choose actual sample coordinates once the latin hypercube selects a sample's particular hyper(sub)rectangle in the input domain.
            
    Returns:
        list: An :math:`m`-list of :math:`k`-vectors, representing an :math:`m`-point latin hypercube sample of the :math:`k`-dimensional input domain.
    """
    #first, set default boundaries to 0,1 in k dimensions
    if bounds==None:
        bounds=[[0,1]for i in range(k)]
        
    # for each dimension, choose randomly (without replacement) which bin each of the m sample points are from
    # bins[i][j]=n says, "in the ith dimension, the jth sample point lands in bin n"
    bins = [random_range(m) for i in range(k)]    
        
    # for each dimension, store the m left-boundaries of each bin
    bin_width = [float(bounds[dim][1]-bounds[dim][0])/m for dim in range(k)]
    bin_bound = [[bin_width[dim] * bin_no for bin_no in range(m)] for dim in range(k)]
    
    samples = [
        [
            bin_bound[dim][bins[dim][bin_no]] + rand_sampler()*bin_width[dim] 
            for dim in range(k)
        ] for bin_no in range(m)
    ]
      
    return samples

def diag(m, k, bounds=None):
    """
    Args:
        m (int): the number of desired sample points
        k (int): the dimension of input space
        bounds (list): the :math:`k` min-max tuples describing the function domain as a :math:`k`-rectangle. Defaults to the unit :math:`k`-cube.
            
    Returns:
        list: An :math:`m`-list of :math:`k`-vectors, representing evenly spaced points on the diagonal of the bound-rectangle.
    """
    if bounds==None:
        bounds=[[0,1]for i in range(k)]
    
    bin_width = [float(bounds[dim][1]-bounds[dim][0])/m for dim in range(k)]    
    samples = [
        [
            (samp_no+0.5)*bin_width[dim]+bounds[dim][0]
            for dim in range(k)
        ]
        for samp_no in range(m)
    ] 
    return samples
    

    
#LH = latin_hypercube(3,2)
#print(LH)

## returns a random permutation of python's range(n)
def random_range(n):
    out = range(n)
    random.shuffle(out)
    return out