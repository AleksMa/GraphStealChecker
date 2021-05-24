# диметрия
import ctypes

from OpenGL.raw.GLUT import glutInitDisplayMode
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet
import numpy as np
from random import random


window = pyglet.window.Window(500, 500, resizable=True)
window.set_minimum_size(100, 100)
glClearColor(1, 0.9, 0.95, 1)
paintedUp = True
colors = [[0.8, 0.7, 0.1], [0.25, 0.5, 0.25], [0.4, 0.3, 0.9], [0.1, 0.1, 0.55], [0.6, 0.3, 0.9], [0.75, 0.5, 0.65]]
pos = [0, 0, 0]
fi = [0, 0, 0]
k = 0.8
cubeMood = GL_FILL
ratio = 1
r1 = 0.5  # радиус образующей
r2 = 0.25  # радиус кругов
seq1 = 10  # кол-во кругов
seq2 = 8  # точность кругов

def cubeFace(mode, first, second, third, fourth, color):
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glEnd()

def TorCor2():
    masPoints = []
    for i in range(seq1):
        an1 = 2 * pi * (i / seq1)
        linePoints = []
        for j in range(seq2):
            an2 = 2 * pi * (j / seq2)
            point = [r1 * sin(an1) + r2 * sin(an2) * sin(an1), r1 * cos(an1) + r2 * sin(an2) * cos(an1), r2 * cos(an2)]
            linePoints.append(point)
        masPoints.append(linePoints)
    return masPoints


masCor = TorCor2()

def drawTor2(mood):
    masPoints = masCor
    mas = masPoints
    m = len(masPoints)
    n = len(masPoints[0])
    for i in range(m):
        glPolygonMode(GL_FRONT_AND_BACK, mood)
        for j in range(n):
            p1 = mas[i%m][j%n]
            p2 = mas[i%m][(j+1)%n]
            p4 = mas[(i+1)%m][j%n]
            p3 = mas[(i+1)%m][(j+1)%n]
            glColor3f(1 - random() % 0.5, 0, 1 - random() % 0.5)
            glBegin(GL_TRIANGLES)
            glVertex3f(*p1)
            glVertex3f(*p2)
            glVertex3f(*p3)
            glEnd()
            glColor3f(1 - random() % 0.5, 0, 1 - random() % 0.5)
            glBegin(GL_TRIANGLES)
            glVertex3f(*p3)
            glVertex3f(*p4)
            glVertex3f(*p1)
            glEnd()
            # из квадратов
            # glBegin(GL_QUADS)
            # glVertex3f(*p1)
            # glVertex3f(p2[0], p2[1], p2[2])
            # glVertex3f(p3[0], p3[1], p3[2])
            # glVertex3f(p4[0], p4[1], p4[2])
            # glEnd()




def unitCube(painted):
    q = 0.1
    lbf = [-q, -q, -q]
    rbf = [q, -q, -q]
    rtf = [q, q, -q]
    ltf = [-q, q, -q]

    lbn = [-q, -q, q]
    rbn = [q, -q, q]
    rtn = [q, q, q]
    ltn = [-q, q, q]

    # BOTTOM
    cubeFace(painted, lbn, lbf, rbf, rbn, colors[0])

    # BACK
    cubeFace(painted, lbf, ltf, rtf, rbf, colors[1])

    # LEFT
    cubeFace(painted, lbn, lbf, ltf, ltn, colors[2])

    # RIGHT
    cubeFace(painted, rbn, rbf, rtf, rtn, colors[3])

    # TOP
    cubeFace(painted, ltn, ltf, rtf, rtn, colors[4])

    # FRONT
    cubeFace(painted, lbn, ltn, rtn, rbn, colors[5])

@window.event
def on_draw():
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if window.height > window.width:
        glViewport(0, 0, window.height, window.height)
    else:
        glViewport(0, 0, window.width, window.width)

    glMatrixMode(GL_PROJECTION)
    f = 3 / 8
    a = asin(f / sqrt(2))
    b = asin(f / sqrt(2 - f * f))
    glLoadIdentity()
    glScaled(1, 1, 1)
    glOrtho(-1, 1, -1, 1, 0.0001, 100)
    glRotatef(a/pi*180, 1, 0, 0)
    glRotatef(b / pi * 180, 0, 1, 0)



    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()                             # small static cube
    glTranslated(-0.7, -0.7, -0.3)
    glScaled(0.7, 0.7, 0.7)
    unitCube(GL_LINE)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()                              # nonstatic cube
    glTranslated(0.3 + pos[0], -0.15 + pos[1], -1+pos[2])
    glRotated(fi[0], 1, 0, 0)
    glRotated(fi[1], 0, 1, 0)
    glRotated(fi[2], 0, 0, 1)
    glScaled(k, k, k)
    # drawTor2(cubeMood)
    unitCube(cubeMood)
    glPopMatrix()

@window.event
def on_resize(width, height):
    global ratio
    ratio = width/height
    if height > width:
        glViewport(0, 0, height, height)
    else:
        glViewport(0, 0, width, width)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global cubeMood
    if button == mouse.LEFT:
        if cubeMood == GL_LINE:
            cubeMood = GL_FILL
        else:
            cubeMood = GL_LINE


incPos = 0.1
incK = 0.3
alfa = 5
@window.event
def on_key_press(symbol, modifiers):
    global pos
    global k
    global r1, r2, seq1, seq2, masCor
    if symbol == key.U:
        pos[1] += incPos
    elif symbol == key.J:
        pos[1] -= incPos
    elif symbol == key.I:
        pos[2] -= incPos
    elif symbol == key.K:
        pos[2] += incPos
    elif symbol == key.N:
        pos[0] -= incPos
    elif symbol == key.M:
        pos[0] += incPos
    elif symbol == key.W:
        fi[0] += alfa
    elif symbol == key.Q:
        fi[0] -= alfa
    elif symbol == key.S:
        fi[1] += alfa
    elif symbol == key.A:
        fi[1] -= alfa
    elif symbol == key.X:
        fi[2] += alfa
    elif symbol == key.Z:
        fi[2] -= alfa
    elif symbol == key.UP:
        k += incK
    elif symbol == key.DOWN:
        k -= incK
    # для тора
    elif symbol == key.E:
        r1 += 0.05
        masCor = TorCor2()
    elif symbol == key.D:
        r1 -= 0.05
        masCor = TorCor2()
    elif symbol == key.R:
        r2 += 0.05
        masCor = TorCor2()
    elif symbol == key.F:
        r2 -= 0.05
        masCor = TorCor2()
    elif symbol == key.T:
        seq1 += 1
        masCor = TorCor2()
    elif symbol == key.G:
        seq1 -= 1
        masCor = TorCor2()
    elif symbol == key.Y:
        seq2 += 1
        masCor = TorCor2()
    elif symbol == key.H:
        seq2 -= 1
        masCor = TorCor2()

pyglet.app.run()