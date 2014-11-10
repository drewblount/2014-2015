from dace_visualizer import *

# this file will be an oft-overwritten notepad for little test scripts
# I use as I go along


def likelihood_test(plot=False):
    # made-up data
    X = [[1.5],[3.5],[2.5],[3.0],[0.5]]
    Y = [[0.25],[0.75],[0.9],[0.8],[0.1]]
    return likelihood_map(X, Y)
    
test_data = likelihood_test()