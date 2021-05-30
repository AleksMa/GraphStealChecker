import pyglet
from pyglet.gl import *

pos = [0, 0, -5]
rot_x = 0
rot_y = 0
rot_z = 0
pos_x = 0
pos_y = 0
pos_z = 0

config = Config(sample_buffers=1, samples=8)
tela = pyglet.window.Window(height=600, width=600, config=config, resizable=True)
@tela.event
def on_draw():
    global pos_x, pos_y, pos_z, rot_x, rot_y, rot_z

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    glRotatef(45, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(5, 0, -5)
    glPushMatrix()
    glRotatef(40, 1, 0, 0)
    glEnable(GL_DEPTH_TEST)

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
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)

    gl.glViewport(int(tela.width/2)-250, int(tela.height/2)-250, 500, 500)

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

    glFlush()

@tela.event
def on_key_press(s,m):

    global pos_x, pos_y, pos_z, rot_x, rot_y, rot_z

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


pyglet.app.run()
