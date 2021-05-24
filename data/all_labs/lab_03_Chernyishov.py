import pyglet
import random
import math
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse


min_color = 0
max_color = 255
pos = [0, -20, -120]
window = pyglet.window.Window(1600, 900)
h = 1600,
w = 900
pyglet.gl.glClearColor(0.7, 0.7, 0.7, 0.7)
start_sq = [-20, -10, -40,
            -30, -10, -40,
            -30, -20, -40,
            -20, -20, -40,
            -20, -10, -50,
            -30, -10, -50,
            -30, -20, -50,
            -20, -20, -50]
steps_square_pol = [0, 1, 2, 3, 4, 5, 6, 7,
                    0, 1, 5, 4, 2, 6, 7, 3,
                    1, 2, 6, 5, 0, 3, 7 ,4]

RGB_sq = (30, 60, 35)
RGB = (1, 20, 30)

a = 15
b = 30
height = 30
angle = 0
angle_c = 6
height_c = 5
wall = []
cap_d = []
cap_u = []

xyz = [0, 0, 0]
scalling = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
main = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]

three_dots = False
pol_not_lines = True
changes = True

def view():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, 1600, 900)
    if three_dots:
        gluPerspective(130.0, 1600.0/900.0, 0.1, 1000.0)
        glRotatef(45, 0, 1, 0)
        glRotatef(45, 1, 0, 1)
    else:
        gluPerspective(90.0, 1600.0/900.0, 0.1, 1000.0)

def min_cube():
    global start_sq, steps_square_pol, RGB_sq
    pyglet.graphics.draw_indexed(int(len(start_sq) / 3), GL_QUADS,
    steps_square_pol,
    ('v3i', start_sq),
    ('c3B', RGB_sq * int(len(start_sq) / 3)))

def rotate_function(angle):
    return [math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[0]*xyz[0]), (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) + float(xyz[2])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) - float(xyz[1])*math.sin(angle), 0.0,
          (1.0 - math.cos(angle))*float(xyz[0]*xyz[1]) - float(xyz[2])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[1]*xyz[1]), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) + float(xyz[0])*math.sin(angle), 0.0,
          (1.0 - math.cos(angle))*float(xyz[0]*xyz[2]) + float(xyz[1])*math.sin(angle), (1.0 - math.cos(angle))*float(xyz[1]*xyz[2]) - float(xyz[0])*math.sin(angle), math.cos(angle) + (1.0 - math.cos(angle))*float(xyz[2]*xyz[2]), 0.0,
          0.0, 0.0, 0.0, 1.0]

def figure_prepare ():
    global a, b, height, angle_c, height_c, RGB
    global wall, cap_d, cap_u
    wall = []
    cap_d = []
    cap_u = []
    angle_building = 0.0
    height_building = -height
    height_current = 2 * height / height_c
    while height_building + height_current <= height + 0.01:
        while angle_building <= 2 * math.pi + 0.01:
                x = a * math.cos(angle_building)
                y = b * math.sin(angle_building)
                wall.append([x, height_building + height_current, y])
                wall.append([x, height_building, y])
                angle_building += 2 * math.pi / angle_c
        wall.append([x, height_building + height_current, 0])
        wall.append([x, height_building, 0])    
        height_building += height_current
        angle_building = 0

    angle_building = 0.0
    while angle_building <= 2*math.pi:
            x = a * math.cos(angle_building)
            y = b * math.sin(angle_building)
            cap_u.append([x, height, y])
            angle_building += 2 * math.pi / angle_c
            cap_u.append([0, height, 0])
            x = a * math.cos(angle_building)
            y = b * math.sin(angle_building)
            cap_u.append([x, height, y])
            
    angle_building = 0.0
    while angle_building <= 2*math.pi:
            x = a * math.cos(angle_building)
            y = b * math.sin(angle_building)
            cap_d.append([x, -height, y])
            angle_building += 2 * math.pi / angle_c
            cap_d.append([0, -height, 0])
            x = a * math.cos(angle_building)
            y = b * math.sin(angle_building)
            cap_d.append([x, -height, y])

def figure_drawing():
    global wall, cap_d, cap_u
    glBegin(GL_QUAD_STRIP)
    glColor3b(*RGB)
    for point in wall:
        glVertex3d(point[0], point[1], point[2])
    glEnd();

    glBegin(GL_TRIANGLES)
    glColor3b(*RGB)
    for point in cap_d:
        glVertex3d(point[0], point[1], point[2])
    glEnd();

    glBegin(GL_TRIANGLES)
    glColor3b(*RGB)
    for point in cap_u:
        glVertex3d(point[0], point[1], point[2])
    glEnd();

    
@window.event
def on_draw():
    window.clear()
    view()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(10, 0, 0)
    if pol_not_lines:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    min_cube()
    glTranslatef(10, 0, 0)

    global  main, angle, scalling, translatef
    main = mult_matrix(main, rotate_function(angle))
    main = mult_matrix(main, scalling)
    main = mult_matrix(main, translatef)

    glTranslatef(*pos)
    glMultMatrixd((gl.GLdouble * len(main))(*main))

    global changes
    if changes:
        figure_prepare()
    figure_drawing()
    

    


@window.event  
def update(dt):
    pass

def restart_full():
    global main, angle, angle_c, height_c, scalling, rotate, translatef, changes
    main = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    angle = 0
    angle_c = 6
    height_c = 5
    scalling = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    xyz = [0, 0, 0]
    changes = True

def restart():
    global angle, scalling, rotate, translatef, changes
    angle = 0
    scalling = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    translatef = [1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0]
    xyz = [0, 0, 0]
    changes = False
      
  
@window.event
def on_key_press(symbol, modkey):
    restart()
    if symbol == pyglet.window.key.ENTER:
        global  pol_not_lines
        pol_not_lines = not pol_not_lines
    if symbol == pyglet.window.key.F:
        global three_dots
        three_dots = not three_dots
    if symbol == pyglet.window.key.R:
        restart_full()
    if symbol == key.SPACE:
        global RGB
        RGB = (random.randint(min_color, max_color),
        random.randint(min_color, max_color),
        random.randint(min_color, max_color))
    
    

    global scalling, xyz, angle, scalling
    if symbol == pyglet.window.key.Q:
        angle = math.pi/6
        xyz = [1, 0, 0]
    if symbol == pyglet.window.key.W:
        angle = -math.pi/6
        xyz = [1, 0, 0]
    if symbol == pyglet.window.key.A:
        angle = math.pi/6
        xyz = [0, 1, 0]
    if symbol == pyglet.window.key.S:
        angle = -math.pi/6
        xyz = [0, 1, 0]
    if symbol == pyglet.window.key.Z:
        angle = math.pi/6
        xyz = [0, 0, 1]
    if symbol == pyglet.window.key.X:
        angle = -math.pi/6
        xyz = [0, 0, 1]
    if symbol == pyglet.window.key.UP:
        for i in range(3):
            scalling[4*i + i] *= 2
    if symbol == pyglet.window.key.DOWN:
        for i in range(3):
            scalling[4*i + i] /= 2

    global translatef
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

    global angle_c, height_c, changes
    if symbol == pyglet.window.key.P:
        angle_c += 1
        changes = True
    if symbol == pyglet.window.key.O:
        angle_c -= 1
        if angle_c == 0:
            angle_c = 1
        changes = True
    if symbol == pyglet.window.key.K:
        height_c += 1
        changes = True
    if symbol == pyglet.window.key.L:
        height_c -= 1
        if height_c == 0:
            height_c = 1
        changes = True

    
    
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
            



pyglet.app.run()

