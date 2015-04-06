"""
.. module:: smb_optimizer
   :platform: Unix, Windows
   :synopsis: A class to describe individual instances of sequential model-based optimizers

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""
from smbo import (
    minimize,
    norm,
    np,
    plt,
    samplers
)
from smbo.lazyprop import lazyprop, reset_lps

from operator import add, sub
from math import sqrt
#current working directory
from os import getcwd

class smb_optimizer:
    """ An object that, given an input domain, objective function, and modelling strategy, seeks to efficiently find
        the global optimum of the objective by the generation of sequential models.
    """
    
    def __init__(self, domain, objective_func, modeller, init_sampler=None, plot_res=0.01, brute_optimize_EI=False):
        """
        Args:
            domain (list): a list whose :math:`i^{th}` element is the :math:`(lower\ bound,\ upper\ bound)` pair 
                describing the domain of interest in the :math:`i^{th}` input dimension. The length 
                of this list defines the dimension of input space, denoted :math:`k`. This smb_optimizer
                then optimizes the :math:`k`-rectangle defined by the domain arg.
            objective_func (function): a function (or any object with a suitable __apply__ method)
                that maps :math:`k`-vectors to floats. The goal of an smb_optimizer is to minimize this
                function over the domain defined above.
            modeller (function): a function (or any object with a suitable __apply__ method) that maps a
                tuple :math:`(X,Y)`, where :math`X` is a list of sample points (each a :math:`k`-vector from the domain),
                and :math:`Y` their evaluated objective values; to a tuple of functions
                :math:`(\hat{y},\ \hat{\sigma}^2)`. Each output function maps points in the input domain to real numbers.
                :math:`\hat{y}` represents the model's best estimate of the objective function, and :math:`\hat{\sigma}^2` 
                is the estimated error of the prediction :math:`\hat{y}`.
            init_sampler (function): a function which will select initial sample points, informing the zero-generation model. 
                If left unspecified, is by default set to a :math:`2k+2`-sample latin hypercube over the domain,
                created with :mod:`smbo.latin_hypercube`.
            plot_res(float): the resolution of the created plots
            brute_optimize_EI(bool): if true, the expected improvement function is maximized by actually evaluating it over a plot_res grid and choosing the argmax. If False, it is maximized by a scipy optimizer. This allows for extremely slow, but trustworthy optimization.
                
        Returns:
            An object with attributes duplicating domain, objective_func, and modeller. Further, the class method 
            :func:`initialize` is called, which picks initial sample points, evaluates the objective function at 
            those points, and generates an inital predictive model with modeller. This object is then ready to 
            iteratively improve its predictions and seek the global minimum of objective_func; the object now has fields
            self.X, self.Y, self.y_hat, and self.err_hat to describe the sample points, corresponding objective values,
            predictor function, and certainty function respectively.
        """
        self.domain = domain
        #input dimension
        self.k = len(self.domain)
        self.objective_func = objective_func
        self.plot_res=plot_res
        self.plot_points=self.make_grid(plot_res)
        self.brute_optimize_EI=brute_optimize_EI
        
        # set initial sample points (in the sample vector X) using init_sampler (default latin hypercube)
        # because it is only once, no need to store a self.init_sampler
        if not init_sampler:
            # use Jones' convention of 2k+2 sample points for the 2k+2 free variables in the DACE model
            self.X=samplers.latin_hypercube(2*self.k+2,self.k,self.domain)
        else:
            self.X=init_sampler()
        self.n = len(self.X)
        # get objective values for initial sample points
        self.Y=[self.objective_func(x) for x in self.X]
        
        # now initialize the model:
        self.modeller = modeller
        # get prediction function and prediction error [prediction] function
        self.pred_y, self.pred_err = self.modeller(self.X,self.Y)
        
    @lazyprop
    def improvement_buffer(self):
        """
        Stores expected improvement values for each point on the plot_point grid
        """
        return [self.exp_improvement(point) for point in self.plot_points]
        
    @lazyprop
    def prediction_buffer(self):
        """
        Stores predicted function values for each point on the plot_point grid
        """
        return [self.pred_y(point) for point in self.plot_points]

    @lazyprop
    def error_buffer(self):
        """
        Stores predicted function error values for each point on the plot_point grid
        """
        return [self.pred_err(point) for point in self.plot_points]
        
        
        
    def make_grid(self, res):
        """
        Args:
            res (float): the resolution of the k-dimensional grid
        Returns:
            np.array: a grid with k-dimensional cubes with side-length res
        """
        n_samples = int(round((self.domain[0][1]-self.domain[0][0])/res))
        step_sizes = [(self.domain[i][1]-self.domain[i][0])/n_samples for i in range(self.k)]
        samples = np.array([[self.domain[i][0]+step_num*step_sizes[i] for i in range(self.k) for step_num in range(n_samples)]])
        
        coords = np.array([np.arange(self.domain[i][0],self.domain[i][1],self.plot_res) for i in range(self.k)]).transpose()
        if (self.k>1):
            mesh = np.array(np.meshgrid(*coords))
            num_coords = len(mesh.flatten())/self.k
            grid = np.reshape(mesh, (num_coords,self.k))
            return grid
        else:
            return coords
        
                    
    @lazyprop 
    def f_min(self):
        """
        Returns:
             dict: {x: xcoord, y: ycoord}, simply the (x,y) sample point with the lowest y value (the current best-minimum)
        """
        min_index = np.argmin(self.Y)
        return ( { 'x': self.X[ min_index ], 'y': self.Y[ min_index ] } )
        
    # expected improvement function (Jones Eq. 15) (eps is included for floating point rounding errs)
    def exp_improvement(self, x_new):
        """
        Args:
            x_new (list): a coordinate in the domain
        Returns:
            float: the expected improvement function (Jones Eq. 15) evaluated at x_new
        This function informs the decision of where to sample next
        """
        # should predict(x) be stored lazily? don't want to double-call the predictor function
        # (maybe unnecessary; is the predictor function ever explicitly used in the iterative process?)
        y = self.pred_y(x_new)
        # improvement over current minimum
        improvement = max(self.f_min['y'] - y,0.0)
        
        # s
        err = self.pred_err(x_new)
        if (err < 0):
            print('Error: pred_err(x) < 0 for x = ' + str(x_new) + '; pred_err(x) = ' + str(err))
        
        st_dev = sqrt(self.pred_err(x_new))
        
        # catches when x_new is in X (already evaluated points, 100% certain of prediction)
        if (st_dev == 0.0): return(0.0)
        
        normed_improvement = improvement/st_dev
        
        return(improvement * norm.cdf(normed_improvement) + st_dev * norm.pdf(normed_improvement))
    
    @lazyprop
    def next_sample(self):
        """
        Args:
            randomize (bool): if true, the next sample point is chosen randomly with probability weighted by expected improvement; otherwise, returns the point in the input domain with the highest expected improvement. NOTE: does nothing for now. Disabled!
        Chooses the next sample point
        """  
        if self.brute_optimize_EI:
            return self.plot_points[np.argmax(self.error_buffer)]
        else: 
            return self.improvement_data.x
        
    @lazyprop
    def improvement_data(self):
        """
        So that it may be accessed by different class methods, this stores the maximization
        result of the expected improvement function
        """
        def neg_imp(x_new): return -(self.exp_improvement(x_new))
        # initial minimization guess in the center of the n-rectangle of interest
        x0 = [(self.domain[i][1]+self.domain[i][0])/float(2) for i in range(self.k)]
        res = minimize(neg_imp, x0, method='SLSQP',bounds=self.domain)
        return res        
    
    def sample(self, randomize=False):
        """
        Args:
            randomize (bool): whether the sample is chosen randomly by next_sample
        Chooses the next sample point, evaluates the objective function, and fits the model
        """
        self.X = np.append(self.X, np.array(self.next_sample))
        self.Y = np.append(self.Y, self.objective_func([self.X[self.n]]))
        self.n += 1
        # Append flattens the array; this fixes
        self.X.resize(self.n,self.k)
        self.Y.resize(self.n)
        self.pred_y, self.pred_err = self.modeller(self.X,self.Y)
        reset_lps(self)
        
    def check_memory(self, eps=1e-6):
        """
        Args:
            eps (float): the margin of error
        Returns:
            bool: checks whether the predictor function correctly interpolates, i.e., if
                the predicted function value matches the observed function value at all sample points
        """
        for i in range(len(self.X)):
            if abs(self.pred_y(self.X[i])-self.Y[i]) > eps:
                return False
        return True
        
    def dim_plotter(plot_dims):
        """
        helper function for selecting either plot1d or plot2d
        """
        if type(plot_dims)==int:
            return self.plot1d
    
    def take_samples(self, stopping_improvement=0.01, max_iters=100, plot_dims=None, fname='plots/', randomize=False,verbose=True):
        """
        Args:
            stopping_improvement(float): the iterative process terminates if the maximum expected improvement anywhere is larger than this value
            num_iters (int): maximum number of successive sample points to be chosen
            plot_dims (int) or (list): the one, or two dimensions along which plots should be saved.
            fname (string): the prefix of the filename of each file to be saved
            randomize (bool): disabled; being passed along
        Iteratively chooses a sample point, evaluates the objective function, and refits the model
        """
        # generate inital plots
        if (type(plot_dims)==int):
            self.plot1d(fname=fname+'0.pdf',plot_objective=True)
        for i in range(max_iters):
            if verbose: 
                print('best place to sample: '+str(self.next_sample))
                print('expected improvement there: '+str(self.exp_improvement(self.next_sample)))
            # look at the expected improvement of the best sample point
            if self.exp_improvement(self.next_sample)<=stopping_improvement: return
            self.sample(randomize)
            if (type(plot_dims)==int):
                self.plot1d(fname=fname+str(i+1)+'.pdf',plot_objective=True)
            
        
        
    def plot1d(self, dim=0, plot_objective=False, plot_improvement=True, plot_next_sp=True, show_plot=False, fname=None):
        """
        Args:
            plot_objective (bool): whether the objective function should be plotted. This is only feasible if that function can be called enough times to generate a smooth plot
            plot_improvement (bool): option to overlay expected emprovement at each x
            plot_next_sp (bool): whether the selection of the next sample point is plotted
            show_plot (bool): whether pyplot.show is called at the end of the function
            dim (int): the index of the dimension of interest
            x_delta (float): the resolution of the plot
            fname: if set, the plot is saved to this
        Uses pyplot to make a nice 1d plot of the predictor function and its error. Optionally, overlay a plot of the
        """
        x_min=self.domain[dim][0]
        x_max=self.domain[dim][1]
        
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        plt.xlabel('x')
        ax.set_ylabel('predicted y(x)')
        plt.title('Predictor Surface with '+str(self.n)+' samples')
        
        pred_range = np.arange(x_min, x_max, self.plot_res)
        preds  = self.prediction_buffer
        # errors are illustrated with 2 times sigma (two standard devs)
        # to illustrate a 95% confidence interval
        errors = self.error_buffer
        # elem-wise sum/difference of above two arrays
        pl_errors = map(add, preds, errors)
        mi_errors = map(sub, preds, errors)
        
        # plot the predictor and +/- errors
        pred_line,  = ax.plot(pred_range, preds)
        p_err_line, = ax.plot(pred_range, pl_errors, color="green")
        m_err_line, = ax.plot(pred_range, mi_errors, color="green")
        
        
        if plot_objective:
            obj = [ self.objective_func([x]) for x in pred_range ]
            exp_imp_line, = ax.plot( pred_range, obj, color='k' )
        
        y_min=np.amin(preds)-np.amax(errors)
        y_max=np.amax(preds)+np.amax(errors)
        plt.axis([x_min, x_max, y_min, y_max])
        
        
        
        # make another axis (exp improv. is at a smaller scale than predictor)
        # plot the expected improvement
        if plot_improvement:
            ax2 = ax.twinx()
            imps = [ self.exp_improvement([x]) for x in pred_range ]
            # if you're plotting, might as well use that info for maximization
            exp_imp_line, = ax2.plot(pred_range, imps, color='r')
            ax2.set_ylabel('expected improvement', color='r')
            for tl in ax2.get_yticklabels():
                tl.set_color('r')            
                
        # plot the actual sample points
        points = ax.plot([x[dim] for x in self.X],self.Y, 'ko')
        # plot a vertical dotted line at the next sample point
        if plot_next_sp:
            point = ax.axvline(self.next_sample, color='k', linestyle='dotted')
            
        if fname:
            # bbox is tight bc I'll add margins in latex if I want to, thankyouverymuch
            plt.savefig(fname, bbox_inches='tight')
            
            
            
        if show_plot: plt.show()
        plt.close()
        
        