"""
.. module:: lazyprop
   :platform: Unix, Windows
   :synopsis: This file contains a function that allows for easy, lazy evaluation
       of object parameters. The dace class methods rely on a number of linear
       algebraic objects, such as the correlation matrix R or input
       vector array X. Products of these, such as Y.T.dot(la.inv(R)).dot(Y),
       are often reused.
       My goal here is to meet three requirements with the handling of those
       linear algebraic objects and their multiplication:
           + results should be saved as egoist object parameters, so that 
             the same matrix multiplication is never performed twice
           + results should be lazily evaluated, so no unnecessary computation
             is performed
           + when some relevant parameters are adjusted (e.g., P or Q is modified,
             of another input-output result is added), all the related
             properties are deleted (the ones which now must be re-evaluated)
    From Mike Boers' response to detly on StackExchange:
    http://stackoverflow.com/questions/3012421/python-lazy-property-decorator
.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""

def lazyprop(fn):
    """
    Args:
        fn (function): a function, whose only argument is self, whose output shouldn't
            be computed more than once for a given X,Y pair.
    Returns:
        function:
            _lazyprop: a function that calls fn the first time it is called, then remembers 
                that output and returns this remembered value after subsequent calls
    """
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop

def reset_lps(self):
    """
    Resets all lazyprops, so that the evaluated function vals are forgotten and must be
    recomputed from raw data
    """
    lazy_keys = [k for k in self.__dict__ if (k[0:6] == '_lazy_') ]
    for key in lazy_keys:
        delattr(self, key)