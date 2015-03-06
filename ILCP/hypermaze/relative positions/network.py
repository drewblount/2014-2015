from random import randint, random
from node import node
import os


def zero_tuples(n):
    return [(0,0) for i in range(n)]

# returns a list of random x,y tuples
def rand_positions(n, xmax, ymax, buffer=15):
    return( [ ( randint(1+buffer,xmax-buffer), randint(1+buffer,ymax-buffer) ) for i in range(n) ] )
    
# a network contains a matrix representation of a graph, as well
# as each node object
class network:
    
    # outlink is a dictionary {link: string, x: int, y: int}
    def __init__(self, net_graph, fname='', position_scheme='random', xdim=100, ydim=100, lweight=3, goal_node=True, outlink=None):
        
        self.name = fname
        self.graph = net_graph
        self.n = len(net_graph)
        self.xdim, self.ydim = xdim, ydim
        positions = rand_positions(self.n,xdim,ydim) if (position_scheme=='random') else zero_tuples(self.n) 
        self.nodes = [ 
            node(
            label='node_%d'%i, 
            index=i, 
            links=[j for j in range(self.n) if (self.graph[i][j]>0)], 
            x=positions[i][0], 
            y=positions[i][1]
        ) for i in range(self.n) ]
        
        # goal node index
        self.goal = self.n-1 if goal_node else None
        # no outgoing links for goal node
        if self.goal:
            self.nodes[self.goal].links = []
        self.outlink = outlink
        
    
        
    # ensures a path from the first to last node 
    # (but no link leaving self.goal)
    def ensure_path(self):
        for nodey in self.nodes:
            if nodey.index != self.goal:
                next = nodey.index + 1 % self.n
                if next not in nodey.links: nodey.links += [next]
        
    def link_to_point(self, link, x, y):
        if link[-5:0] != '.html':
            link+='.html'
        self.outlink = {'link':link, 'x':x, 'y':y}
        
    # links this network to another one:
    # sets this.outlink, and (for smoothing the transition between viewing
    # one network and the next) makes sure that the other network's
    # second node is at the same coordinates as this net's goal
    def link_to(self, othernet, othernet_num):
        othernode_address='../net_%d/node_0' % othernet_num
        otherx = othernet.nodes[0].x
        othery = othernet.nodes[0].y
        self.link_to_point(othernode_address, otherx, othery)
        # now set coords of othernet's #1 node, which will be connected
        # to #0 if ensure_path has been run, to equal self.goal
        othernet.nodes[1].x = self.nodes[self.goal].x
        othernet.nodes[1].y = self.nodes[self.goal].y
    # this is the html when you reach the goal node-- it will show only
    # the goal node and a line connecting it to another black node which,
    # when clicked, takes you to another network
    def goal_html(self):
        goal = self.nodes[self.goal]
        old_net_node = goal.html_node(fill='white', stroke='black', fillstroke=4)
        x, y, r = self.outlink['x'], self.outlink['y'], 10
        
        stroke, fill, fillstroke = 'FireBrick', 'FireBrick', 4
        new_net_node = '<circle cx="%d" cy="%d" r="%d" stroke="%s" fill="%s" stroke-width="%d"/> ' % (x, y, r, stroke, fill, fillstroke)
        
        # make new node a link
        new_net_node = '<a xlink:href = %s> '%self.outlink['link']+new_net_node+'</a>'
        
        line = '<line x1="%d%%" y1="%d%%" x2="%d%%" y2="%d%%" style="stroke:black;stroke-width:2" />' % (goal.x, goal.y, x, y)
        
        
        
        svg = '\n'.join( [
            '<svg width = "%d%%" height = "%d%%" >' % (self.xdim, self.ydim),
            line,
            old_net_node,
            new_net_node,
            '</svg>'
        ] )
        return svg
    
        
    # produces a string that is an html svg object which illustrates the graph.
    # here_node is colored differently, and link_nodes are links which are
    # colored differently. both here_node and link_nodes work by node index
    def html_svg(self, here_node=None):
        # draw the edges (each edge is drawn twice but whatever, this will only run once)
        
        if here_node==self.nodes[self.goal]:
            return self.goal_html()
        
        links = [] if not here_node else here_node.links
        def link_weight(i):
            return 4 if here_node and here_node.index==i else 1
            
        edges = [ nodey.html_links( self.nodes, fillstroke=link_weight(nodey.index) ) for nodey in self.nodes ]
        edges = '\n'.join( edges )        
    
        def node_color(i):
            # if there's no here_node, default to else_node_color
            if not here_node:
                return  self.nodes[i].default_color
            elif (i == here_node.index): return self.nodes[i].here_color
            elif (i in here_node.links): return self.nodes[i].link_color
            else: return self.nodes[i].default_color
    
        
        # if here_node, only draw here_node and its neighbors
        node_indices = range(self.n) if not here_node else here_node.links+[here_node.index]
        
        
        nodes =  [ self.nodes[i].html_node( fill=node_color(i), link=i in links, fillstroke=link_weight(i)) for i in node_indices ]
        
        if self.goal: 
            nodes += [self.nodes[
                self.goal
            ].html_node(fill='FireBrick', link=self.goal in links, stroke='FireBrick', fillstroke=link_weight(self.goal in links))]
            
        nodes = '\n'.join( nodes )
        
        # add svg tag on beginning and end
        svg = '\n'.join( [
            '<svg width = "%d%%" height = "%d%%" >' % (self.xdim, self.ydim),
            edges,
            nodes,
            '</svg>'
        ] )
        return svg
        
    # saves a fname.html depicting the graph
    def save_html(self, fname='', here_node=None):
        svg = self.html_svg(here_node)
        fname = self.name+fname
        
        if here_node:
            fname = fname + here_node.label
        with open(fname+'.html', 'w') as file:
            file.write('''
<html>
<body>
%s
</body>
</html>
''' % svg)
            file.close()
        
    # saves an .html for each node, with that node's neighbors as
    # hyperlinks
    def write_htmls(self, dirname=''):
        dirname = self.name+dirname
        
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        for nodey in self.nodes:
            self.save_html(fname = dirname+'/', here_node=nodey)
        
        
# returns a 2d array which is a random edge graph; d = degree, avg number of
# links from a node.
def rand_graph(n, d):
    link_prob = float(d)/n
    return [ [ 1 if random() < link_prob else 0 for i in range(n)] for j in range(n)]
    
# calls init above with a random incidence matrix with n nodes
# of average degree d
def rand_net(n, d, name=''):
    return network(rand_graph(n,d), fname='')
