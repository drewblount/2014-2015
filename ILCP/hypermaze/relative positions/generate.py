from network import *

n_nets  = 2
net_ids = range(n_nets)

# nets is the array of networks
nets = []
for i in net_ids:
    n_nodes = 5
    degree = 3
    newnet = rand_net(n_nodes, degree, name='net_%d' % i)
    newnet.ensure_path()
    nets.append(newnet)
    

for i in net_ids:
    link_n = (i+1) % n_nets
    # link each network to the one after it
    nets[i].link_to( othernet=nets[ link_n ], othernet_num=link_n )

for i in net_ids:
    # save a skeleton image of the network
    nets[i].save_html()
    # save each of the network's node htmls
    nets[i].write_htmls(dirname='net_%d' % i)
    
    
#cd html/hypermaze
#put node*
    