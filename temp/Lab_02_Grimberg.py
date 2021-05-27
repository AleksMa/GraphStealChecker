from abc import ABC

import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from math import *

width1 = 800
height1 = 800

ALPHA = 0
BETA = 0
GAMMA = 0

l = 1
O = 45
mat = [1, 0, 0, 0,
       0, 1, 0, 0,
       -l * cos(O), -l * sin(O), -1, 0,
       0, 0, 0, 1]





def defaultCube():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(-6, -6, -3)
    glScalef(0.8, 0.8, 0.8)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glBegin(GL_QUADS)
    # 1
    glColor3ub(232, 68, 1)
    glVertex3f(0, 0, 0)
    glColor3ub(189, 245, 68)
    glVertex3f(1, 0, 0)
    glColor3ub(245, 197, 68)
    glVertex3f(1, 1, 0)
    glColor3ub(245, 68, 92)
    glVertex3f(0, 1, 0)

    # 2
    glColor3ub(6, 245, 138)
    glVertex3f(0, 0, 0)
    glColor3ub(36, 234, 89)
    glVertex3f(1, 0, 0)
    glColor3ub(234, 36, 36)
    glVertex3f(1, 0, 1)
    glColor3ub(36, 49, 234)
    glVertex3f(0, 0, 1)

    # 3
    glColor3ub(59, 100, 250)
    glVertex3f(1, 1, 0)
    glColor3ub(255, 140, 0)
    glVertex3f(0, 1, 0)
    glColor3ub(78, 95, 150)
    glVertex3f(0, 1, 1)
    glColor3ub(153, 190, 250)
    glVertex3f(1, 1, 1)

    # 4
    glColor3ub(59, 100, 250)
    glVertex3f(1, 0, 0)
    glColor3ub(255, 0, 0)
    glVertex3f(1, 1, 0)
    glColor3ub(234, 201, 36)
    glVertex3f(1, 1, 1)
    glColor3ub(36, 234, 132)
    glVertex3f(1, 0, 1)

    # 5
    glColor3ub(255, 255, 0)
    glVertex3f(0, 0, 0)
    glColor3ub(255, 155, 0)
    glVertex3f(0, 1, 0)
    glColor3ub(155, 255, 0)
    glVertex3f(0, 1, 1)
    glColor3ub(255, 255, 150)
    glVertex3f(0, 0, 1)

    # 6
    glColor3ub(10, 175, 246)
    glVertex3f(1, 0, 1)
    glColor3ub(204, 9, 248)
    glVertex3f(0, 0, 1)
    glColor3ub(244, 248, 9)
    glVertex3f(0, 1, 1)
    glColor3ub(248, 255, 150)
    glVertex3f(1, 1, 1)

    glEnd()
    glPopMatrix()

def base_ort():
    glBegin(GL_LINES)
    glVertex3f(5, 0.0, 0.0)
    glColor3ub(255, 0, 0)
    glVertex3f(0, 0, 0)
    glColor3ub(255, 0, 0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3ub(0, 255, 0)
    glVertex3f(0, 0, 0)
    glColor3ub(0, 255, 0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 5.0)
    glColor3ub(0, 0, 255)
    glVertex3f(0, 0, 0)
    glColor3ub(0, 0, 255)
    glEnd()

class Cube:
    def __init__(self):
        self.alpha = ALPHA
        self.beta = BETA
        self.gamma = GAMMA
        self.xangle_projection = 0
        self.yangle_projection = 0
        self.displaymode = GL_FILL
        self.baseort = False
        self.scale = 2
        self.movex = 0
        self.movey = 0

    def draw_cube(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMultMatrixd((GLdouble * len(mat))(*mat))
        glOrtho(-20, 20 ,-20, 20, -20, 20)
        glScalef(1,1,1)
        #
        if self.baseort:
            base_ort()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glScalef(self.scale, self.scale, self.scale)
        glTranslatef(self.movex, self.movey, 0)
        glRotatef(self.alpha, 0, 1, 0)
        glRotatef(self.beta, 0, 0, 1)
        glRotatef(self.gamma, 1, 0, 0)


        glPolygonMode(GL_FRONT_AND_BACK, self.displaymode)
        glBegin(GL_QUADS)
        # 1
        glColor3ub(232, 68, 1)
        glVertex3f(0, 0, 0)
        glColor3ub(189, 245, 68)
        glVertex3f(1, 0, 0)
        glColor3ub(245, 197, 68)
        glVertex3f(1, 1, 0)
        glColor3ub(245, 68, 92)
        glVertex3f(0, 1, 0)

        # 2
        glColor3ub(6, 245, 138)
        glVertex3f(0, 0, 0)
        glColor3ub(36, 234, 89)
        glVertex3f(1, 0, 0)
        glColor3ub(234, 36, 36)
        glVertex3f(1, 0, 1)
        glColor3ub(36, 49, 234)
        glVertex3f(0, 0, 1)

        # 3
        glColor3ub(59, 100, 250)
        glVertex3f(1, 1, 0)
        glColor3ub(255, 140, 0)
        glVertex3f(0, 1, 0)
        glColor3ub(78, 95, 150)
        glVertex3f(0, 1, 1)
        glColor3ub(153, 190, 250)
        glVertex3f(1, 1, 1)

        # 4
        glColor3ub(59, 100, 250)
        glVertex3f(1, 0, 0)
        glColor3ub(255, 0, 0)
        glVertex3f(1, 1, 0)
        glColor3ub(234, 201, 36)
        glVertex3f(1, 1, 1)
        glColor3ub(36, 234, 132)
        glVertex3f(1, 0, 1)

        # 5
        glColor3ub(255, 255, 0)
        glVertex3f(0, 0, 0)
        glColor3ub(255, 155, 0)
        glVertex3f(0, 1, 0)
        glColor3ub(155, 255, 0)
        glVertex3f(0, 1, 1)
        glColor3ub(255, 255, 150)
        glVertex3f(0, 0, 1)

        # 6
        glColor3ub(10, 175, 246)
        glVertex3f(1, 0, 1)
        glColor3ub(204, 9, 248)
        glVertex3f(0, 0, 1)
        glColor3ub(244, 248, 9)
        glVertex3f(0, 1, 1)
        glColor3ub(248, 255, 150)
        glVertex3f(1, 1, 1)


        glEnd()
        glPopMatrix()


class RealWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(100, 100)
        self.set_maximum_size(1920, 1080)
        self.cube = Cube()
        glClearColor(0, 0, 0, 0)

    def on_draw(self):
        self.clear()
        self.cube.draw_cube()
        defaultCube()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.cube.yangle_projection -= dy
            self.cube.xangle_projection += dx
        elif buttons == mouse.RIGHT:
            self.cube.gamma -= dy
            self.cube.alpha += dx

    def on_key_press(self, symbol, modifiers):
        if symbol == 115:
            self.cube.displaymode = GL_FILL
        elif symbol == 119:
            self.cube.displaymode = GL_LINE
        elif symbol == 102:
            self.cube.baseort = not self.cube.baseort
        elif symbol == 65362:
            self.cube.movey += 1
        elif symbol == 65364:
            self.cube.movey -= 1
        elif symbol == 65361:
            self.cube.movex -= 1
        elif symbol == 65363:
            self.cube.movex += 1


if __name__ == "__main__":
    window = RealWindow(width1, height1, "lab2", resizable=True)
    pyglet.app.run()
