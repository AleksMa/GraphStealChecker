from pyglet import *
from pyglet.gl import *
from pyglet.window import *
import random
import math

window = pyglet.window.Window(800, 600, resizable=True)
pyglet.gl.glClearColor(0.0, 0.0, 0.0, 0)


class Node(object):

    def __init__(self, start = None, point = None, dist = None, intersection = None, exit_or_enter = None, jump = None):
        self.start = start
        self.prev = self
        self.next = self
        self.value = point
        self.jump = jump
        self.dist = dist
        self.intersection = intersection
        self.exit_or_enter = exit_or_enter
        self.changed = False
        

    def __eq__(self, other):
        return self.value == other.value

def list_empty(l):
    return l.next == l

def list_length(l):
    cur_len = 0
    x = l
    while x.next != l:
        cur_len += 1
        x = x.next
    return cur_len

def list_search(l, value):
    x = l.next
    while x != l and x.value != value:
        x = x.next
    return x

def insert_before_dist(l, node):
    x = l.next
    while x.dist < node.dist:
        x = x.next
    if (x.dist == node.dist):
        return
    insert_before(x, node)

def insert_after(x, y):
    z = x.next
    x.next = y
    y.prev = x
    y.next = z
    z.prev = y

def insert_before(x, y):
    insert_after(x.prev, y)

def detele(x):
    y = x.prev
    z = x.next
    y.next = x
    z.prev = y

    x.prev = None
    x.next = None

def insert_after_tail(x, y):
    l = list_search(x, None)
    insert_before(l, y)

def right_or_left(p1, p2, p3):
    return ((p3.x - p1.x) * (p2.y - p1.y) - (p3.y - p1.y) * (p2.x - p1.x)) > 0
    

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def print(self):
        return [self.x, self.y]

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

class Line(object):

    def __init__(self, p1, p2):
        self.x0 = p1.x
        self.y0 = p1.y
        self.a = p2.x - p1.x
        self.b = p2.y - p1.y
        
    def determination(self, other):
        return self.a * other.b - other.a * self.b


    def get(self, t):
        return Point(self.x0 + self.a * t, self.y0 + self.b * t)

    def intersection(self, other):
        det = self.determination(other)
        if det == 0:
            return None
        t =  ((other.x0 - self.x0) * other.b - (other.y0 - self.y0) * other.a) / det
        u =  ((other.x0 - self.x0) * self.b - (other.y0 - self.y0) * self.a) / det
        if 0 <= t <= 1 and 0 <= u <= 1:
            return self.get(t)
        else:
            return None

class Polygon(object):
    
    def __init__(self, node = None):
        self.RGB_main = [random.random(), random.random(), random.random()]
        self.RGB_sub = [random.random(), random.random(), random.random()]
        self.points_outside = node
        self.points_inside = []

    def add_inside_full(self, array):
        l = Node(True, array[0], array[0].distance(array[len(array) - 1]))
        for i in range(1, len(array)):
            insert_before(l, Node(False, array[i], array[i].distance(array[i - 1])))
        self.points_inside.append(l)

    def add_outside_full(self, array):
        l = Node(True, array[0], array[0].distance(array[len(array) - 1]))
        for i in range(1, len(array)):
            insert_before(l, Node(False, array[i], array[i].distance(array[i - 1])))
        self.points_outside = l

    def draw(self):
        glBegin(GL_LINES)
        glColor3f(*self.RGB_main)
        l = self.points_outside.next
        while l != self.points_outside:
            glVertex2f(l.prev.value.x, l.prev.value.y)
            glVertex2f(l.value.x, l.value.y)
            l = l.next
        glVertex2f(l.value.x, l.value.y)
        glVertex2f(l.prev.value.x, l.prev.value.y)
        glEnd()

        for i in range(len(self.points_inside)):
            l = self.points_inside[i].next
            glBegin(GL_LINES)
            glColor3f(*self.RGB_sub)
            while l != self.points_inside[i]:
                glVertex2f(l.prev.value.x, l.prev.value.y)
                glVertex2f(l.value.x, l.value.y)
                l = l.next
            glVertex2f(l.value.x, l.value.y)
            glVertex2f(l.prev.value.x, l.prev.value.y)
            glEnd()
                    
    

class Weilor(object):

    def __init__(self, polygon1, polygon2):
        self.pol1 = polygon1
        self.pol2 = polygon2
        self.enters = []
        self.lists_main = []
        self.lists_clip = []
        self.final = []

    def finds_intersections(self, outline1, outline2):
        found = False
        l = outline1.next
        while True:
            left_node = l.prev
            right_node = l
            p1 = left_node.value
            p2 = right_node.value
            line1 = Line(p1, p2)
            n = outline2.next
            while True:
                left = n.prev
                right = n
                p3 = left.value
                p4 = right.value
                line2 = Line(p3, p4)
                current_point = line1.intersection(line2)
                if current_point is not None:
                    found = True
                    enter = right_or_left(p1, p2, p3)
                    #(self, start = None, point = None, dist = None, intersection = None, exit_or_enter = None, jump = None):
                    current_node_1 = Node(False, current_point, p1.distance(current_point), True, enter)
                    current_node_2 = Node(False, current_point, p3.distance(current_point), True, not enter)
                    current_node_1.jump = current_node_2
                    current_node_2.jump = current_node_1
                    insert_before_dist(left_node, current_node_1)
                    insert_before_dist(left, current_node_2)
                n = n.next
                if n == outline2.next:
                    break
            l = l.next
            if l == outline1.next:
                break
        return found

    def find_enters(self, i = 0):
        l = self.lists_main[i].next
        while l != self.lists_main[i]:
            if (l.exit_or_enter):
                self.enters.append(l)
            l = l.next
            
    def create(self):
        self.lists_main.append(self.pol1.points_outside)
        self.lists_clip.append(self.pol2.points_outside)
        for i in range(len(self.pol1.points_inside)):
            self.lists_main.append(self.pol1.points_inside[i])
        for i in range(len(self.pol2.points_inside)):
            self.lists_clip.append(self.pol2.points_inside[i])

        for i in range(len(self.lists_main)):
            for j in range(len(self.lists_clip)):
                if self.finds_intersections(self.lists_main[i], self.lists_clip[j]):
                    self.lists_main[i].changed = True
                    self.lists_clip[j].changed = True

    def find_exit(self, enter):
        current_outline = []
        current_main = False
        current_outline.append(enter)
        current_node = enter.jump.next
        while current_node != enter:
            current_outline.append(current_node)
            if current_node.exit_or_enter is not None:
                if not current_main and current_node.jump.exit_or_enter == current_main:
                    current_node = current_node.jump
                    current_main = not current_main
                if current_main and current_node.exit_or_enter == current_main:
                    current_node = current_node.jump
                    current_main = not current_main
            current_node = current_node.next
        self.final.append(current_outline)

    #inside           
    def is_it_left(self, main, second):
        left = True
        l = main.next
        while True:
            current_point = l.value
            n = second.next
            while True:
                left_point = n.prev.value
                right_point = n.value
                if right_or_left(left_point, right_point, current_point):
                    left = False
                n = n.next
                if n == second.next:
                    break
            l = l.next
            if l == main.next:
                break
        return left

    def is_it_right(self, main, second):
        right = True
        l = main.next
        while True:
            current_point = l.value
            n = second.next
            while True:
                left_point = n.prev.value
                right_point = n.value
                if not right_or_left(left_point, right_point, current_point):
                    right = False
                n = n.next
                if n == second.next:
                    break
            l = l.next
            if l == main.next:
                break
        return right
            
        
    def check_main(self, current):
        check = True
        for i in range(len(self.lists_clip)):
            if i == 0:
                check = self.is_it_left(current, self.lists_clip[i])
            else:
                check = not self.is_it_right(current, self.lists_clip[i])
            if not check:
                return
        current_array = []
        current_array.append(current)
        x = current.next
        while x != current:
             current_array.append(x)
             x = x.next
        self.final.append(current_array)
            
        
    def check_clip(self, current):
        check = True
        for i in range(len(self.lists_main)):
            if i == 0:
                check = self.is_it_left(current, self.lists_main[i])
            else:
                check = not self.is_it_right(current, self.lists_main[i])
            if not check:
                return
        current_array = []
        current_array.append(current)
        x = current.next
        while x != current:
             current_array.append(x)
             x = x.next
        self.final.append(current_array)

    def draw_final(self):
        for i in range(len(self.final)):
            glBegin(GL_LINE_STRIP)
            glColor3f(1.0, 1.0, 1.0)
            for j in range(len(self.final[i])):
                glVertex2f(*self.final[i][j].value.print())
            glVertex2f(*self.final[i][0].value.print())
            glEnd()

    def start(self):
        self.create()
        for i in range(len(self.lists_main)):
            if self.lists_main[i].changed:
                self.find_enters(i)

        for i in range(len(self.enters)):
            print(len(self.lists_main))
            self.find_exit(self.enters[i])

        for i in range(len(self.lists_main)):
            if not self.lists_main[i].changed:
                self.check_main(self.lists_main[i])

        for i in range(len(self.lists_clip)):
            if not self.lists_clip[i].changed:
                self.check_clip(self.lists_clip[i])
        
        self.draw_final()
    

class Lab5(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = []
        self.polygons = []
        

    def add_point(self, x, y):
        self.points.append(Point(x, y))

    def reset(self):
        global weilor_done, w
        weilor_done = False
        self.points = []
        self.polygons = []
        w = Weilor(None, None)

    def resize(self, width, height):
        self.reset()
        self.width = width
        self.height = height

    def add_polygon(self):
        current_polygon = Polygon()
        current_polygon.add_outside_full(self.points)
        self.polygons.append(current_polygon)
        self.points = []

    def add_polygon_hole(self):
        self.polygons[len(self.polygons) - 1].add_inside_full(self.points)
        self.points = []

    def draw1(self):
        for i in range(len(self.points) - 3):
            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 1.0)
            glVertex2f(self.points[i].x, self.points[i].y)
            print(right_or_left(self.points[i], self.points[i + 1], self.points[i + 2]))
            print(self.points[i].distance(self.points[i + 1]))
            glVertex2f(self.points[i + 1].x, self.points[i + 1].y)
            glVertex2f(self.points[i + 2].x, self.points[i + 2].y)
            glVertex2f(self.points[i + 3].x, self.points[i + 3].y)
            glEnd()
            line1 = Line(self.points[i], self.points[i + 1])
            line2 = Line(self.points[i + 2], self.points[i + 3])
            line1.intersection(line2)

    def draw(self):
        for i in range(len(self.polygons)):
            self.polygons[i].draw()
        
        
        

lab5 = Lab5(800, 600)
w = Weilor(None, None)
weilor_done = False

@window.event
def on_draw():
    window.clear()
    lab5.draw()
    if weilor_done:
        w.start()

@window.event
def on_key_press(symbol, modkey):
    if symbol == pyglet.window.key.O:
        lab5.add_polygon()
    if symbol == pyglet.window.key.I:
        lab5.add_polygon_hole()
    if symbol == pyglet.window.key.R:
        lab5.reset()
    if symbol == pyglet.window.key.SPACE:
        global weilor_done, w
        weilor_done = True
        w = Weilor(lab5.polygons[0], lab5.polygons[1])



@window.event
def on_mouse_press(x, y, button, modifiers):
    if button & mouse.LEFT:
        lab5.add_point(x,y)
        
        

@window.event
def on_resize(width, height):
    lab5.resize(width, height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)


pyglet.app.run()
