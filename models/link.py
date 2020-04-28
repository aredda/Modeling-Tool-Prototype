from tkinter import * 

class Link(object):

    TOP = 't'
    RIGHT = 'r'
    DOWN = 'd'
    LEFT = 'l'

    def __init__(self, item1, item2, canvas: Canvas):
        self.item1 = item1
        self.item2 = item2
        self.canvas = canvas
        self.linkInstance = -1

    def get_port (canvas: Canvas, item, port):
        x1, y1, x2, y2 = canvas.coords (item)
        width, height = (x2 - x1), (y2 - y1)
        
        ports = {}
        ports[Link.RIGHT] = (x2, y1 + height/2)
        ports[Link.LEFT] = (x1, y1 + height/2)
        ports[Link.TOP] = (x1 + width/2, y1)
        ports[Link.DOWN] = (x1 + width/2, y2)
        
        return ports[port]

    def get_linkable_ports(self):
        coords1 = self.canvas.coords(self.item1)
        coords2 = self.canvas.coords(self.item2)
        c1 = (coords1[0] + self.get_width(self.item1) / 2, coords1[1] + self.get_height(self.item1) / 2)
        c2 = (coords2[0] + self.get_width(self.item2) / 2, coords2[1] + self.get_height(self.item2) / 2)
        dist = (c2[0] - c1[0], c2[1] - c1[1])
        
        # If the horizontal magnitude is bigger than the vertical magnitude
        if abs(dist[0]) > abs(dist[1]):
            return {
                self.item1: Link.get_port(self.canvas, self.item1, Link.RIGHT if c1[0] < c2[0] else Link.LEFT),
                self.item2: Link.get_port(self.canvas, self.item2, Link.LEFT if c1[0] < c2[0] else Link.RIGHT)
            }

        return {
            self.item1: Link.get_port(self.canvas, self.item1, Link.DOWN if c1[1] < c2[1] else Link.TOP),
            self.item2: Link.get_port(self.canvas, self.item2, Link.TOP if c1[1] < c2[1] else Link.DOWN)
        }
            
    def get_width(self, item):
        x1, y1, x2, y2 = self.canvas.coords (item)
        width = x2 - x1

        return width

    def get_height(self, item):
        x1, y1, x2, y2 = self.canvas.coords (item)
        height = y2 - y1

        return height

    def draw_link(self, **options):
        points = []
        for p in self.get_linkable_ports().values(): points.append (p)
        self.linkInstance = self.canvas.create_line(points, **options)
        return self.linkInstance

    def update_link(self):
        if self.linkInstance == -1:
            return

        points = []
        for port in self.get_linkable_ports().values(): 
            points.append(port[0])
            points.append(port[1])
        self.canvas.coords(self.linkInstance, points)

    