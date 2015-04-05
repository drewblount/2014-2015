"""
.. module:: models
   :platform: Unix, Windows
   :synopsis: implements the DACE modeller given a set of sample points

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""

from smbo import (
    la,
    minimize, 
    norm, 
    np,
    plt, 
)

from smbo.lazyprop import lazyprop, reset_lps

from matplotlib.widgets import Slider
from operator import add, sub
from math import exp, pi, sqrt

import logging
log = logging.getLogger('ego.log')


class dace:
    """
    A little hefty to be simply a function, this class (which behaves as a function because of its __apply__ method)
    fits a DACE model to provided sample points
    """
    
    # nearzero values for Q parameters lead to singular matrices, hence
    eps = 1e-5
    
    def __init__(self,X,Y):
        """
        Args:
            X (list): a list of input vectors
            Y (list): a list of observed objective values
        Returns:
            tuple:
                (pred_y,pred_err): two functions, each k-to-1, where k is the dimension of the input space, representing the dace predictor surface and predicted error at each point in input space
        """ 
        self.X=X
        self.Y=Y
        # number of dimensions
        self.k = len(X[0])
        # number of evaluated points
        self.n = len(X)
        
        #the stuff under here
        
        # now sets P and Q to maximize likelihood (first, dummy variables)
        self.P = self.Q = [1.5 for i in range(self.k)]
        self.max_likelihood()
    
    # distance in input-space (x1 is an array; an input vector)
    def dist(self, x1, x2):
        """
        Args:
            x1 (list): a coordinate in the domain
            x2 (list): a coordinate in the domain
        Returns:
            float:
                the parameterized distance between x1 and x2
        """
        return np.sum( [ 
            self.Q[i] * 
            abs( x1[i] - x2[i] ) ** self.P[i]
            for i in range( self.k ) 
        ] )

    # correlation between the function values at two points in input-space
    def corr(self, x1, x2):
        """
        Args:
            x1 (list): a coordinate in the domain
            x2 (list): a coordinate in the domain
        Returns:
            float:
                the correlation between estimation errors at x1 and x2
        """
        return exp(-self.dist(x1,x2))
    
    
    # following are a bunch of lazyprops, which are lazily evaluated properties that are
    # saved so that the same linear algebra is never performed twice.
    
    # When the ego object at hand changes, e.g. by manual manipulation of the parameters
    # P and Q, these saved properties must be refreshed.
    def reset(self):
        """
        Resets all lazyprops
        """
        # can't change a dict while iterating through it, hence intermediate list
        lazy_keys = [k for k in self.__dict__ if (k[0:6] == '_lazy_') ]
        for key in lazy_keys:
            delattr(self, key)
        
    @lazyprop
    def R(self):
        """
        R is the n*n matrix whose i,jth entry is the correlation between the i,jth {evaluated inputs
        """
        return np.array([[self.corr(self.X[i],self.X[j]) for i in range(self.n)] for j in range(self.n)])
        
    # like a column of R
    def corr_vector(self, x_new):
        """
        Args:
            x_new: a :math:`k`-vector from the domain
        Returns:
            list:
                a vector whose :math:`i^{th}` element is the parameterized correlation between x_new and the :math`i^{th}` sample point
        """
        return np.array([self.corr(self.X[i],x_new) for i in range(self.n)])
        
    @lazyprop
    def R_inv(self):
        return la.inv(self.R)
        
    @lazyprop
    def R_det(self,eps=1e-8):
        #hmmm, this seems like terrible practice, but I can't have R_det == 0 because of a div by zero in the likelihood equation.
        return max(eps,la.det(self.R))
        
    @lazyprop
    def ones(self):
        return np.ones(self.n) 
    
    # this one is used a bunch
    @lazyprop
    def ones_R_inv(self):
        return(self.ones.T.dot(self.R_inv))
    
    @lazyprop
    def ones_R_inv_Y(self):
        return self.ones_R_inv.dot(self.Y)
        
    @lazyprop
    def ones_R_inv_ones(self):
        return self.ones_R_inv.dot(self.ones)
    
    # best predictor of the mean mu, Jones eq 5
    @lazyprop
    def mu_hat(self):
        return self.ones_R_inv_Y / self.ones_R_inv_ones
        
    @lazyprop
    def Y_min_mu(self):
        return self.Y - (self.ones*self.mu_hat)
    
    @lazyprop
    def R_inv_Y_min_mu(self):
        return self.R_inv.dot(self.Y_min_mu)    
    
    # Jones eq(6)
    @lazyprop
    def var_hat(self, eps=1e-8):
        #hmmm, this seems like terrible practice, but I can't have var_hat == 0 because of a div by zero in the likelihood equation.
        return max(eps, self.Y_min_mu.T.dot(self.R_inv_Y_min_mu) / self.n)
                
    # Jones eq 4 w/ 5, 6 inserted for mu, stdev
    def conc_likelihood(self, new_P=None, new_Q=None):
        """
        Args:
            new_P (list): an :math:`n`-vector resetting the :math:`p` parameter of the DACE model
            new_Q (list): an :math:`n`-vector resetting the :math:`q` or :math:`\theta` parameter of the DACE model
        Returns:
            float:
                the likelihood of the current DACE params P and Q, given the data X and Y
        """
        if new_P!=None: self.P=new_P
        if new_Q!=None: self.Q=new_Q
        if new_P!=None or new_Q!=None: reset_lps(self)
        
        inv_linear_term = pow(2.0 * pi * self.var_hat, self.n/2.0) * self.R_det ** (0.5)
        return exp(self.n/2.0)/inv_linear_term
    
        
    def max_likelihood(self, bounds=None, verbose=False):
        """
        Args:
            bounds(list): the :math:`P\times Q` domain over which likelihood is being maximized, defaults to :math:`(1,2)\times(0,\infty)`
        Returns:
            optimization_result:
                res: an object describing the :math:`P` and :math`Q` values that optimize likelihood
        The evaluation of this function also resets self.P and self.Q to the values indicated by res, i.e.
        it sets P and Q to maximize the likelihood of the DACE model, thereby fitting the model to the data.
        """
        
        # default parameter range is each p from 1 to 2, each q > 0
        if not bounds:
            p_bounds = [(1,2) for _ in range(self.k)]
            q_bounds = [(self.eps,None) for _ in range(self.k)]
            bounds = tuple(p_bounds+q_bounds)
        
        # allows for the case when P and Q are not yet set
        if not self.P: self.P = [1.5 for i in range(self.n)]
        if not self.Q: self.Q = [1.5 for i in range(self.n)]
        
        # the function to be minimized. note that P is the first half of z, Q the second
        def neg_conc(z): return (-1 * self.conc_likelihood(z[:self.k],z[self.k:]))
        
        # the minimizer needs an initial coord
        z0 = self.P + self.Q
        
        res = minimize(neg_conc, z0, method='L-BFGS-B',bounds=bounds)
        # now save the output to P and Q, and reset lazyprops
        self.P = res.x[:self.k]
        self.Q = res.x[self.k:]
        reset_lps(self)
        print('P and Q have been set to maximize the likelihood equation.')
        
        return res
       
    
    # the 
    def predict(self, x_new):
        """
        Args:
            x_new (list): a :math:`k`-vector from the domain
        Returns:
            float:
                the predicted function value at x_new
        This is computed using the so-called best linear unbiased predictor,  Jones Eq. 7
        """
        r = self.corr_vector(x_new)
        return self.mu_hat + r.dot(self.R_inv_Y_min_mu)
        
    # the error of the predictor, Jones Eq. 9
    def pred_err(self, x_new):
        """
        Args:
            x_new (list): a :math:`k`-vector from the domain
        Returns:
            float:
                the predicted function value at x_new
        This is computed using the so-called best linear unbiased predictor,  Jones Eq. 7
        """
        r = self.corr_vector(x_new)
        R_inv_r = self.R_inv.dot(r)
        # was getting some weird tiny (magnitude) negative number float errors
        out = self.var_hat * (1 - r.dot(R_inv_r) + ( ( 1 - self.ones.dot( R_inv_r) )**2 / (self.ones_R_inv_ones)) )
        return (max(out, 0.0))
        
      
    # what follows below are the components required to maximize the expected improvement
    # function (Jones Eq. 15)  
    @lazyprop
    def stdev(self):
        return sqrt(self.var_hat)
        
    # current minimum function value (assume optimization problem is minimization)
    @lazyprop
    def f_min(self):
        """
        Args:
        Returns:
            float:
                the data set's minimum evaluated function value
        """
        return np.min(self.Y)
    
    # expected improvement function (Jones Eq. 15) (eps is included for floating point rounding errs)
    def exp_improvement(self, x_new):
        """
        Args:
            x_new (list): a :math:`k`-vector from the domain
        Returns:
            float:
                the predicted benefit in f_min of sampling the objective function at x_new
        """
        # should predict(x) be stored lazily? don't want to double-call the predictor function
        # (maybe unnecessary; is the predictor function ever explicitly used in the iterative process?)
        y = self.predict(x_new)
        # improvement over current minimum
        improvement = self.f_min - y
        
        # s
        err = self.pred_err(x_new)
        if (err < 0):
            print('Error: pred_err(x) < 0 for x = ' + str(x_new) + '; pred_err(x) = ' + str(err))
        
        st_dev = sqrt(self.pred_err(x_new))
        
        # catches when x_new is in X (already evaluated points, 100% certain of prediction)
        if (st_dev == 0.0): return(0.0)
        
        normed_improvement = improvement/st_dev
        return(improvement * norm.cdf(normed_improvement) + st_dev * norm.pdf(normed_improvement))
        
def dace_function(X,Y):
    """
    Args:
        X (list): a list of input vectors
        Y (list): a list of observed objective values
    Returns:
        tuple:
            (pred_y,pred_err): two functions, each k-to-1, where k is the dimension of the input space, representing the dace predictor surface and predicted error at each point in input space
    This instantiates a dace class member behind the scenes and returns its predictor function, and the predicted error function of its predictor function.
    """
    dacer = dace(X,Y)
    return (dacer.predict, dacer.pred_err)
    