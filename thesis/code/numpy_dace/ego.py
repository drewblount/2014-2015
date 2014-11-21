## an object-oriented EGO algorithm machine


from math import exp, pi
import numpy as np
from scipy import linalg as la
import matplotlib.pyplot as plt
from operator import add, sub

# 'lazyprop's are lazily-evaluated properties that save the results of
# certain matrix operations. also imports a lazyprop-deleter
from lazyprop import *

class egoist:
    
    ## The solver is initialized by passing it the starting
    ## inputs and outputs.
    ## X's type: 2d array of input vectors. Y is a 1d array of outputs
    def __init__(self, X0=[[]], Y0=[]):
        
        self.X = np.array(X0)
        self.Y = np.array(Y0)
        # number of dimensions
        self.k = len(self.X[0])
        # number of evaluated points
        self.n = len(self.X)
        
        
        ## temporary: regression parameters are initialized at default values
        ## (should eventually be chosen by max. likelihood)
        self.P = [1.3 for _ in range(self.k)]
        self.Q = [3.8 for _ in range(self.k)]
        
    # distance in input-space (x1 is an array; an input vector)
    def dist(self, x1, x2):
        return np.sum( [ 
            self.Q[i] * 
            abs( x1[i] - x2[i] ) ** self.P[i]
            for i in range( self.k ) 
        ] )

    # correlation between the function values at two points in input-space
    def corr(self, x1, x2):
        return exp(-self.dist(x1,x2))
    
    
    # following are a bunch of lazyprops, which are lazily evaluated properties that are
    # saved so that the same linear algebra is never performed twice.
    
    # When the ego object at hand changes, e.g. by manual manipulation of the parameters
    # P and Q, these saved properties must be refreshed.
    def reset(self):        
        # want: delete any of self's attributes with names starting with _lazy_
        for key in self.__dict__:
            if key[0:6] == '_lazy_':
                del self['key']
        
        
    
    # R is the n*n matrix whose i,jth entry is the correlation between the i,jth {evaluated inputs
    @lazyprop
    def R(self):
        #return np.fromiter( ( self.corr(self.X[i],self.X[j]) for i in range(self.n) for j in range(self.n) ), dtype=int).reshape(self.n,self.n)
        # would like to do the below without the intermediate non-numpy array:
        #       ((how do you do 2d numpy array list comprehension? above is a failed attempt))
        return np.array([[self.corr(self.X[i],self.X[j]) for i in range(self.n)] for j in range(self.n)])
        
    # like a column of R
    def corr_vector(self, x_new):
        return np.array([self.corr(self.X[i],x_new) for i in range(self.n)])
        
    @lazyprop
    def R_inv(self):
        return la.inv(self.R)
        
    @lazyprop
    def R_det(self):
        return la.det(self.R)
        
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
    def stdev_hat(self):
        return ( self.Y_min_mu.T.dot(self.R_inv_Y_min_mu) ) / self.n
        
    # Jones eq 4 w/ 5, 6 inserted for mu, stdev
    def conc_likelihood(self):
        inv_linear_term =(2 * pi * self.stdev)**(self.n/2.0) * self.R_det ** (0.5)
    
    
    # the so-called best linear unbiased predictor,  Jones Eq. 7
    def predict(self, x_new):
        # correlation between x_new and each evaluated x:
        #r = np.fromfunction(lambda i: self.corr(x_new, self.X[i]), self.n, dtype=int)
        # wanted: an rewrite of the below to not use an intermediate non-numpy list
        #           ((how do you make numpy arrays w list comprehension??))
        r = self.corr_vector(x_new)
        return self.mu_hat + r.dot(self.R_inv_Y_min_mu)
        
    # the error of the predictor
    def pred_err(self, x_new):
        r = self.corr_vector(x_new)
        R_inv_r = self.R_inv.dot(r)
        return (self.stdev_hat * (1 - r.dot(R_inv_r) + ( 1 - self.ones.dot( R_inv_r) )**2 / (self.ones_R_inv_ones) ))
        
    # plots the predictor and its error:
    def plot1d(self, x_min=0.0, x_max=5.0, x_delta=0.01, y_min=0.0, y_max=1.0):
        pred_range = np.arange(x_min, x_max, x_delta)
        preds  = [ self.predict( [x]) for x in pred_range ]
        errors = [ self.pred_err([x]) for x in pred_range ]
        # elem-wise sum/difference of above two arrays
        pl_errors = map(add, preds, errors)
        mi_errors = map(sub, preds, errors)
        
        # plot the predictor and +/- errors
        plt.plot(pred_range, preds)
        plt.plot(pred_range, pl_errors, color="green")
        plt.plot(pred_range, mi_errors, color="green")
        
        plt.axis([x_min,x_max,y_min,y_max])
        plt.xlabel('x')
        plt.ylabel('predicted y(x)')
        plt.title('Toy Problem')
        plt.show()
        
    # Performs the above, with sliders to manipulate P and Q
    
        
