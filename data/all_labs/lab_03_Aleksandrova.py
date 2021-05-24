import pyglet
from pyglet import *
from pyglet.gl import *
from pyglet.window import key
import math

window = pyglet.window.Window(600, 600) #размер окна
pyglet.gl.glClearColor(0, 0, 0, 0) #цвет фона
current_offset = []
main_array_big = []
main_array_small = []
div_height = 5
div_angle_main = 7
div_angle_sub = 15
radius_sub_big = 6
radius_sub_small = 3
radius_main = 10
radius_sub = 5
height = 90
x = 40
y = 0
z = 40
angle_x = 0
angle_y = 0
angle_z = 0
lines = True
flag1 = False

@window.event
def on_draw():
    window.clear()
    if lines:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(25, 0, 1, 0)
    glRotatef(-5, 1, 0, 0)
    #передняя
    glBegin(GL_QUADS)
    glColor3ub(206, 113, 243)
    glVertex3f(-0.7, -0.7, -0.5)
    glColor3ub(252, 111, 144)
    glVertex3f(-0.5, -0.7, -0.5)
    glColor3ub(135, 127, 244)
    glVertex3f(-0.5, -0.5, -0.5)
    glColor3ub(248, 255, 112)
    glVertex3f(-0.7, -0.5, -0.5)
    glEnd()
    #задняя
    glBegin(GL_QUADS)
    glColor3ub(255, 120, 0)
    glVertex3f(-0.7, -0.7, -0.7)
    glColor3ub(86, 20, 208)
    glVertex3f(-0.5, -0.7, -0.7)
    glColor3ub(178, 247, 0)
    glVertex3f(-0.5, -0.5, -0.7)
    glColor3ub(170, 80, 0)
    glVertex3f(-0.7, -0.5, -0.7)
    glEnd()
    #нижняя грань
    glBegin(GL_QUADS)
    glColor3ub(59, 100, 250)
    glVertex3f(-0.7, -0.7, -0.7)
    glColor3ub(255, 140, 0)
    glVertex3f(-0.7, -0.7, -0.5)
    glColor3ub(78, 95, 150)
    glVertex3f(-0.5, -0.7, -0.5)
    glColor3ub(153, 190, 250)
    glVertex3f(-0.5, -0.7, -0.7)
    glEnd()
    #левая грань
    glBegin(GL_QUADS)
    glColor3ub(240, 142, 15)
    glVertex3f(-0.7, -0.7, -0.7)
    glColor3ub(224, 237, 15)
    glVertex3f(-0.7, -0.5, -0.7)
    glColor3ub(179, 11, 133)
    glVertex3f(-0.7, -0.5, -0.5)
    glColor3ub(19, 98, 154)
    glVertex3f(-0.7, -0.7, -0.5)
    glEnd()
    #верхняя
    glBegin(GL_QUADS)
    glColor3ub(186, 114, 228)
    glVertex3f(-0.7, -0.5, -0.7)
    glColor3ub(236, 127, 195)
    glVertex3f(-0.7, -0.5, -0.5)
    glColor3ub(151, 121, 229)
    glVertex3f(-0.5, -0.5, -0.5)
    glColor3ub(255, 254, 120)
    glVertex3f(-0.5, -0.5, -0.7)
    glEnd()
    # правая грань
    glBegin(GL_QUADS)
    glColor3ub(116, 2, 136)
    glVertex3f(-0.5, -0.7, -0.7)
    glColor3ub(178, 0, 69)
    glVertex3f(-0.5, -0.7, -0.5)
    glColor3ub(57, 9, 139)
    glVertex3f(-0.5, -0.5, -0.5)
    glColor3ub(178, 201, 0)
    glVertex3f(-0.5, -0.5, -0.7)
    glEnd()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, 600.0/600.0, 0.1, 1000.0)
    glRotatef(135, 0, 1, 0)
    glTranslatef(x, y, z)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)
    print('x = ' + str(x))
    print('y = ' + str(y))
    print('z = ' + str(z))
    print('angle_x = ' + str(angle_x))
    print('angle_y = ' + str(angle_y))
    print('angle_z = ' + str(angle_z))
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    creation()
    drawing()

@window.event
def on_key_press(symbol, modkey):
    global div_height, x, y, z, angle_x, angle_y, angle_z, div_angle_sub, lines, flag1
    if symbol == pyglet.window.key.DOWN:
        div_height -= 1
    if symbol == pyglet.window.key.UP:
        div_height += 1
    if symbol == pyglet.window.key.LEFT:
        div_angle_sub -= 1
    if symbol == pyglet.window.key.RIGHT:
        div_angle_sub += 1
    if symbol == pyglet.window.key.E:
        x -= 10
    if symbol == pyglet.window.key.D:
        y -= 10
    if symbol == pyglet.window.key.C:
        z -= 10
    if symbol == pyglet.window.key.T:
        x += 10
    if symbol == pyglet.window.key.G:
        y += 10
    if symbol == pyglet.window.key.B:
        z += 10
    if symbol == pyglet.window.key.Q:
        angle_x -= 5
    if symbol == pyglet.window.key.W:
        angle_x += 5
    if symbol == pyglet.window.key.A:
        angle_y -= 5
    if symbol == pyglet.window.key.S:
        angle_y += 5
    if symbol == pyglet.window.key.Z:
        angle_z -= 5
    if symbol == pyglet.window.key.X:
        angle_z += 5
    if symbol == pyglet.window.key.R:
        flag1 = not flag1
        if flag1:
            x = 80
            y = 30
            z = 40
            angle_x = 90
            angle_y = 10
            angle_z = 5
            div_height = 1
    if symbol == pyglet.window.key.ENTER:
        lines = not lines

def creation():
    global main_array, current_offset, div_angle_sub, main_array_big, main_array_small, div_height
    main_array = []
    current_offset = []
    main_array_big = []
    main_array_small = []
    height_current = 0
    if div_height == 0:
        div_height = 1
    if div_angle_sub == 2:
        div_angle_sub = 3
    height_changes = height / div_height
    angle = 0
    angle_change = 6 * math.pi / div_height
    while height_current <= height + 0.01:
        x = radius_main * math.cos(angle)
        y = radius_main * math.sin(angle)
        current_offset.append(x)
        current_offset.append(y)
        current_offset.append(height_current)
        angle += angle_change
        height_current += height_changes

    for i in range(0, len(current_offset), 3):
        current_array = []
        dx = current_offset[i]
        dy = current_offset[i + 1]
        dz = current_offset[i + 2]
        angle = 0
        angle_change = 2 * math.pi / div_angle_sub
        while angle < 2 * math.pi + 0.01:
             x = radius_sub_big * math.cos(angle)
             y = radius_sub_big * math.sin(angle)
             angle += angle_change
             current_array.append(x + dx)
             current_array.append(y + dy)
             current_array.append(dz)
        x = radius_sub_small * math.cos(0)
        y = radius_sub_small * math.sin(0)
        current_array.append(x + dx)
        current_array.append(y + dy)
        current_array.append(dz)
        main_array_big.append(current_array)

    for i in range(0, len(current_offset), 3):
        current_array = []
        dx = current_offset[i]
        dy = current_offset[i + 1]
        dz = current_offset[i + 2]
        angle = 0
        angle_change = 2 * math.pi / div_angle_sub
        while angle < 2 * math.pi + 0.01:
             x = radius_sub_small * math.cos(angle)
             y = radius_sub_small * math.sin(angle)
             angle += angle_change
             current_array.append(x + dx)
             current_array.append(y + dy)
             current_array.append(dz)
        x = radius_sub_small * math.cos(0)
        y = radius_sub_small * math.sin(0)
        current_array.append(x + dx)
        current_array.append(y + dy)
        current_array.append(dz)
        main_array_small.append(current_array)

def drawing():
    cap_down_big = main_array_big[0]
    cap_down_small = main_array_small[0]
    glBegin(GL_QUADS)
    for i in range(0, len(cap_down_big) - 6, 3): #первый сигмент
        glColor3ub(105, 8, 95)
        glVertex3d(cap_down_big[i], cap_down_big[i + 1], cap_down_big[i + 2])
        glColor3ub(138, 41, 128)
        glVertex3d(cap_down_small[i], cap_down_small[i + 1], cap_down_small[i + 2])
        glColor3ub(199, 56, 185)
        glVertex3d(cap_down_small[i + 3], cap_down_small[i + 4], cap_down_small[i + 5])
        glColor3ub(255, 255, 255)
        glVertex3d(cap_down_big[i + 3], cap_down_big[i + 4], cap_down_big[i + 5])
    glEnd()

    glBegin(GL_QUADS) #отверстие
    for i in range(0, len(main_array_small) - 1):
        for j in range(0, len(main_array_small[i]) - 6, 3):
            glColor3ub(0, 0, 0)
            glVertex3d(main_array_small[i][j], main_array_small[i][j + 1], main_array_small[i][j + 2])
            glColor3ub(85, 85, 85)
            glVertex3d(main_array_small[i + 1][j], main_array_small[i + 1][j + 1], main_array_small[i + 1][j + 2])
            glColor3ub(170, 170, 170)
            glVertex3d(main_array_small[i + 1][j + 3], main_array_small[i + 1][j + 4], main_array_small[i + 1][j + 5])
            glColor3ub(255, 255, 255)
            glVertex3d(main_array_small[i][j + 3], main_array_small[i][j + 4], main_array_small[i][j + 5])
    glEnd()

    glBegin(GL_QUADS) #обертка
    for i in range(0, len(main_array_big) - 1):
        for j in range(0, len(main_array_big[i]) - 6, 3):
            glColor3ub(116, 2, 136)
            glVertex3d(main_array_big[i][j], main_array_big[i][j + 1], main_array_big[i][j + 2])
            glColor3ub(178, 0, 69)
            glVertex3d(main_array_big[i + 1][j], main_array_big[i + 1][j + 1], main_array_big[i + 1][j + 2])
            glColor3ub(57, 9, 139)
            glVertex3d(main_array_big[i + 1][j + 3], main_array_big[i + 1][j + 4], main_array_big[i + 1][j + 5])
            glColor3ub(133, 105, 179)
            glVertex3d(main_array_big[i][j + 3], main_array_big[i][j + 4], main_array_big[i][j + 5])
    glEnd()

    cap_up_big = main_array_big[len(main_array_big) - 1]
    cap_up_small = main_array_small[len(main_array_small) - 1]
    glBegin(GL_QUADS)
    for i in range(0, len(cap_up_big) - 6, 3): #остальные сегменты
        glColor3ub(105, 8, 95)
        glVertex3d(cap_up_big[i], cap_up_big[i + 1], cap_up_big[i + 2])
        glColor3ub(138, 41, 128)
        glVertex3d(cap_up_small[i], cap_up_small[i + 1], cap_up_small[i + 2])
        glColor3ub(199, 56, 185)
        glVertex3d(cap_up_small[i + 3], cap_up_small[i + 4], cap_up_small[i + 5])
        glColor3ub(255, 255, 255)
        glVertex3d(cap_up_big[i + 3], cap_up_big[i + 4], cap_up_big[i + 5])
    glEnd()

pyglet.app.run()
