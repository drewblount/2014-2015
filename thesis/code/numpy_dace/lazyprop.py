## This file contains a function that allows for easy, lazy evaluation
## of object parameters. From Mike Boers' response to detly on StackExchange:
## http://stackoverflow.com/questions/3012421/python-lazy-property-decorator

## MOTIVATION:
## The ego solver object ("egoist")'s methods rely on a number of linear
## algebraic objects, such as the correlation matrix R or input
## vector array X. Products of these, such as Y.T.dot(la.inv(R)).dot(Y),
## are often reused.

## my goal here is to meet three requirements with the handling of those
## linear algebraic objects and their multiplication:
##    + results should be saved as egoist object parameters, so that 
##      the same matrix multiplication is never performed twice
##    + results should be lazily evaluated, so no unnecessary computation
##      is performed
##    + when some relevant parameters are adjusted (e.g., P or Q is modified,
##      of another input-output result is added), all the related
##      properties are deleted (the ones which now must be re-evaluated)

def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop

def delete_lp(self, fn):
    attr_name = '_lazy_' + fn.__name__
    del self.attr_name
    
## Example code: (from above-linked StackExchange)
"""
class Test(object):

    @lazyprop
    def a(self):
        print 'generating "a"'
        return range(5)
>>> t = Test()
>>> t.__dict__
{}
>>> t.a
generating "a"
[0, 1, 2, 3, 4]
>>> t.__dict__
{'_lazy_a': [0, 1, 2, 3, 4]}
>>> t.a
[0, 1, 2, 3, 4]
"""