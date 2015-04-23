"""
.. module:: tests.plot
   :platform: Unix, Windows
   :synopsis: tests 2d plotting

.. moduleauthor:: Drew Blount <dblount@reed.edu>

"""

from smbo import np, plt
import matplotlib.mlab as mlab
from test_funcs import branin, branin_domain

delta = 0.25
dom = branin_domain()
x = np.arange(dom[0][0], dom[0][1], delta)
y = np.arange(dom[1][0], dom[1][1], delta)
X, Y = np.meshgrid(x, y)
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
# difference of Gaussians
print(str(Y[0]))
Z = [ [ branin( [X[i][j], Y[i][j]] ) for j in range(len(X[i]) )] for i in range(len(X))]
plt.figure()
CS = plt.contour(X, Y, Z,100)
plt.title('branin test')

plt.show()