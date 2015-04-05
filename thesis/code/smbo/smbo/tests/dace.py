"""
.. module:: tests.dace
   :platform: Unix, Windows
   :synopsis: tests the DACE modeller defined in smbo.models

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""

from ..models    import dace, dace_function
from ..samplers  import latin_hypercube
from .test_funcs import sinusoparaboloid

def main_test(ndims = 3):
    """
    Args:
        ndims(int): the dimensionality of the sample space to be tested.
    """
    F = sinusoparaboloid()
    X = latin_hypercube(3,ndims)
    Y = [F(x) for x in X]
    
    pred_func, pred_err = dace_function(X,Y)
    
    print('Testing the DACE module:')
    print('    X = '+str(X))
    print('    Y = '+str(Y))
    print('    pred_func = '+str(pred_func))
    print('    pred_err = '+str(pred_err))
    print('    pred_func correctly predicts sample points: ' +str(check_memory(X,Y,pred_func)))
    
    
def check_memory(X,Y,pred_func,eps=1e-6):
    """
    Args:
        X (list): the sample points' input coords
        Y (list): the sample points' output values
        pred_func (func): a predictor function which should match xs with ys
        eps (float): the margin of error
    Returns:
        bool: the truth value of the statement, "pred_func(x)=y (within eps) for all corresponding x,y"
    """
    for i in range(len(X)):
        if abs(pred_func(X[i])-Y[i]) > eps:
            return False
    return True    
    