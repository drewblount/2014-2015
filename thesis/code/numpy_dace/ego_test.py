from ego import *
from random import random

# Reality check: does the predictor predict each already-evaluated function value?
def pred_y_check(E, verbose=False, eps = 0.0001):
    allmatch = True
    for i in range(E.n):
        x, y = E.X[i], E.Y[i]
        y_hat = E.predict(x)
        match = abs(y-y_hat)<eps
        if verbose:
            print('x = '+str(x)+', y = '+str(y)+', y_hat = '+str(y_hat)+'. match = '+str(match))
        allmatch = allmatch and match
    if verbose:
        print('The predictor %s the already evaluated points.' % ('accurately predicts' if allmatch else 'does not accurately predict'))
    return allmatch
    
    
    
X = [[1.5],[3.5],[2.5],[3.0],[0.5]]
Y = [0.25,0.75,0.9,0.8,0.1]
E = egoist(X, Y)

print E.R

pred_y_check(E,True)

for _ in range(10):
    x = random()*10
    print('The error at x = '+str(x)+' is ' + str( E.pred_err([x]) ) )
    
E.plot1d()