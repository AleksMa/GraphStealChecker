import math

import glfw
from OpenGL.GL import *
import time

xpos = ypos = zpos = 0
oxtr = oytr = oztr = 0
xscale = yscale = zscale = scale = 1
colormode = True


def moveevent(window, key, scancode, action, mods):
    global xpos, ypos, zpos
    global oztr, oytr, oxtr
    global scale, colormode, xscale, yscale, zscale
    if chr(key) == 'U':
        xscale += 0.01
    if chr(key) == 'J':
        xscale -= 0.01
    if chr(key) == 'I':
        yscale += 0.01
    if chr(key) == 'K':
        yscale -= 0.01
    if chr(key) == 'O':
        zscale += 0.01
    if chr(key) == 'L':
        zscale -= 0.01
    if chr(key) == 'Z':
        scale += 0.01
    if chr(key) == 'X':
        scale -= 0.01
    if chr(key) == 'C' and action == 1:
        colormode = not colormode

    if chr(key) == 'Q':
        ypos += 0.01
    if chr(key) == 'A':
        ypos -= 0.01
    if chr(key) == 'W':
        xpos += 0.01
    if chr(key) == 'S':
        xpos -= 0.01
    if chr(key) == 'E':
        zpos += 0.01
    if chr(key) == 'D':
        zpos -= 0.01

    if chr(key) == 'R':
        oztr += 0.01
    if chr(key) == 'F':
        oztr -= 0.01
    if chr(key) == 'T':
        oytr += 0.01
    if chr(key) == 'G':
        oytr -= 0.01
    if chr(key) == 'Y':
        oxtr += 0.01
    if chr(key) == 'H':
        oxtr -= 0.01


size_x, size_y = 450, 450


def main():
    if not glfw.init():
        return
    window = glfw.create_window(2 * size_x, 2 * size_y, "lab", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, moveevent)

    glClearColor(0.3, 0.3, 0.3, 1)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    glMultMatrixd([1, 0, 0, 0,  # move back
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   -0.9, -0.9, 0.2, 1])
    cos45 = math.sqrt(2) / 2
    glMultMatrixd([1, 0, 0, 0,  # ox 45
                   0, cos45, cos45, 0,
                   0, -cos45, cos45, 0,
                   0, 0, 0, 1])
    glMultMatrixd([cos45, cos45, 0, 0,  # oz 45
                   -cos45, cos45, 0, 0,
                   0, 0, 1, 0,
                   0, 0, 0, 1])
    glMultMatrixd([1, 0, 0, 0,  # move to center
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   0.9, 0.9, -0.2, 1])
    glPushMatrix()

    def mainbox():
        glMultMatrixd([scale * xscale, 0, 0, 0,  # back center + scale
                       0, scale * yscale, 0, 0,
                       0, 0, scale * zscale, 0,
                       0, 0, 0.5, 1])
        glMultMatrixd([math.cos(oztr), math.sin(oztr), 0, 0,  # z rotate
                       -math.sin(oztr), math.cos(oztr), 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1])
        glMultMatrixd([math.cos(oytr), 0, math.sin(oytr), 0,  # y rotate
                       0, 1, 0, 0,
                       -math.sin(oytr), 0, math.cos(oytr), 0,
                       0, 0, 0, 1])
        glMultMatrixd([1, 0, 0, 0,  # x rotate
                       0, math.cos(oxtr), -math.sin(oxtr), 0,
                       0, math.sin(oxtr), math.cos(oxtr), 0,
                       0, 0, 0, 1])
        glMultMatrixd([1, 0, 0, 0,  # move to center
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, -0.5, 1])
        glBegin(GL_QUADS if colormode else GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glColor3f(0, 1, 0)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glColor3f(0, 0, 1)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glColor3f(0, 0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glColor3f(0.5, 0.2, 0.7)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glColor3f(0.5, 0.5, 0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glEnd()

    def minibox():
        glPopMatrix()
        glBegin(GL_QUADS)
        glColor3f(0.8, 0.2, 0.2)
        glVertex3f(-0.9, -0.9, 0.2)
        glVertex3f(-0.8, -0.9, 0.2)
        glVertex3f(-0.8, -0.8, 0.2)
        glVertex3f(-0.9, -0.8, 0.2)
        glColor3f(0.2, 0.8, 0.2)
        glVertex3f(-0.9, -0.9, 0.2)
        glVertex3f(-0.9, -0.9, 0.3)
        glVertex3f(-0.9, -0.8, 0.3)
        glVertex3f(-0.9, -0.8, 0.2)
        glColor3f(0.2, 0.2, 0.8)
        glVertex3f(-0.9, -0.9, 0.2)
        glVertex3f(-0.8, -0.9, 0.2)
        glVertex3f(-0.8, -0.9, 0.3)
        glVertex3f(-0.9, -0.9, 0.3)
        glEnd()
        glPushMatrix()

    def ortograph():
        # front view
        glViewport(0, size_y, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, -1, 0,
                       0, 0, 0, 1])
        mainbox()
        # top view
        glViewport(0, 0, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([1, 0, 0, 0,
                       0, 0, -1, 0,
                       0, -1, 0, 0,
                       0, 0, 0, 1])
        mainbox()
        # side view
        glViewport(size_x, size_y, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([0, 0, -1, 0,
                       0, 1, 0, 0,
                       -1, 0, 0, 0,
                       0, 0, 0, 1])
        mainbox()
        # main view
        glViewport(size_x, 0, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([0.87, 0, 1, 0.5,  # double point perspective
                       0, 1, 0, 0,
                       0.5, 0, -1.73, -0.87,
                       0, 0, 1, 2])
        glMultMatrixd([1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       xpos, ypos, zpos, 1])
        mainbox()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ortograph()
        minibox()
        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
