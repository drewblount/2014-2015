"""
.. module:: dace
   :platform: Unix, Windows
   :synopsis: A function/class hybrid to describe individual instances of DACE predictors

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""


class dace_model:
    
    def __init__(self, Xs, Ys):
        """
        Args:
            Xs (list): an :math:`n`-list containing the `k`-dimensional input coordinates of the :math:`n` sample points
            Ys (list): a list (index-aligned with Xs) containing the evaluated objective function output at each sample point
        Returns:
            A tuple of functions, (pred_y, pred_err). pred_y is the DACE predictor function, and pred_err is the predicted standard deviation (or is it variance?) of that predictor; both are :math:`k\rightarrow 1` dimensional.
        """
        
    # distance in input-space (x1 is an array; an input vector)
    def dist(self, x1, x2):
        """
        Args:
            x1 (list): a coordinate in input space
            x2 (list): a coordinate in input space
        Returns:
            the DACE-parameterized distance between the two points.
        The distance function for points in input space
        """
        return np.sum( [ 
            self.Q[i] * 
            abs( x1[i] - x2[i] ) ** self.P[i]
            for i in range( self.k ) 
        ] )
        
    def corr(self, x1, x2):
        """
        Args:
            x1 (list): a coordinate in input space
            x2 (list): a coordinate in input space
        Returns:
            the DACE-parameterized correlation between the predictor error at two points.
        As the DACE predictor is built upon the notion of correlated predictor error, this
        correlation function is the conceptual center of the DACE predictor.
        """
        return exp(-self.dist(x1,x2))
    
    