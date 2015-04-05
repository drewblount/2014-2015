"""
.. module:: tests.smb_opt
   :platform: Unix, Windows
   :synopsis: tests the smb_optimizer class with the DACE model

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""

from ..models    import  dace_function
from ..samplers  import latin_hypercube
from ..smb_optimizer  import smb_optimizer
from .test_funcs import sinusoparaboloid

def sample_test():
    """
    Sets up some sample inputs and runs them through the EGO algorithm
    """
    domain=[[0,5]]
    # A test function with a global minimum near (5)
    obj_F = sinusoparaboloid(1,1,2.5,sin_strength=0.01)

    test = smb_optimizer(domain, obj_F, dace_function)
    print('Testing the smbo package:')
    print('    X = '+str(test.X))
    print('    Y = '+str(test.Y))
    print('    pred_func = '+str(test.pred_y))
    print('    pred_err = '+str(test.pred_err))
    print('    pred_func correctly predicts sample points: ' +str(test.check_memory()))
    print('    next best sample point: ' + str(test.choose_sample()))
    test.plot1d(plot_objective=True,fname='testplot.pdf')
    test.take_samples(5)
    
    
sample_test()