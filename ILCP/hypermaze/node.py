class node:
    
    # I can imagine label being an int or a string,
    def __init__(self, label, index, links, x=0, y=0, default_color='white', link_color='white',here_color='black'):
        self.label = label # this node's name
        self.index = index 
        self.links = links # outgoing edge destination indices
        self.x = x # position
        self.y = y
        
        self.default_color = default_color
        self.link_color = link_color
        self.here_color = here_color
        
        
    # should produce a string defining a circle
    # within an html svg element
    # the link url is (self.label).html
    def html_node(self, fill='self.default_color', stroke='black', r=10, link=False, is_sq=False, fillstroke=3):
        circ = '<circle cx="%d" cy="%d" r="%d" stroke="%s" fill="%s" stroke-width="%d"/> ' % (self.x, self.y, r, stroke, fill, fillstroke)
        if link:
            return '<a xlink:href = %s.html> '%self.label + circ + ' </a>'
        else:
            return circ
      
    # produces a string which is a list of lines, one for each link
    # needs an up-to-date list of correctly-indexed nodes
    def html_links(self, nodes, color='black', fillstroke=2):
        links = [
            '<line x1="%d" y1="%d" x2="%d" y2=%d style="stroke:%s;stroke-width:%d" />' % (self.x, self.y, nodes[out].x, nodes[out].y, color, fillstroke)
            for out in self.links
        ]
        return '\n'.join(links)
        
    
