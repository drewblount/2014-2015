thesis/code/numpy_dace
======================


After doing some big data operations in numpy this summer, it's the most natural environment for me to throw together simple and powerful sketches. Here, my goal is to replicate the DACE predictor presented in Jones, Schonlau, and Welch, 1998: Efficient Global Optimization of Expensive Blackbox Functions.


Done:
------
 + dace.py contains the function dace_predictor, which takes a vector of input vectors xs, evaluated outputs ys, and regression terms ps and qs (qs = Jones et al's thetas), and returns the prediction function described on page 461, Eq. 7


To do:
-------
 + make process to derive regression terms ps and qs, given xs and ys--see section 4.4 of the paper on using a 'nonconvex relation' to estimate ps and qs
   ++ why/when can you assume that all ps == 2?

