## This is a playground for applying the EGO algorithm on small
## toy problems.
##
## My highest priority will be visualizing everything.
##
## I'll first consider the case where the black-box function (BBF) has
## one input dimension, and I'll try and reproduce figures like Fig. 9
## in the original Jones et al EGO paper.

import matplotlib.pyplot as plt
## import my code
##from dace import *

## X is the vector of input vectors, Y output
X = [[1.5],[3.5]]
Y = [[0.25],[0.75]]

## Plot the evaluated input/outputs
plt.scatter(X, Y)

## generate the predictor function:
## DACE parameters p and theta (only one of each)
P = [[1.0]]
Q = [[1.0]]
predictor = dace_predictor(X,Y,P,Q)

pred_range = np.arange(0.0, 5.0, 0.01)
plt.plot(pred_range, predictor(pred_range))


## generate the estimated error function:


## Evaluate the likelihood of these Ys given Xs, Ps, Qs:



plt.axis([0,5,0,1])
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Toy Problem')

plt.show()



