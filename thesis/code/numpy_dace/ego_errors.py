class dim_error(Exception):
    def __init__(self, dim, desired_dim=1):
        self.dim = dim
        self.desired_dim = desired_dim
    def __str__(self):
        return ('')
...     def __init__(self, dim, desired_dim=1):
...         self.dim = dim
...     def __str__(self):
...         return repr(self.value)
...
>>> try:
...     raise MyError(2*2)
... except MyError as e:
...     print 'My exception occurred, value:', e.value