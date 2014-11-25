## an object-oriented EGO algorithm machine


from math import exp, pi
import numpy as np
from scipy import linalg as la
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from operator import add, sub

import logging
log = logging.getLogger('ego.log')

# 'lazyprop's are lazily-evaluated properties that save the results of
# certain matrix operations. also imports a lazyprop-deleter
from lazyprop import lazyprop, reset_lps

class egoist:
    
    ## The solver is initialized by passing it the starting
    ## inputs and outputs.
    ## X's type: 2d array of input vectors. Y is a 1d array of outputs
    def __init__(self, X0=[[]], Y0=[], logger=None):
        
        self.log = logger or logging.getLogger(__name__)
        logging.basicConfig(filename='ego.log', level=logging.INFO)
        
        self.log.info('new ego class initialized')
        
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
        
        #logs the creation of the object
        
    # adds an evaluated point:
    def addpoint(self, x_new, y_new, verbose=False):
        self.X = np.append(self.X, [x_new])
        self.Y = np.append(self.Y, y_new)
        if verbose:
            print ('X = ' + str(E.X))
            print ('Y = ' + str(E.Y))
        # have to reset lazy properties
        reset_lps(self)
        
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
        # can't change a dict while iterating through it, hence intermediate list
        lazy_keys = [k for k in self.__dict__ if (k[0:6] == '_lazy_') ]
        for key in lazy_keys:
            delattr(self, key)
        
    
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
    def conc_likelihood(self, new_P=None, new_Q=None):
        if new_P!=None: self.P=new_P
        if new_Q!=None: self.Q=new_Q
        if new_P!=None or new_Q!=None: reset_lps(self)
        
        inv_linear_term =(2.0 * pi * self.stdev_hat)**(self.n/2.0) * self.R_det ** (0.5)
        return exp(self.n/2.0)/inv_linear_term
    
    
    # Sets P and Q so as to maximize the above likelihood function
    # param_range is a series of parenthesized min/max tuples:
    # ((P[0]min,P[0]max),...(Q[n-1]min,Q[n-1]max))
    # note that None is a valid upper/lower bound
    
    # WARNING: MIGHT ONLY WORK FOR 1D
    def max_likelihood(self, param_range=((1.0,2.0),(0.01,None)), verbose=False):
        
        # the function to be minimized. note that P is the first half of z, Q the second
        def neg_conc(z): return (-1 * self.conc_likelihood(z[:self.k],z[self.k:]))
        z0 = self.P + self.Q
        
        res = minimize(neg_conc, z0, bounds=param_range)
        return res
        
    
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
        
    # assumes a 1d x-space
    def pred_over(x_range):
        return [ self.predict( [x]) for x in pred_range ]
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
        plt.show()
        
    # Performs the above, with sliders to manipulate P and Q
    def plot1d_sliders(self, x_min=0.0, x_max=5.0, x_delta=0.01, y_min=0.0, y_max=1.0, P_min=1.0,P_max=2.0,Q_min=0.1,Q_max=10.0):
        
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        plt.xlabel('x')
        plt.ylabel('predicted y(x)')
        plt.title('Toy Problem')
        
        pred_range = np.arange(x_min, x_max, x_delta)
        preds  = [ self.predict( [x]) for x in pred_range ]
        errors = [ self.pred_err([x]) for x in pred_range ]
        # elem-wise sum/difference of above two arrays
        pl_errors = map(add, preds, errors)
        mi_errors = map(sub, preds, errors)
        
        # plot the predictor and +/- errors
        pred_line,  = plt.plot(pred_range, preds)
        p_err_line, = plt.plot(pred_range, pl_errors, color="green")
        m_err_line, = plt.plot(pred_range, mi_errors, color="green")
        plt.axis([x_min, x_max, y_min, y_max])
                
        # sets slider locations
        axP = plt.axes([0.25, 0.05, 0.65, 0.03])
        axQ = plt.axes([0.25, 0.1, 0.65, 0.03])
        
        slidP = Slider(axP, 'P', P_min, P_max, valinit=self.P[0])
        slidQ = Slider(axQ, 'Q', Q_min, Q_max, valinit=self.Q[0])
        
        def update(val):
            self.P = [slidP.val]
            self.Q = [slidQ.val]
            # all the lazyprops are inaccurate after P or Q change
            reset_lps(self)
            
            # re-draw each line (lazyprops will now be re-evaluated)
            preds  = [ self.predict( [x]) for x in pred_range ]
            pred_line.set_ydata(preds)
            errors = [ self.pred_err([x]) for x in pred_range ]
            # elem-wise sum/difference of above two arrays
            pl_errors = map(add, preds, errors)
            p_err_line.set_ydata(pl_errors)
            mi_errors = map(sub, preds, errors)
            m_err_line.set_ydata(mi_errors)
            
            fig.canvas.draw_idle()
                        
        slidP.on_changed(update)
        slidQ.on_changed(update)
        
        plt.show()
        
        
        
        
