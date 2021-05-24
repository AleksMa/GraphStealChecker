import glfw
from pyglet.gl import *
import pyglet
from pyglet.window import key,mouse
import pyglet.window.key as key
import math

class frame_buffer(object):

    def __init__(self, width, height):
        self.nodes = []
        self.width = width
        self.height = height
        self.pixel = [0] * self.width * self.height * 3
        self.fill = False

    def delete(self):
        self.nodes.clear()
        self.pixel = [0] * self.width * self.height * 3
        self.fill = False

    def resize(self, a, b):
        self.width, self.height = a, b
        self.pixel = [0] * self.width * self.height * 3
        #self.fill = True
    def draw(self):
            if len(self.nodes) > 2:
                glColor3f(1, 1, 1)
                if self.fill:
                    self.filler()
                    #self.fill = False
                    self.filter(3)
                glDrawPixels(self.width, self.height, GL_RGB, GL_FLOAT, (GLfloat * len(self.pixel)) (*self.pixel))
                if not self.fill:
                    for i in range(len(self.nodes)):
                        glBegin(GL_LINES)
                        glVertex2f(*self.nodes[i])
                        glVertex2f(*self.nodes[(i + 1) % len(self.nodes)])
                        glEnd()

    def invert(self, x, y):
        for i in range(3):
            self.pixel[(y * self.width + x) * 3 + i] = (self.pixel[(y * self.width + x) * 3 + i] + 1) % 2
            

    def filler(self):

        def edges(x0, y0, x1, y1, border):
            if y0 == y1 or x0 == x1:
                return
            if y0 > y1:
                x0, x1, y0, y1 = x1, x0, y1, y0
            for y in range(y0, y1):
                a = math.floor(((y - y0) / (y1 - y0)) * (x1 - x0) + x0)
                b = border
                if b < a:
                    a += 1
                a, b = min(a, b), max(a, b)
                for x3 in range(a, b):
                    self.invert(x3, y)
        data = [self.nodes[i][0] for i in range(len(self.nodes))]
        border = (max(data) + min(data)) // 2
        for i in range(len(self.nodes)):
            x0, y0 = self.nodes[i]
            x1, y1 = self.nodes[(i + 1) % len(self.nodes)]
            edges(x0, y0, x1, y1, border)

    def add_point(self, x, y):
        self.nodes.append((x, y))
    def filter(self, n):
        def mask(x, y):
            data = [0, 0, 0]
            for i in range(0, 3):
                for j in range(0, n):
                    for u in range(0, n):
                        data[i] += self.pixel[((y + u) * self.width + x + j) * 3 + i]

                data[i] /= n * n
            for i in range(0, 3):
                for j in range(0, n):
                    for u in range(0, n):

                        self.pixel[((y + u) * self.width + x + j) * 3 + i] = data[i]
        for i in range(0, self.width - 2 * n, n):
            for j in range(0, self.height - 2 * n, n):
                mask(i, j)


window = pyglet.window.Window(800, 600, resizable=True)
pyglet.gl.glClearColor(0,0,0,0)
frame_buffer = frame_buffer(800,600)

@window.event
def on_draw():
    window.clear()
    frame_buffer.draw()

@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.SPACE:
        frame_buffer.delete()
    elif symbol == key.U:
        frame_buffer.fill = True
    print(0)


@window.event
def on_mouse_press(x, y, button, modifier):
    if button & mouse.LEFT:
        frame_buffer.add_point(x, y)


@window.event
def on_resize(width,height):
    if height < 0:
        height = 1
    frame_buffer.resize(width,height)
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,width,0,height)
    glMatrixMode(GL_MODELVIEW)

#if __name__ == "__main__":
pyglet.app.run()