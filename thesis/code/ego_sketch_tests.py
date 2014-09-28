from ego_sketch import *

# generates random data and random regressor values qs and ps
# to feed to dace_predictor
def dace_predictor_test(num_dims, num_samples, num_tests = 2, verbose=True):
    # the values in xs are random in [0.0, 100.0)
    xs = [[random()*100 for i in range(num_dims)] for j in range(num_samples)]
    # same with the values in ys
    ys = [random() * 100 for i in range(num_samples)]
    # ps from [1, 2)
    ps = [random() + 1 for i in range(num_dims)]
    # qs from [0,10)
    qs = [random() * 10 for i in range(num_dims)]
    
    pred_func = dace_predictor(xs, ys, ps, qs)
    
    test_inputs = [random() * 100 for i in range(num_tests)]
    
    for i in range(num_tests):
        y = pred_func(test_inputs[i])
        if verbose: print 'predicted output of %.2f is %.2f' % (test_inputs[i], y)
        
    # so interpreter user can play with it
    return pred_func
    
