import pyglet
import random
import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse


@window.event
def on_draw():
    global RGB, square, steps_sq
    global main, angle, xyz, scalling


    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if three_dots:
        gluPerspective(130.0, 1600.0/900.0, 0.1, 1000.0)
        glRotatef(45, 0, 1, 0)
        glRotatef(45, 1, 0, 1)
    else:
        gluPerspective(90.0, 1600.0/900.0, 0.1, 1000.0)



    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    pyglet.graphics.draw_indexed(int(len(start_sq) / 3), GL_TRIANGLES,
    steps_square_pol,
    ('v3i', start_sq),
    ('c3B', RGB_sq * int(len(start_sq) / 3)))


    rotate = [math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[0]*xyz[0]), (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) + float(xyz[2])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) - float(xyz[1])*math.sin(angle), 0.0,
          (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) - float(xyz[2])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[1]*xyz[1]), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) + float(xyz[0])*math.sin(angle), 0.0,
          (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) + float(xyz[1])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) - float(xyz[0])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[2]*xyz[2]), 0.0,
          0.0, 0.0, 0.0, 1.0]
    main = mult_matrix(main, translatef)
    main = mult_matrix(main, scalling)
    main = mult_matrix(main, rotate)

    glTranslatef(*pos)
    glMultMatrixd((gl.GLdouble * len(main))(*main))


    if pol_not_lines:
        pyglet.graphics.draw_indexed(int(len(square) / 3), GL_TRIANGLES,
        steps_square_pol,
        ('v3i', square),
        ('c3B', RGB * int(len(square) / 3)))
    else:
        pyglet.graphics.draw_indexed(int(len(square) / 3), GL_LINES,
        steps_square_lines,
        ('v3i', square),
        ('c3B', RGB * int(len(square) / 3)))




@window.event
def update(dt):
    pass

@window.event
def on_key_press(symbol, modkey):
    print("vain")
    global start_sq
    start_sq = [-40, -10, -40,
            -50, -10, -40,
            -50, -20, -40,
            -40, -20, -40,
            -40, -10, -45,
            -50, -10, -45,
            -50, -20, -45,
            -40, -20, -45]
    if symbol == pyglet.window.key.ENTER:
        global  pol_not_lines
        pol_not_lines = not pol_not_lines
    if symbol == pyglet.window.key.F:
        global three_dots
        three_dots = not three_dots
    if three_dots:
        start_sq = [-20, -10, -20,
            -30, -10, -20,
            -30, -20, -20,
            -20, -20, -20,
            -20, -10, -25,
            -30, -10, -25,
            -30, -20, -25,
            -20, -20, -25]
    if symbol == pyglet.window.key.R:
        global main, rotate
        rotate = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
        main = rotate
    if symbol == key.SPACE:
        global RGB
        RGB = (random.randint(min_color, max_color),
        random.randint(min_color, max_color),
        random.randint(min_color, max_color))

    global translatef, scalling, xyz, angle, angle_x, angle_y, angle_z
    scalling = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    xyz = [0, 0, 0]
    angle = 0

    if symbol == pyglet.window.key.Q:
        angle = math.pi/12
        xyz = [1, 0, 0]
    if symbol == pyglet.window.key.W:
        angle = -math.pi/12
        xyz = [1, 0, 0]
    if symbol == pyglet.window.key.A:
        angle = math.pi/12
        xyz = [0, 1, 0]
    if symbol == pyglet.window.key.S:
        angle = -math.pi/12
        xyz = [0, 1, 0]
    if symbol == pyglet.window.key.Z:
        angle = math.pi/12
        xyz = [0, 0, 1]
    if symbol == pyglet.window.key.X:
        angle = -math.pi/12
        xyz = [0, 0, 1]
    if symbol == pyglet.window.key.UP:
        for i in range(3):
            scalling[4*i + i] *= 2
    if symbol == pyglet.window.key.DOWN:
        for i in range(3):
            scalling[4*i + i] /= 2

    if symbol == pyglet.window.key.E:
        translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        20.0, 0.0, 0.0, 1.0]
    if symbol == pyglet.window.key.D:
        translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 20.0, 0.0, 1.0]
    if symbol == pyglet.window.key.C:
        translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 20.0, 1.0]
    if symbol == pyglet.window.key.T:
        translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        -20.0, 0.0, 0.0, 1.0]
    if symbol == pyglet.window.key.G:
        translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, -20.0, 0.0, 1.0]
    if symbol == pyglet.window.key.B:
        translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, -20.0, 1.0]




@window.event
def on_mouse_press(x, y, button, modifiers):
    pass

def mult_matrix(martix1, matrix2):
    i, j, k = 0, 0, 0
    matrix = list()
    for i in range(4):
        for j in range(4):
            number = 0
            for k in range(4):
                number += float(martix1[4*k + j] * matrix2[4*i + k])
            matrix.append(number)
    return matrix

if __name__ == "__main__":

    pyglet.app.run()
