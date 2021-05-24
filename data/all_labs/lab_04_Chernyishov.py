from pyglet import *
from pyglet.gl import *
from pyglet.window import *
import numpy

window = pyglet.window.Window(800, 600, resizable=True)
pyglet.gl.glClearColor(0.0, 0.0, 0.0, 0)


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.print()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def print(self):
        return [self.x, self.y]

class Lab4(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = []
        self.pixels = numpy.empty(3 * (self.width + 1) * (self.height + 1), dtype = GLfloat)
        self.pixels.fill(0.0)
        self.changed = False
        self.fill = False
        self.add = False
        self.line = True
        self.start = False
        self.antialiasing = False
        self.start_point = Point(400, 300)

    def add_point(self, x, y):
        self.points.append(Point(x, y))
        self.changed = True

    def reset(self):
        self.points = []
        self.pixels.fill(0.0)

    def draw_lines(self):
        if len(self.points) < 1:
            return
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for i in range(len(self.points) - 1):
            glVertex2f(self.points[i].x, self.points[i].y)
            glVertex2f(self.points[i + 1].x, self.points[i + 1].y)
        glVertex2f(self.points[len(self.points) - 1].x, self.points[len(self.points) - 1].y)
        glVertex2f(self.points[0].x, self.points[0].y)
        glEnd()

    def set_pixel(self, x, y, brightness):
        place = y * self.width + x
        for i in range(3):
            self.pixels[3 * place + i] = brightness

    def check_pixel(self, x, y):
        return self.pixels[3 * (y * self.width + x)]

    def plot_line_low(self, x0, y0, x1, y1, brigthness):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        e = 2 * dy - dx
        
        y = y0
        for x in range(x0, x1 + 1):
            self.set_pixel(x, y, brigthness)
            if e > 0:
                y += yi
                self.set_pixel(x, y, brigthness)
                e -= 2 * dx
            e += 2 * dy

    def plot_line_high(self, x0, y0, x1, y1, brigthness):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        e = 2 * dx - dy
        
        x = x0
        for y in range(y0, y1 + 1):
            self.set_pixel(x, y, brigthness)
            if e > 0:
                x += xi
                self.set_pixel(x, y, brigthness)
                e -= 2 * dy
            e += 2 * dx

    def plot_line(self, x0, y0, x1, y1, brigthness):
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                self.plot_line_low(x1, y1, x0, y0, brigthness)
            else:
                self.plot_line_low(x0, y0, x1, y1, brigthness)
        else:
            if y0 > y1:
                self.plot_line_high(x1, y1, x0, y0, brigthness)
            else:
                self.plot_line_high(x0, y0, x1, y1, brigthness)

    def draw_bresenham(self):
        self.pixels.fill(0.0)
        for i in range(len(self.points) - 1):
                self.plot_line(self.points[i].x, self.points[i].y, self.points[i + 1].x, self.points[i + 1].y, 1.0)
        self.plot_line(self.points[len(self.points) - 1].x, self.points[len(self.points) - 1].y,
                       self.points[0].x, self.points[0].y, 1.0)

            
        

    def fill_flood(self):
        stack = []
        stack.append(self.start_point)
        while len(stack) != 0:
            point = stack.pop()
            #print(point.x, point.y)
            
            y = point.y
            
            current_x = point.x
            while current_x >= 0 and self.pixels[3 * (y * self.width + current_x)] != 1.0:
                current_x -= 1
            current_x += 1

            spanAbove, spanBelow = False, False
            if y < self.height - 1 and self.pixels[3 * ((y + 1) * self.width + current_x - 1)] == 0.0:
                stack.append(Point(current_x - 1, y + 1))
                spanBelow = True
            if y > 0 and self.pixels[3 * ((y - 1) * self.width + current_x - 1)] == 0.0:
                stack.append(Point(current_x - 1, y - 1))
                spanAbove = True

            while current_x < self.width and self.pixels[3 * (y * self.width + current_x)] == 0.0:
                for i in range(3):
                    self.pixels[3 * (y * self.width + current_x) + i] = 1.0

                if not spanAbove and y > 0 and self.pixels[3 * ((y - 1) * self.width + current_x)] == 0.0:
                    stack.append(Point(current_x, y - 1))
                    spanAbove = True
                elif spanAbove and y > 0 and self.pixels[3 * ((y - 1) * self.width + current_x)] != 0.0:
                    spanAbove = False

                if not spanBelow and y < self.height - 1 and self.pixels[3 * ((y + 1) * self.width + current_x)] == 0.0:
                    stack.append(Point(current_x, y + 1))
                    spanBelow = True
                elif spanBelow and y < self.height - 1 and self.pixels[3 * ((y + 1) * self.width + current_x)] != 0.0:
                    spanBelow = False
                    
                current_x += 1

            if y < self.height - 1 and current_x < self.width and self.pixels[3 * ((y + 1) * self.width + current_x)] == 0.0:
                stack.append(Point(current_x, y + 1))
            if y > 0 and current_x < self.width - 1 and self.pixels[3 * ((y - 1) * self.width + current_x)] == 0.0:
                stack.append(Point(current_x, y - 1))

    def draw_antialiasing_number(self, number):
        print(number)
        if number == 0:
            return Point(1, 1)
        elif number == 1:
            return Point(2, 1)
        elif number == 2:
            return Point(2, 2)
        elif number == 3:
            return Point(1, 2)
        elif number == 4:
            return Point(0, 2)
        elif number == 5:
            return Point(0, 1)
        elif number == 6:
            return Point(0, 0)
        elif number == 7:
            return Point(1, 0)
        elif number == 8:
            return Point(2, 0)
            
    def draw_antialiasing(self):
        for i in range(9):
            glDrawPixels(self.width, self.height, GL_RGB,GL_FLOAT,
                                (GLfloat * len(self.pixels))(*self.pixels))
            point = self.draw_antialiasing_number(i)
            glRasterPos2i(point.x, point.y)
            if i == 0:
                glAccum(GL_LOAD, 1.0 / 9.0)
            else:
                glAccum(GL_ACCUM, 1.0 / 9.0)
        glAccum(GL_RETURN, 1.0)
            

                
        

    def draw(self):
        if self.line:
            self.draw_lines()
        else:
            if (len(self.points) > 2):
                if self.antialiasing:
                    self.draw_bresenham()
                    if self.fill:
                        self.fill_flood()
                    self.draw_antialiasing()
                else:
                    self.draw_bresenham()
                    if self.fill:
                        self.fill_flood()
                    glRasterPos2i(1, 1)
                    glDrawPixels(self.width, self.height, GL_RGB,GL_FLOAT,
                                (GLfloat * len(self.pixels))(*self.pixels))

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.pixels = numpy.empty(3 * self.width * self.height, dtype = GLfloat)
        
        
        

lab4 = Lab4(800, 600)

@window.event
def on_draw():
    window.clear()
    lab4.draw()

@window.event
def on_key_press(symbol, modkey):
    if symbol == pyglet.window.key.A:
        lab4.add = not lab4.add
    if symbol == pyglet.window.key.F:
        lab4.fill = not lab4.fill
    if symbol == pyglet.window.key.R:
        lab4.reset()
    if symbol == pyglet.window.key.L:
        lab4.line = not lab4.line
    if symbol == pyglet.window.key.S:
        lab4.start = not lab4.start
    if symbol == pyglet.window.key.Q:
        lab4.antialiasing = not lab4.antialiasing
    if symbol == pyglet.window.key.O:
        lab4.add_point(200, 200)
        lab4.add_point(400, 200)
        lab4.add_point(400, 400)
        lab4.add_point(200, 400)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button & mouse.LEFT & lab4.add:
        lab4.add_point(x, y)
    if button & mouse.LEFT & lab4.start:
        print(x, y)
        lab4.start_point = Point(x, y)
        

@window.event
def on_resize(width, height):
    lab4.resize(width, height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)


pyglet.app.run()
