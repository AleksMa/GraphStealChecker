# горизонтальная изометрия

from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet

def main():
    window = pyglet.window.Window(500, 500, resizable=True)
    window.set_minimum_size(100, 100)
    window.set_maximum_size(700, 700)

    glClearColor(0, 0, 0, 1)
    colors = [[0.6, 0.14, 0.14], [0.22, 0.2, 0.27], [0.4, 0.2, 0.27], [0.2, 0.14, 0.27], [0.2, 0.27, 0.27],
              [0.1, 0.2, 0.11]]
    vertex = [[[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [0.1, -0.1, -0.1], [0.1, -0.1, 0.1]],
              [[-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, -0.1, -0.1]],
              [[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [-0.1, 0.1, 0.1]],
              [[0.1, -0.1, 0.1], [0.1, -0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1]],
              [[-0.1, 0.1, 0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1]],
              [[-0.1, -0.1, 0.1], [-0.1, 0.1, 0.1], [0.1, 0.1, 0.1], [0.1, -0.1, 0.1]]]
    pos = [0, 0, 0]
    fi = [0, 0, 0]
    k = 1.8
    cubeModeSec = GL_FILL
    pyglet.app.run()


def drawCube(mode, first, second, third, fourth, color):
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glEnd()


def coordsCube(painted):
    drawCube(painted, vertex[0][0], vertex[0][1], vertex[0][2], vertex[0][3], colors[0])  # Bottom
    drawCube(painted, vertex[1][0], vertex[1][1], vertex[1][2], vertex[1][3], colors[1])  # Back
    drawCube(painted, vertex[2][0], vertex[2][1], vertex[2][2], vertex[2][3], colors[2])  # Left
    drawCube(painted, vertex[3][0], vertex[3][1], vertex[3][2], vertex[3][3], colors[3])  # Right
    drawCube(painted, vertex[4][0], vertex[4][1], vertex[4][2], vertex[4][3], colors[4])  # Top
    drawCube(painted, vertex[5][0], vertex[5][1], vertex[5][2], vertex[5][3], colors[5])  # Front


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
                       angle, angle, -1, 0,
                       0, 0, 0, 1)
    glLoadIdentity()
    glScaled(1, 1, 1)
    glOrtho(-1, 1, -1, 1, -1, 100)
    glLoadMatrixf(m)
    staticCube()
    nonStaticCube()


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

if __name__ == "__main__":
    main()
