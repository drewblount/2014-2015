
num_dims = 10
num_samples = 10

from random import random
from dace import *

xs = [[random()*5 for i in range(num_dims)] for j in range(num_samples)]
# same with the values in ys
ys = [random() * 10 for i in range(num_samples)]
# ps from [1, 2)
ps = [random() + 1 for i in range(num_dims)]
# qs from [0.0, 1.0)
qs = [random() for i in range(num_dims)]

corr = corr_func(qs, ps)

dist = dist_func(qs,ps)

R = corr_matrix(xs, qs, ps)
R_inv = R.I
# naming vars so they aren't computed more than once
R_inv_y = R_inv * matrix(ys)
ones = matrix([1 for i in range(len(xs))])
ones_T = ones.T
ones_T_R_inv = ones_T * R_inv

# Regression term -- Jones Eq 5
mu_hat = ones_T * R_inv_y / (ones_T_R_inv * ones)

# correlation function
corr = corr_func(qs, ps)

dist = dist_func(qs,ps)