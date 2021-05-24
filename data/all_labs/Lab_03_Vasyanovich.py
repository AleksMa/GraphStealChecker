from math import sqrt, pi, cos, sin
from random import random

from mathutils import Matrix
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from OpenGL.GLUT import *


window = pyglet.window.Window(1000, 1000, resizable = True)
window.set_minimum_size(144, 144)
gl.glClearColor(0, 0.5, 0.8, 1)
glutInit()

Width = 1000
Height = 1000
ratio = 1
pos = [0, 0, 0]
rot = [0, 0, 0]
isFramedMode = False
colors = [[0.1, 0.7, 0.1], [0.25, 0.5, 0.25], [0.4, 0.1, 0.4], [0.55, 0.5, 0.55], [0.7, 0.1, 0.7], [0.85, 0.5, 0.85]]
Horizontal = 15
Vertical = 15
Points = [[[0.0, 0.0, 0.0] for i in range(Vertical)] for j in range(Horizontal)]
heightOfParaboloid = 1
P = 0.25
Q = 0.5
Changed = False


dodeccolors = [[0.2, 0.2, 0.2], [0.25, 0.25, 0.25], [0.3, 0.3, 0.3],
               [0.35, 0.35, 0.35], [0.4, 0.4, 0.4], [0.45, 0.45, 0.45],
               [0.5, 0.5, 0.5], [0.55, 0.55, 0.55], [0.6, 0.6, 0.6],
               [0.65, 0.65, 0.65], [0.7, 0.7, 0.7], [0.75, 0.75, 0.75]]


alpha = sqrt(2.0 / (3.0 + sqrt(5.0)))
beta = 1.0 + sqrt(6.0 / (3.0 + sqrt(5.0)) - 2.0 + 2.0 * sqrt(2.0 / (3.0 + sqrt(5.0))))
dodec = [[i for i in range(3)] for j in range(20)]
dodec[0][0] = -alpha; dodec[0][1] = 0; dodec[0][2] = beta
dodec[1][0] = alpha; dodec[1][1] = 0; dodec[1][2] = beta
dodec[2][0] = -1; dodec[2][1] = -1; dodec[2][2] = -1
dodec[3][0] = -1; dodec[3][1] = -1; dodec[3][2] = 1
dodec[4][0] = -1; dodec[4][1] = 1; dodec[4][2] = -1
dodec[5][0] = -1; dodec[5][1] = 1; dodec[5][2] = 1
dodec[6][0] = 1; dodec[6][1] = -1; dodec[6][2] = -1
dodec[7][0] = 1; dodec[7][1] = -1; dodec[7][2] = 1
dodec[8][0] = 1; dodec[8][1] = 1; dodec[8][2] = -1
dodec[9][0] = 1; dodec[9][1] = 1; dodec[9][2] = 1
dodec[10][0] = beta; dodec[10][1] = alpha; dodec[10][2] = 0
dodec[11][0] = beta; dodec[11][1] = -alpha; dodec[11][2] = 0
dodec[12][0] = -beta; dodec[12][1] = alpha; dodec[12][2] = 0
dodec[13][0] = -beta; dodec[13][1] = -alpha; dodec[13][2] = 0
dodec[14][0] = -alpha; dodec[14][1] = 0; dodec[14][2] = -beta
dodec[15][0] = alpha; dodec[15][1] = 0; dodec[15][2] = -beta
dodec[16][0] = 0; dodec[16][1] = beta; dodec[16][2] = alpha
dodec[17][0] = 0; dodec[17][1] = beta; dodec[17][2] = -alpha
dodec[18][0] = 0; dodec[18][1] = -beta; dodec[18][2] = alpha
dodec[19][0] = 0; dodec[19][1] = -beta; dodec[19][2] = -alpha


def which(mode, first, second, third, fourth, color):
    if mode:
        glBegin(GL_LINE_LOOP)
        glColor3f(0, 0, 0)
    else:
        glBegin(GL_POLYGON)
        glColor3f(*color)

    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)

    glEnd()


def baseCube(framed):
    lbf = [-0.5, -0.5, -0.5]
    rbf = [0.5, -0.5, -0.5]
    rtf = [0.5, 0.5, -0.5]
    ltf = [-0.5, 0.5, -0.5]

    lbn = [-0.5, -0.5, 0.5]
    rbn = [0.5, -0.5, 0.5]
    rtn = [0.5, 0.5, 0.5]
    ltn = [-0.5, 0.5, 0.5]

    # BOTTOM
    which(framed, lbn, rbn, rbf, lbf, colors[0])

    # BACK
    which(framed, lbf, rbf, rtf, ltf, colors[1])

    # LEFT
    which(framed, ltf, ltn, lbn, lbf, colors[2])

    # RIGHT
    which(framed, rtn, rtf, rbf, rbn, colors[3])

    # TOP
    which(framed, ltn, ltf, rtf, rtn, colors[4])

    # FRONT
    which(framed, lbn, ltn, rtn, rbn, colors[5])


def pentagon(mode, first, second, third, fourth, fifth, color):
    if mode:
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 1, 1)
    else:
        glBegin(GL_POLYGON)
        glColor3f(*color)

    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glVertex3f(*fifth)

    glEnd()


def dodecahedron(framed):
    pentagon(framed, dodec[0], dodec[1], dodec[9], dodec[16], dodec[5], dodeccolors[0])
    pentagon(framed, dodec[1], dodec[0], dodec[3], dodec[18], dodec[7], dodeccolors[1])
    pentagon(framed, dodec[1], dodec[7], dodec[11], dodec[10], dodec[9], dodeccolors[2])
    pentagon(framed, dodec[11], dodec[7], dodec[18], dodec[19], dodec[6], dodeccolors[3])
    pentagon(framed, dodec[8], dodec[17], dodec[16], dodec[9], dodec[10], dodeccolors[4])
    pentagon(framed, dodec[2], dodec[14], dodec[15], dodec[6], dodec[19], dodeccolors[5])
    pentagon(framed, dodec[2], dodec[13], dodec[12], dodec[4], dodec[14], dodeccolors[6])
    pentagon(framed, dodec[2], dodec[19], dodec[18], dodec[3], dodec[13], dodeccolors[7])
    pentagon(framed, dodec[3], dodec[0], dodec[5], dodec[12], dodec[13], dodeccolors[8])
    pentagon(framed, dodec[6], dodec[15], dodec[8], dodec[10], dodec[11], dodeccolors[9])
    pentagon(framed, dodec[4], dodec[17], dodec[8], dodec[15], dodec[14], dodeccolors[10])
    pentagon(framed, dodec[4], dodec[12], dodec[5], dodec[16], dodec[17], dodeccolors[11])


def sectorOfParaboloid(framed, i, j, top):
    global heightOfParaboloid, Vertical, Horizontal, Points

    if framed:
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 1, 1)
    else:
        glBegin(GL_POLYGON)
        glColor3f(random(), random(), random())

    if not top:
        glVertex3f(*Points[i][j])

        if j + 1 == Vertical:
            glVertex3f(*Points[i][0])
        else:
            glVertex3f(*Points[i][j + 1])

        if i == 0:
            glVertex3f(0, 0, 0)
        else:
            if j + 1 == Vertical:
                glVertex3f(*Points[i - 1][0])
            else:
                glVertex3f(*Points[i - 1][j + 1])

            glVertex3f(*Points[i - 1][j])
    else:
        x = Points[i][j]
        x[1] = heightOfParaboloid
        glVertex3f(*x)

        if i == 0:
            glVertex3f(0, heightOfParaboloid, 0)
        else:
            # glVertex3f(*Points[i - 1][j])
            x = Points[i - 1][j]
            x[1] = heightOfParaboloid
            glVertex3f(*x)

            if j + 1 == Vertical:
                # glVertex3f(*Points[i - 1][0])
                x = Points[i - 1][0]
                x[1] = heightOfParaboloid
                glVertex3f(*x)
            else:
                # glVertex3f(*Points[i - 1][j + 1])
                x = Points[i - 1][j + 1]
                x[1] = heightOfParaboloid
                glVertex3f(*x)

        if j + 1 == Vertical:
            # glVertex3f(*Points[i][0])
            x = Points[i][0]
            x[1] = heightOfParaboloid
            glVertex3f(*x)
        else:
            # glVertex3f(*Points[i][j + 1])
            x = Points[i][j + 1]
            x[1] = heightOfParaboloid
            glVertex3f(*x)

    glEnd()


def EllepticalParaboloid(framed):
    #resetPoints()
    global Points, Horizontal, Vertical, heightOfParaboloid
    for i in range(Horizontal):
        for j in range(Vertical):
            sectorOfParaboloid(framed, i, j, False)

    # if framed:
    #     glBegin(GL_LINE_LOOP)
    # else:
    #     glBegin(GL_POLYGON)
    # glColor3f(1, 1, 1)
    # for i in range(vertical - 1, -1, -1):
    #     glVertex3f(*points[horizontal - 1][i])
    # glEnd()

    for i in range(Horizontal):
        for j in range(Vertical):
            sectorOfParaboloid(framed, i, j, True)


def resetPoints():
    global Points, P, Q, Vertical, Horizontal, heightOfParaboloid
    Points = [[[0.0, 0.0, 0.0] for i in range(Vertical)] for j in range(Horizontal)]
    stepy = float(heightOfParaboloid) / Horizontal
    anglexz = 2 * pi / Vertical
    curangle = 0
    h = 0.0

    for i in range(Horizontal):
        h += stepy
        for j in range(Vertical):
            Points[i][j][0] = sqrt(2 * Q * h) * cos(curangle)
            Points[i][j][1] = h
            Points[i][j][2] = sqrt(2 * P * h) * sin(curangle)
            curangle += anglexz


@window.event
def on_draw():
    global Width, Height
    global ratio
    global isFramedMode, Changed
    global Horizontal, Vertical, heightOfParaboloid, P, Q
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    cx = 3
    cy = 3
    cz = 3

    p = float(-1) / float(cx)
    q = float(-1) / float(cy)
    r = float(-1) / float(cz)

    matrixShift = Matrix([(1, 0, 0, 0),
                          (0, 1, 0, 0),
                          (0, 0, 1, 0),
                          (0.175, 0.175, 0.175, 1)])
    matrixRatio = Matrix([(1 / ratio, 0, 0, 0),
                          (0, 1, 0, 0),
                          (0, 0, 1, 0),
                          (0, 0, 0, 1)])
    matrixPerspective = Matrix([(1, 0, 0, p),
                                (0, 1, 0, q),
                                (0, 1, 0, r),
                                (0, 0, 0, 1)])
    matrixProjection = Matrix([(1, 0, 0, 0),
                               (0, 1, 0, 0),
                               (0, 0, 0, 0),
                               (0, 0, 0, 1)])
    # Matrix.transpose(matrixProjection)
    # Matrix.transpose(matrixPerspective)
    # Matrix.transpose(matrixRatio)
    # Matrix.transpose(matrixShift)
    #matrixFinal = matrixRatio @ matrixShift @ matrixPerspective @ matrixProjection
    matrixFinal = matrixProjection @ matrixPerspective @ matrixShift @ matrixRatio
    #matrixFinal = matrixPerspective @ matrixShift @ matrixRatio
    Matrix.transpose(matrixFinal)

    glMatrixMode(GL_PROJECTION)
    value = (GLfloat * 16)()
    for i in range(4):
        for j in range(4):
            value[i * 4 + j] = matrixFinal[i][j]

    glLoadMatrixf(value)
    # gluPerspective(40, ratio, 0.1, 100)
    # glOrtho(-ratio, ratio, -1, 1, float(-1), float(1))

    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CW)

    glLoadIdentity()

    glPushMatrix()
    # glTranslated(-0.25, -0.25, 0)
    glScaled(0.35, 0.35, 0.35)
    glRotatef(30, 1, 0, 0)
    glRotatef(-30, 0, 1, 0)
    glRotatef(0, 0, 0, 1)
    baseCube(False)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)

    #glDisable(GL_CULL_FACE)
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CW)

    glLoadIdentity()

    glPushMatrix()
    glTranslated(pos[0] + 0.775, pos[1] + 0.775, pos[2] + 0.775)
    glScaled(0.7, 0.7, 0.7)
    glRotatef(rot[0], 1, 0, 0)
    glRotatef(rot[1], 0, 1, 0)
    glRotatef(rot[2], 0, 0, 1)
    # baseCube(isFramedMode)
    # dodecahedron(isFramedMode)
    # if Changed:
    #     resetPoints()
    EllepticalParaboloid(isFramedMode)
    Changed = False

    glPopMatrix()


@window.event
def on_resize(width, height):
    global ratio
    glViewport(0, 0, width, height)
    ratio = width / height
    resetPoints()

    # global Width, Height
    # glMatrixMode(gl.GL_PROJECTION)
    # glLoadIdentity()
    # glOrtho(0, width, 0, height, -1, 1)
    # glMatrixMode(gl.GL_MODELVIEW)
    # Width = width
    # Height = Height


@window.event
def on_mouse_press(x, y, button, modifiers):
    resetPoints()

    global isFramedMode
    if button == mouse.LEFT:
        isFramedMode = not isFramedMode

@window.event
def on_key_press(symbol, modifiers):
    global pos, rot, Horizontal, Vertical, Changed

    #Changed = True

    if symbol == key.S and pos[1] >= -0.65:
        pos[1] -= 0.05
    elif symbol == key.W:
        pos[1] += 0.05
    elif symbol == key.D:
        pos[0] += 0.05
    elif symbol == key.A and pos[0] >= -0.65:
        pos[0] -= 0.05
    elif symbol == key.UP:
        pos[2] += 0.05
    elif symbol == key.DOWN and pos[2] >= -0.65:
        pos[2] -= 0.05

    elif symbol == key.Z:
        rot[0] -= 5
    elif symbol == key.X:
        rot[0] += 5
    elif symbol == key.C:
        rot[1] -= 5
    elif symbol == key.V:
        rot[1] += 5
    elif symbol == key.B:
        rot[2] -= 5
    elif symbol == key.N:
        rot[2] += 5

    elif symbol == key.O:
        Horizontal -= 1
        #resetPoints()
    elif symbol == key.P:
        Horizontal += 1
        #resetPoints()
    elif symbol == key.K:
        Vertical -= 1
        #resetPoints()
    elif symbol == key.L:
        Vertical += 1
        #resetPoints()

    resetPoints()

resetPoints()
pyglet.app.run()
