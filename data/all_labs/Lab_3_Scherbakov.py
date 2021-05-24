import pyglet
from pyglet.gl import *
from math import *
from random import random
from random import seed


class Ellipsoid:
    def __init__(self):
        global a, b
        a = max(a, 10)
        b = max(b, 10)
        self.vertices = dict()
        for i in range(a):
            line = dict()
            for j in range(b+1):
                x = 20*sin(pi*j/b)*cos(2*pi*i/a)
                y = 10*sin(pi*j/b)*sin(2*pi*i/a)
                z = 10*cos(pi*j/b)
                line[j] = (x, y, z)
            self.vertices[i] = line

    def draw(self):
        for i in range(a):
            seed(i)
            glColor3f(random(), random(), random())
            glBegin(GL_TRIANGLES)
            glVertex3f(*self.vertices[0][0])
            glVertex3f(*self.vertices[i][1])
            glVertex3f(*self.vertices[(i+1) % a][1])
            glEnd()
            glBegin(GL_QUADS)
            for j in range(1, b-1):
                glColor3f(random(), random(), random())
                glVertex3f(*self.vertices[i][j])
                glVertex3f(*self.vertices[(i+1) % a][j])
                glVertex3f(*self.vertices[(i+1) % a][j+1])
                glVertex3f(*self.vertices[i][j+1])
            glEnd()
            glBegin(GL_TRIANGLES)
            glVertex3f(*self.vertices[i][b-1])
            glVertex3f(*self.vertices[(i+1) % a][b-1])
            glVertex3f(*self.vertices[0][b])
            glEnd()


pos = [0, 0, -5]
rot_x = 0
rot_y = 0
rot_z = 0
pos_x = 0
pos_y = 0
pos_z = 0
lines = False
a = b = 10
ellipsoid = Ellipsoid()

config = Config(sample_buffers=1, samples=8)
tela = pyglet.window.Window(height=600, width=600, config=config, resizable=True)
@tela.event
def on_draw():
    global pos_x, pos_y, pos_z, rot_x, rot_y, rot_z, lines

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    glRotatef(45, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(10, 0, -10)
    glPushMatrix()
    glRotatef(40, 1, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if lines else GL_FILL)

    tela.clear()

    gl.glViewport(int(tela.width/2)-300, int(tela.height/2)-300, 100, 100)

    glBegin(GL_QUADS)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()

    glPopMatrix()
    glTranslatef(pos_x+10, pos_y, pos_z-10)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)

    gl.glViewport(int(tela.width/2)-250, int(tela.height/2)-250, 500, 500)

    ellipsoid.draw()

    glFlush()

@tela.event
def on_key_press(s,m):

    global pos_x, pos_y, pos_z, rot_x, rot_y, rot_z, lines, a, b

    if s == pyglet.window.key.A:
        rot_y += 10
    if s == pyglet.window.key.D:
        rot_y -= 10
    if s == pyglet.window.key.Q:
        rot_z += 10
    if s == pyglet.window.key.E:
        rot_z -= 10
    if s == pyglet.window.key.Z:
        rot_x += 10
    if s == pyglet.window.key.C:
        rot_x -= 10
    if s == pyglet.window.key.I:
        pos_z += 1
    if s == pyglet.window.key.K:
        pos_z -= 1
    if s == pyglet.window.key.UP:
        pos_y += 1
    if s == pyglet.window.key.DOWN:
        pos_y -= 1
    if s == pyglet.window.key.LEFT:
        pos_x -= 1
    if s == pyglet.window.key.RIGHT:
        pos_x += 1
    if s == pyglet.window.key.SPACE:
        lines = not lines
    if s == pyglet.window.key.R:
        a += 1
        ellipsoid.__init__()
    if s == pyglet.window.key.F:
        a -= 1
        ellipsoid.__init__()
    if s == pyglet.window.key.T:
        b += 1
        ellipsoid.__init__()
    if s == pyglet.window.key.G:
        b -= 1
        ellipsoid.__init__() 


pyglet.app.run()
