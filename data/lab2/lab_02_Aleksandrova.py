import pyglet
import math
from pyglet.gl import *
from pyglet.window import key


@window.event
def on_draw():
    global RGB, square, steps_sq, main, angle, xyz, scalling

    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if three_dots:
        gluPerspective(130.0, 1000.0/600.0, 0.1, 1000.0)
        glRotatef(45, 0, 1, 0)
        glRotatef(45, 1, 0, 1)
    else:
        gluPerspective(90.0, 1000.0/600.0, 0.1, 1000.0)

    glMatrixMode(GL_MODELVIEW)
    if pol_not_lines:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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

    pyglet.graphics.draw_indexed(int(len(square) / 3), GL_TRIANGLES,
    steps_square_pol,
    ('v3i', square),
    ('c3B', RGB * int(len(square) / 3)))


@window.event
def on_key_press(symbol, modkey):
    global start_sq, translatef, scalling, xyz, angle, angle_x, angle_y, angle_z, pol_not_lines, three_dots, main, rotate
    start_sq = [-50, -40, -50,
            -60, -40, -50,
            -60, -50, -50,
            -50, -50, -50,
            -50, -40, -55,
            -60, -40, -55,
            -60, -50, -55,
            -50, -50, -55]
    if symbol == pyglet.window.key.ENTER:
        pol_not_lines = not pol_not_lines
    if symbol == pyglet.window.key.F:
        three_dots = not three_dots
        if three_dots:
            start_sq = [-50, -40, -50,
                -60, -40, -50,
                -60, -50, -50,
                -50, -50, -50,
                -50, -40, -55,
                -60, -40, -55,
                -60, -50, -55,
                -50, -50, -55]
        angle = 0
        translatef = [1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0]
        main = [1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0]
        square = [-15, -15, -15,
                  15, -15, -15,
                  15, 15, -15,
                  -15, 15, -15,
                  -15, -15, 15,
                  15, -15, 15,
                  15, 15, 15,
                  -15, 15, 15]
        for i in range(3):
            translatef = [1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            20.0, 0.0, 0.0, 1.0]
            main = mult_matrix(main, translatef)
        for i in range(5):
            translatef = [1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 20.0, 1.0]
            main = mult_matrix(main, translatef)
        angle = -math.pi/12
        xyz = [0, 1, 0]
        rotate = [math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[0]*xyz[0]), (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) + float(xyz[2])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) - float(xyz[1])*math.sin(angle), 0.0,
                 (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) - float(xyz[2])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[1]*xyz[1]), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) + float(xyz[0])*math.sin(angle), 0.0,
                 (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) + float(xyz[1])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) - float(xyz[0])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[2]*xyz[2]), 0.0,
                 0.0, 0.0, 0.0, 1.0]
        main = mult_matrix(main, rotate)
        angle = 0
        for i in range(2):
            translatef = [1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            -20.0, 0.0, 0.0, 1.0]
            main = mult_matrix(main, translatef)
        for i in range(2):
            angle = math.pi/12
            xyz = [0, 1, 0]
            rotate = [math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[0]*xyz[0]), (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) + float(xyz[2])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) - float(xyz[1])*math.sin(angle), 0.0,
                     (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) - float(xyz[2])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[1]*xyz[1]), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) + float(xyz[0])*math.sin(angle), 0.0,
                     (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) + float(xyz[1])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) - float(xyz[0])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[2]*xyz[2]), 0.0,
                     0.0, 0.0, 0.0, 1.0]
            main = mult_matrix(main, rotate)
        angle = 0
        translatef = [1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0]
    if symbol == pyglet.window.key.R:
        rotate = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
        main = rotate

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
