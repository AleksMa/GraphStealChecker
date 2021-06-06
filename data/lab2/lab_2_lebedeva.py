# диметрия
import ctypes

from OpenGL.raw.GLUT import glutInitDisplayMode
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet

def main():
    window = pyglet.window.Window(500, 500, resizable=True)
    window.set_minimum_size(100, 100)
    glClearColor(1, 0.9, 0.95, 1)
    paintedUp = True
    colors = [[0.8, 0.7, 0.1], [0.25, 0.5, 0.25], [0.4, 0.3, 0.9], [0.1, 0.1, 0.55], [0.6, 0.3, 0.9], [0.75, 0.5, 0.65]]
    pos = [0, 0, 0]
    fi = [0, 0, 0]
    k = 1
    cubeMood = GL_FILL
    ratio = 1

    masCor = TorCor()

    incPos = 0.1
    incK = 0.3
    alfa = 5

    pyglet.app.run()


def cubeFace(mode, first, second, third, fourth, color):
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glEnd()

def TorCor():
    theta = 0
    phi = 0
    R = 1
    r = 0.5
    feet = 1/100 * pi
    masPoints = []
    while phi < 2*pi:
        while theta < 2*pi:
            x = (R + r * cos(phi)) * cos(theta)
            y = (R + r * cos(phi)) * sin(theta)
            z = r * sin(phi)
            onePoint = [x, y, z]
            masPoints.append(onePoint)
            phi += feet
            theta += feet
    print(masPoints)
    return masPoints

masCor = TorCor()

def drawTor():
    masPoints = masCor
    glBegin(GL_LINES)
    for i in masPoints:
        glVertex3f(i[0], i[1], i[2])
    glEnd()

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

    # glLoadIdentity()
    # gluPerspective(45, window.width/window.height, 0.01, 500)
    f = 3 / 8
    a_phi = asin(f / sqrt(2))
    a_theta = asin(f / sqrt(2 - f * f))
    m = (GLfloat * 16) (
        cos(a_phi) / ratio, sin(a_phi) * sin(a_theta), -cos(a_theta) * sin(a_phi), 0,
        0, cos(a_theta), sin(a_theta), 0,
        sin(a_phi) / ratio, -sin(a_theta) * cos(a_phi), cos(a_theta) * cos(a_phi), 0,
        0, 0, 0, 1
    )

    # диметрия
    # f = 3 / 8
    # a = asin(f / sqrt(2))
    # b = asin(f / sqrt(2 - f * f))
    # m = (GLfloat * 16)(cos(b), 0, sin(b), 0,
    #         sin(a) * sin(b), cos(a), - cos(b) * sin(a), 0,
    #         cos(a) * sin(b), - sin(a), - cos(a) * cos(b), 0,
    #         0, 0, 0, 1)


    glLoadMatrixf(m)

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
    glTranslated(0 + pos[0], 0 + pos[1], -0.3+pos[2])
    glRotated(fi[0], 1, 0, 0)
    glRotated(fi[1], 0, 1, 0)
    glRotated(fi[2], 0, 0, 1)
    glScaled(k, k, k)
    # drawTor()
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


@window.event
def on_key_press(symbol, modifiers):
    global pos
    global k
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
    elif symbol == key.E:
        fi[0] -= alfa
    elif symbol == key.S:
        fi[1] += alfa
    elif symbol == key.D:
        fi[1] -= alfa
    elif symbol == key.X:
        fi[2] += alfa
    elif symbol == key.C:
        fi[2] -= alfa
    elif symbol == key.UP:
        k += incK
    elif symbol == key.DOWN:
        k -= incK


if __name__ == "__main__":
    main()
