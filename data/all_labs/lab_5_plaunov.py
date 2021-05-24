import glfw
from pyglet.gl import *
import pyglet
from pyglet.window import key, mouse
import pyglet.window.key as key
import math


def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]
def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]
def mul(a, t):
    return [a[0] * t, a[1] * t]
class frame_buffer(object):

    def __init__(self, width, height):
        self.nodes = []
        self.data = []
        self.width = width
        self.height = height
        self.normal = []
        self.fill = False
        self.result = []
        self.input = [[[0, -1], [0, 0]]]
        self.fiu = False

    def delete(self):
        self.nodes = []
        self.data = []
        self.normal = []
        self.fill = False
        self.result = []
        self.input = [[[0, -1], [0, 0]]]
        self.fiu = False

    def resize(self, a, b):
        self.width, self.height = a, b
        self.pixel = [0] * self.width * self.height * 3

    def draw(self):
        if len(self.nodes) > 1:
            glColor3f(0, 1, 0)
            for i in range(len(self.nodes)):
                glBegin(GL_LINES)
                glVertex2f(*self.nodes[i])
                glVertex2f(*self.nodes[(i + 1) % len(self.nodes)])
                glEnd()
            glColor3f(1, 1, 1)
            for i in range(len(self.data)):
                glBegin(GL_LINES)
                glVertex2f(*self.data[i])
                glVertex2f(*self.data[(i + 1) % len(self.data)])
                glEnd()
        if self.fill and self.result == []:
            self.cyrus_beck()
        if self.fill:
            for i in range(len(self.result)):
                glBegin(GL_LINES)
                glVertex2f(*self.result[i][0])
                glVertex2f(*self.result[i][1])
                glEnd()
        else:
            for i in range(len(self.input)):
                if (len(self.input[i]) < 2):
                    continue
                glBegin(GL_LINES)
                glVertex2f(*self.input[i][0])
                glVertex2f(*self.input[i][1])
                glEnd()

    def add_point(self, x, y):
        self.nodes.append((x, y))
        print(x, y)

    def add_line(self, x, y):
        if len(self.input[-1]) < 2:
            self.input[-1].append([x, y])
        else:
            self.input.append([[x, y]])
        self.result = []
        print(x, y)

    def cyrus_beck(self):
        def normal(a, b):
            return [a[1] - b[1], b[0] - a[0]]
        def f(a, b, t1, t2):
            print(0)
            return [add(a, mul(b, t1)), add(a, mul(b, t2))]
        def f12(a, b, t1, t2):
            print(0)
            return [[a, add(a, mul(b, t1))], [add(a, mul(b, t2)), add(a, b)]]
        n = len(self.nodes)
        self.normal = [normal(self.nodes[i], self.nodes[(i + 1) % n]) for i in range(n)]
        for [a, b] in self.input:
            print(a, b)
            p1p0 = sub(b, a)
            dist = [sub(self.nodes[i], a) for i in range(n)]
            t = [0] * n
            tin = []
            tout = []
            for i in range(n):
                u1 = dot(self.normal[i], dist[i])
                u2 = dot(self.normal[i], p1p0)
                if u2 == 0:
                    continue
                t[i] = u1 / u2
                if u2 < 0:
                    tin.append(t[i])
                else:
                    tout.append(t[i])
            result = [max(tin + [0]), min(tout + [1])]
            if False:
                if result[0] > result[1]:
                    continue
                vec = f(a, p1p0, result[0], result[1])
                self.result.append(vec)
            else:
                if result[0] > result[1]:
                    self.result.append([a, b])
                else:
                    vec1, vec2 = f12(a, p1p0, result[0], result[1])
                    self.result.append(vec1)
                    self.result.append(vec2)
                #print(tin, tout, result, vec)
window = pyglet.window.Window(800, 600, resizable=True)
window.maximize()
pyglet.gl.glClearColor(0, 0, 0, 0)
frame_buffer = frame_buffer(800, 600)


@window.event
def on_draw():
    window.clear()
    frame_buffer.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        frame_buffer.delete()
    elif symbol == key.U:
        frame_buffer.fill ^= 1
        frame_buffer.fill = True if frame_buffer.fill == 1 else False
    elif symbol == key.Z:
        frame_buffer.fiu ^= 1
        frame_buffer.fiu = True if frame_buffer.fiu == 1 else False
    print(0)


@window.event
def on_mouse_press(x, y, button, modifier):
    if frame_buffer.result != [] and frame_buffer.fiu:
        return
    if button and mouse.LEFT and not frame_buffer.fiu:
        if frame_buffer.result == []:
            frame_buffer.add_point(x, y)
    elif button and mouse.LEFT:
        frame_buffer.add_line(x, y)


@window.event
def on_resize(width, height):
    if height < 0:
        height = 1
    frame_buffer.resize(width, height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)


# if __name__ == "__main__":
pyglet.app.run()