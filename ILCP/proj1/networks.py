from random import randint

class node:
    
    # I can imagine label being an int or a string,
    def __init__(self, label, index, links, x=0, y=0):
        self.label = label # this node's name
        self.index = index 
        self.links = links # outgoing edge destination indices
        self.x = x # position
        self.y = y
        
        
    # should produce a string defining a circle
    # within an html svg element
    def html_node(self, fill='white', stroke='black', r=15):
        return('<circle cx="%d" cy="%d" r="%d" stroke="%s" fill="%s" /> ' % (self.x, self.y, r, stroke, fill) )
      
    # produces a string which is a list of lines, one for each link
    # needs an up-to-date list of correctly-indexed nodes
    def html_links(self, nodes, color='black', fillstroke='4'):
        links = [
            '<line x1="%d" y1="%d" x2="%d" y2=%d color="%s" fillstroke="s" />' % (self.x, self.y, nodes[out].x, nodes[out].y, color, fillstroke)
            for out in self.links
        ]
        return '\n'.join(links)
        
    
# returns a list of random x,y tuples
class rand_positions(n, xmax, ymax):
    return( [ ( randint(1,xmax), randint(1,ymax) ) for i in range(n) ] )
    
# a network contains a matrix representation of a graph, as well
# as each node object

class network:
    
    
    def __init__(self, net_graph, position_scheme='random'):
        
        self.graph = net_graph
        self.n = len(net_graph)
        positions = rand_positions(n,500,500) if position_scheme=='random' else raise NameError('Unrecognized position scheme: %s' % position_scheme)
        self.nodes = [ node(
            label=i,
            links=net_graph[i]
            x=positions(i[0])
            y=positions(i[1])
        ) for i in range(n) ]
        
    # produces a string that is an html svg object which illustrates the graph.
    # here_node is colored differently, and link_nodes are links which are
    # colored differently. both here_node and link_nodes work by node index
    def html_svg(self, here_node=None, link_nodes=[]):
        here_node_color = 'black'
        link_node_color = 'grey'
        else_node_color = 'white'
        
        # draw the edges (each edge is drawn twice but whatever, this will only run once)
        edges = '\n'.join( [ nodey.html_links(nodes) for nodey in self.nodes ] )
    
        def node_color(i):
            if i == here_node return here_node_color
            elif i in link_nodes return link_node_color
            else return else_node_color
            
        nodes = '\n'.join( [ nodey.html_node( fill=node_color(i) ) ] )
        
        return( edges+'\n'+nodes )
        
        
        
        