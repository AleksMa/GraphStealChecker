import pyglet as pgl
from pyglet.gl import *
from pyglet.window import key, mouse
import math as m

def main():
    S = 600
    c = 0.5
    sides = [[c,c,c], [-c,c,c], [-c,-c,c], [c,-c,c],
             [c,-c,-c], [-c,-c,-c], [-c,c,-c], [c,c,-c]]

    win = pgl.window.Window(S, S, resizable=True)
    win.set_minimum_size(200, 200)
    pgl.app.run()


def drawCube(c, s1, s2, s3, s4):
    glBegin(GL_POLYGON)
    glColor3f(*c)
    glVertex3f(*s1)
    glVertex3f(*s2)
    glVertex3f(*s3)
    glVertex3f(*s4)
    glEnd()

def drawSkeletonCube(s1, s2, s3, s4):
    glBegin(GL_LINE_LOOP)
    glColor3f(*colors[6])
    glVertex3f(*s1)
    glVertex3f(*s2)
    glVertex3f(*s3)
    glVertex3f(*s4)
    glEnd()

@win.event
def on_draw():
    win.clear()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if win.height > win.width:
        glViewport(0, 0, win.height, win.height)
    else:
        glViewport(0, 0, win.width, win.width)

    glMatrixMode(GL_PROJECTION)

    gluPerspective(60, anti_resize, 1, 1000)

    coef = 0.5
    front_dimetry = (GLfloat*16)(1,0,0,0,
                     0,1,0,0,
                     -coef*m.cos(m.pi/4),-coef*m.sin(m.pi/4),1,0,
                     0,0,0,1)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -100, 100)
    glMultMatrixf(front_dimetry)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-1, -1, -0.5)
    glScalef(0.2, 0.2, 0.2)
    useful_function()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(coords[0] - 2, coords[1] - 2, coords[2] - 0.3)
    glScalef(0.2, 0.2, 0.2)
    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)
    glRotatef(rotation[2], 0, 0, 1)
    if skeleton:
        draw_skeleton()
    else:
        useful_function()

@win.event
def on_resize(width, height):
    global anti_resize
    glViewport(0, 0, width, height)
    anti_resize = width/height

@win.event
def on_key_press(symbol, modifiers):
    global skeleton
    c1 = 0.1
    c2 = 11
    if symbol == key.UP:
        coords[1] += c1
    elif symbol == key.DOWN:
        coords[1] += -c1
    elif symbol == key.LEFT:
        coords[0] += -c1
    elif symbol == key.RIGHT:
        coords[0] += c1
    elif symbol == key.Q:
        coords[2] += c1
    elif symbol == key.A:
        coords[2] += -c1
    elif symbol == key.W:
        rotation[0] += -c2
    elif symbol == key.S:
        rotation[0] += c2
    elif symbol == key.E:
        rotation[1] += -c2
    elif symbol == key.R:
        rotation[1] += c2
    elif symbol == key.D:
        rotation[2] += -c2
    elif symbol == key.F:
        rotation[2] += c2
    elif symbol == key.SPACE:
        skeleton = not skeleton

if __name__ == "__main__":
    main()
