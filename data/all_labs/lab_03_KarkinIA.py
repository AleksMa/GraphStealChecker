import math

import glfw
from OpenGL.GL import *
import time
import numpy as np

dt = 0
xpos = ypos = zpos = 0
oxtr = oytr = oztr = 0
xscale = yscale = zscale = 1
scale = 0.1
colormode = False
vertex_height_count = 1  # кол-во эллипсов в единицу t
vertex_lenght_count = 3  # общее кол-во вершин(3)
t_param = 3  # высота спирали
changes = True
figure = None


def moveevent(window, key, scancode, action, mods):
    global xpos, ypos, zpos
    global oztr, oytr, oxtr
    global scale, colormode, xscale, yscale, zscale
    global vertex_height_count, vertex_lenght_count, t_param, changes
    if chr(key) == 'U':
        xscale += dt
    if chr(key) == 'J':
        xscale -= dt
    if chr(key) == 'I':
        yscale += dt
    if chr(key) == 'K':
        yscale -= dt
    if chr(key) == 'O':
        zscale += dt
    if chr(key) == 'L':
        zscale -= dt

    if chr(key) == 'Z':
        scale += dt / 10
    if chr(key) == 'X':
        scale -= dt / 10
    if chr(key) == 'C' and action == 1:
        colormode = not colormode

    if chr(key) == 'Q':
        ypos += dt
    if chr(key) == 'A':
        ypos -= dt
    if chr(key) == 'W':
        xpos += dt
    if chr(key) == 'S':
        xpos -= dt
    if chr(key) == 'E':
        zpos += dt
    if chr(key) == 'D':
        zpos -= dt

    if chr(key) == 'R':
        oztr += dt
    if chr(key) == 'F':
        oztr -= dt
    if chr(key) == 'T':
        oytr += dt
    if chr(key) == 'G':
        oytr -= dt
    if chr(key) == 'Y':
        oxtr += dt
    if chr(key) == 'H':
        oxtr -= dt

    if chr(key) == '1':
        vertex_height_count += 1
        changes = True
    if chr(key) == '2' and vertex_height_count > 1:
        vertex_height_count -= 1
        changes = True
    if chr(key) == '3':
        vertex_lenght_count += 1
        changes = True
    if chr(key) == '4' and vertex_lenght_count > 3:
        vertex_lenght_count -= 1
        changes = True
    if chr(key) == '5':
        t_param += 1
        changes = True
    if chr(key) == '6' and t_param > 1:
        t_param -= 1
        changes = True



size_x, size_y = 500, 500


def main():
    global dt
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

    def calc():
        ellipse_param = 2
        radius = 5  # радиус спирали

        def dx_dt(t):
            return -radius * math.sin(t)

        def dy_dt(t):
            return radius * math.cos(t)

        def x(t):
            return radius * math.cos(t)

        def y(t):
            return radius * math.sin(t)

        def z(t):
            return t

        def int_r(num):
            num = int(num + (0.5 if num > 0 else -0.5))
            return num

        quads_poly = []
        ellipse = []
        for i in range(vertex_lenght_count):
            ellipse.append(np.array([math.cos(2 * math.pi * i / vertex_lenght_count) * ellipse_param,
                            math.sin(2 * math.pi * i / vertex_lenght_count), 0]))
        t = 0
        delta_t_param = 1 / vertex_height_count
        align = 0  # параметр выравнивания t по целым числам
        while t <= t_param:
            align += 1
            pos = np.array([x(t), y(t), z(t)])
            new_z = np.array([dx_dt(t), dy_dt(t), 1])
            new_x = np.array([x(t), y(t), -(x(t) * new_z[0] + y(t) * new_z[1])])
            new_y = np.array([new_x[1] * new_z[2] - new_x[2] * new_z[1], new_x[2] * new_z[0] - new_x[0] * new_z[2],
                     new_x[0] * new_z[1] - new_x[1] * new_z[0]])
            new_z /= np.linalg.norm(new_z)
            new_y /= np.linalg.norm(new_y)
            new_x /= np.linalg.norm(new_x)
            trans_matrix = np.array([[new_x[0], new_y[0], new_z[0]],
                                     [new_x[1], new_y[1], new_z[1]],
                                     [new_x[2], new_y[2], new_z[2]]])
            if t > 0:
                trang_lines = []
                for i in range(vertex_lenght_count):
                    trang_lines.append(quads_poly[len(quads_poly) - 2 * vertex_lenght_count + 1])
                    trang_lines.append(list(trans_matrix.dot(ellipse[i]) + pos))
                    quads_poly.append(quads_poly[len(quads_poly) - 2 * vertex_lenght_count])
                    quads_poly.append(list(trans_matrix.dot(ellipse[i]) + pos))
                for i in trang_lines:
                    quads_poly.append(i)
            for i in range(vertex_lenght_count - 1):
                quads_poly.append(list(trans_matrix.dot(ellipse[i]) + pos))
                quads_poly.append(list(trans_matrix.dot(ellipse[i + 1]) + pos))
            quads_poly.append(list(trans_matrix.dot(ellipse[vertex_lenght_count - 1]) + pos))
            quads_poly.append(list(trans_matrix.dot(ellipse[0]) + pos))
            t += delta_t_param
            if align == vertex_height_count:
                align = 0
                t = int_r(t)
        return quads_poly

    def mainbox():
        global changes
        global figure
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
        if changes:
            changes = False
            figure = calc()
        glEnableClientState(GL_VERTEX_ARRAY)
        glColor(0, 1, 0)
        if not colormode:
            glVertexPointer(3, GL_FLOAT, 0, figure)
            glDrawArrays(GL_LINES, 0, len(figure))




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

    cur_time = time.time()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ortograph()
        minibox()
        glfw.swap_buffers(window)
        glfw.poll_events()
        new_time = time.time()
        dt = new_time - cur_time
        # print(1 / dt)
        cur_time = new_time
        if dt < 0.005:
            time.sleep(0.01)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
