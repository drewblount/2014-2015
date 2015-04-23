"""
.. module:: tests.smb_opt
   :platform: Unix, Windows
   :synopsis: tests the smb_optimizer class with the DACE model

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""

from ..models    import  dace_function
from ..samplers  import latin_hypercube, diag
from ..smb_optimizer  import smb_optimizer
from .test_funcs import sinusoparaboloid, branin, branin_domain

from datetime import datetime
import logging
logging.basicConfig(filename=__name__+'.log',level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('\n------------------------\nNew test log at ' +str(datetime.today()))

def sample_test():
    """
    Sets up some sample inputs and runs them through the EGO algorithm
    """

    #test = smb_optimizer(branin_domain(), branin, dace_function, brute_optimize_EI=False)
    bounds = [[0,10]]
    width = bounds[0][1]-bounds[0][0]
    def fixed_sampler():
        return diag(6,1,bounds)
    def lher():
        return latin_hypercube(8,1,bounds)
    def fixed_lh():
        return [[1.2401768021409674], [6.412180558905743], [4.982912130389163], [8.269898346390113], [3.3601092758327518], [9.629361060595107], [5.207781969807999], [2.0566450769172135]]
    h = lher()
    print('LH is:\n'+str(h))
    test = smb_optimizer(bounds, sinusoparaboloid(1,3,width/2+0.5,2), dace_function, init_sampler=fixed_lh, brute_optimize_EI=False)
    print('Testing the smbo package:')
    #print('    X = '+str(test.X))
    #print('    Y = '+str(test.Y))
    #print('    pred_func = '+str(test.pred_y))
    #print('    pred_err = '+str(test.pred_err))
    #print('    pred_func correctly predicts sample points: ' +str(test.check_memory()))
    #print('    next best sample point: ' + str(test.choose_sample()))
    #test.take_samples(0.05,1)
    test.plot1d(show_plot=False,plot_objective=True,plot_err=True,fname='basinhopping.pdf')
    
print('name is '+__name__)
    
sample_test()