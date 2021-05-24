# горизонтальная изометрия

from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet

window = pyglet.window.Window(500, 500, resizable=True)
window.set_minimum_size(100, 100)
window.set_maximum_size(700, 700)
glClearColor(0, 0, 0, 1)
colors = [[0.17, 0.01, 0.04], [0.2, 0, 0.22], [0.01, 0.06, 0.17], [0, 0.22, 0.2], [0.1, 0.15, 0.7], [0, 0.33, 0.31]]
vertex = [[[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [0.1, -0.1, -0.1], [0.1, -0.1, 0.1]],
          [[-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, -0.1, -0.1]],
          [[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [-0.1, 0.1, 0.1]],
          [[0.1, -0.1, 0.1], [0.1, -0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1]],
          [[-0.1, 0.1, 0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1]],
          [[-0.1, -0.1, 0.1], [-0.1, 0.1, 0.1], [0.1, 0.1, 0.1], [0.1, -0.1, 0.1]]]

coordsArray = []
coordsTurn = []
pos = [0, 0, 0]
fi = [0, 0, 0]
k = 1.8
n = 8

cubeModeSec = GL_FILL


def drawCube(mode, first, second, third, fourth, color):
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glEnd()


def drawPolygon(mode):
    global n
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glBegin(GL_TRIANGLES)
    if mode == GL_LINE:
        glColor3f(*colors[5])
    else:
        glColor3f(*colors[0])
    for i in range(n):
        glVertex3f(*coordsArray[i])
        glVertex3f(*coordsArray[i - 1])
        glVertex3f(0, 0.1, 0)
    if mode == GL_LINE:
        glColor3f(*colors[5])
    else:
        glColor3f(*colors[2])
    for j in range(n):
        glVertex3f(*coordsTurn[j])
        glVertex3f(*coordsTurn[j - 1])
        glVertex3f(0, -0.17, 0)
    if mode == GL_LINE:
        glColor3f(*colors[5])
    else:
        glColor3f(*colors[2])
    for k in range(n):
        glVertex3f(*coordsArray[k])
        glVertex3f(*coordsTurn[k - 1])
        glVertex3f(*coordsArray[k - 1])
    if mode == GL_LINE:
        glColor3f(*colors[5])
    else:
        glColor3f(*colors[0])
    for k in range(n):
        glVertex3f(*coordsTurn[k])
        glVertex3f(*coordsArray[k])
        glVertex3f(*coordsTurn[k - 1])
    glEnd()


def coords():
    global coordsArray, n
    for i in range(n):
        x = cos(2*pi*i/n)
        z = sin(2*pi*i/n)
        coordsArray.append([x*0.1, 0.1, z*0.1])
    return coordsArray

def tNout():
    global coordsTurn, n
    turnAngle = pi / n
    for i in range(n):
        newX = coordsArray[i][0]*cos(turnAngle) - coordsArray[i][2]*sin(turnAngle)
        newZ = coordsArray[i][0]*sin(turnAngle) + coordsArray[i][2]*cos(turnAngle)
        coordsTurn.append([newX, -0.17, newZ])
    return coordsTurn

def coordsStaticCube(painted):
    drawCube(painted, vertex[0][0], vertex[0][1], vertex[0][2], vertex[0][3], colors[5])  # Bottom
    drawCube(painted, vertex[1][0], vertex[1][1], vertex[1][2], vertex[1][3], colors[5])  # Back
    drawCube(painted, vertex[2][0], vertex[2][1], vertex[2][2], vertex[2][3], colors[5])  # Left
    drawCube(painted, vertex[3][0], vertex[3][1], vertex[3][2], vertex[3][3], colors[5])  # Right
    drawCube(painted, vertex[4][0], vertex[4][1], vertex[4][2], vertex[4][3], colors[5])  # Top
    drawCube(painted, vertex[5][0], vertex[5][1], vertex[5][2], vertex[5][3], colors[5])  # Front

def coordsPoly(painted):
    coords()
    tNout()
    drawPolygon(painted)




def staticCube():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslated(-0.5, -0.5, -0.3)
    glScaled(0.5, 0.5, 0.5)
    coordsStaticCube(GL_LINE)
    glPopMatrix()


def antiprism():
    global coordsTurn, coordsArray
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslated(0 + pos[0], 0 + pos[1], -0.3 + pos[2])
    glRotated(fi[0], 1, 0, 0)
    glRotated(fi[1], 0, 1, 0)
    glRotated(fi[2], 0, 0, 1)
    glScaled(k, k, k)
    coordsPoly(cubeModeSec)
    coordsArray = []
    coordsTurn = []
    glPopMatrix()



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
    angle = -cos(pi / 4.0)
    m = (GLfloat * 16)(1, 0, 0, 0,
                       0, 1, 0, 0,
                       angle, angle, -m1, 0,
                       0, 0, 0, 1)
    glLoadIdentity()
    glScaled(1, 1, 1)
    glOrtho(-1, 1, -1, 1, -1, 100)
    glLoadMatrixf(m)
    staticCube()
    antiprism()


@window.event
def on_resize(width, height):
    glViewport(0, 0, height, width)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global cubeModeSec
    if button == mouse.LEFT:
        if cubeModeSec == GL_LINE:
            cubeModeSec = GL_FILL
        else:
            cubeModeSec = GL_LINE


@window.event
def on_key_press(symbol, modifiers):
    global k
    global n
    if symbol == key.W:
        pos[1] += 0.1
    elif symbol == key.S:
        pos[1] -= 0.1
    elif symbol == key.Q:
        pos[2] -= 0.1
    elif symbol == key.E:
        pos[2] += 0.1
    elif symbol == key.A:
        pos[0] -= 0.1
    elif symbol == key.D:
        pos[0] += 0.1
    elif symbol == key.R:
        fi[0] += 5
    elif symbol == key.T:
        fi[0] -= 5
    elif symbol == key.F:
        fi[1] += 5
    elif symbol == key.G:
        fi[1] -= 5
    elif symbol == key.X:
        fi[2] += 5
    elif symbol == key.C:
        fi[2] -= 5
    elif symbol == key.UP:
        k += 0.3
    elif symbol == key.DOWN:
        k -= 0.3
    elif symbol == key.N:
        n += 1
    elif symbol == key.M and n > 3:
        n -= 1



pyglet.app.run()
