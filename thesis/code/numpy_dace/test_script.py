from dace_visualizer import *

# this file will be an oft-overwritten notepad for little test scripts
# I use as I go along


def likelihood_test(plot=True):
    # made-up data
    X = [[1.5],[3.5],[2.5],[3.0],[0.5]]
    Y = [[0.25],[0.75],[0.9],[0.8],[0.1]]
    Y = [0.25,0.75,0.9,0.8,0.1]
    return likelihood_map(X, Y,Pmin=1.0,Pmax=1.3,Qmin=2.5,Qmax=3.5,P_res=0.0025,Q_res=0.025)
    
test_data = likelihood_test()


from ego import *
X = [[1.5],[3.5],[2.5],[3.0],[0.5]]
Y = [0.25,0.75,0.9,0.8,0.1]
E = egoist(X, Y)