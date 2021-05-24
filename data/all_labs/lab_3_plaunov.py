import pyglet
from pyglet.gl import *
from math import *


pos = [100, 0, -160]
pos_prizme = [0, 0, 0]
rot_y = 0
status = False
delta = 100
side_polygon = 3
inside_polygon = 3

wind = pyglet.window.Window(height=700, width=700, resizable=True)
#wind.maximize()
z = 0.75
ux = 0
uz = 0
data = []
size = 500
edge = 12

def make_prizme(ux, uz, n):
    global data, inside_polygon
    u = inside_polygon

    angle = radians(360 / n)
    data = [[] for i in range(u + 1)]
    for i in range(u + 1):
        data[i].append([ux * (u - i) / u, 0, uz * (u - i) / u])
    for j in range(n):
        ux, uz = ux * cos(angle) - uz * sin(angle), ux * sin(angle) + uz * cos(angle)
        for i in range(u + 1):
            data[i].append([ux * (u - i) / u, 0, uz * (u - i) / u])
    print(data)

make_prizme(delta, 0, edge)

def draw_cube(x, y, z, u):
    glBegin(GL_QUAD_STRIP)

    glVertex3f(x, y, z)
    glVertex3f(x, y, z + u)
    glVertex3f(x + u, y, z)
    glVertex3f(x + u, y, z + u)
    glVertex3f(x + u, y + u, z)
    glVertex3f(x + u, y + u, z + u)
    glVertex3f(x, y + u, z)
    glVertex3f(x, y + u, z + u)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + u)

    glEnd()
    glBegin(GL_QUAD_STRIP)
    glVertex3f(x, y, z)
    glVertex3f(x + u, y, z)
    glVertex3f(x, y + u, z)
    glVertex3f(x + u, y + u, z)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(x, y, z + u)
    glVertex3f(x + u, y, z + u)
    glVertex3f(x + u, y + u, z + u)
    glVertex3f(x, y + u, z + u)
    glEnd()
    glFlush()

def draw_prizme(dx, dy, dz, n, u):
    glRotatef(pos_prizme[0], 1, 0, 0)
    glRotatef(pos_prizme[1], 0, 1, 0)
    glRotatef(pos_prizme[2], 0, 0, 1)


    for i in range(3):
        glBegin(GL_QUAD_STRIP)
        for j in range(n):
            glVertex3d(*data[i][j])
            glVertex3d(*data[i + 1][j])
        glVertex3d(*data[i][0])
        glVertex3d(*data[i + 1][0])
        glEnd()
    for i in range(3):
        glBegin(GL_QUAD_STRIP)
        for j in range(n):
            glVertex3d(data[i][j][0] + dx, data[i][j][1] + dy, data[i][j][2] + dz)
            glVertex3d(data[i + 1][j][0] + dx, data[i + 1][j][1] + dy, data[i + 1][j][2] + dz)
        glVertex3d(data[i][0][0] + dx, data[i][0][1] + dy, data[i][0][2] + dz)
        glVertex3d(data[i + 1][0][0] + dx, data[i + 1][0][1] + dy, data[i + 1][0][2] + dz)
        glEnd()
    # glBegin(GL_POLYGON)
    # for i in range(n):
    #     glVertex3d(data[i][0] + dx, data[i][1] + dy, data[i][2] + dz)
    # glEnd()
    for i in range(1, u + 1):
        glBegin(GL_QUAD_STRIP)
        for j in range(n):
            glVertex3d(data[0][j][0] + dx * (i - 1) / u, data[0][j][1] + dy * (i - 1) / u, data[0][j][2] + dz * (i - 1) / u)
            glVertex3d(data[0][j][0] + dx * i / u, data[0][j][1] + dy * i / u, data[0][j][2] + dz * i / u)
        glVertex3d(data[0][0][0] + dx * (i - 1) / u, data[0][0][1] + dy * (i - 1) / u, data[0][0][2] + dz * (i - 1) / u)
        glVertex3d(data[0][0][0] + dx * i / u, data[0][0][1] + dy * i / u, data[0][0][2] + dz * i / u)
        glEnd()
    glFlush()

@wind.event
def on_draw():
    global pos, rot_y, edge

    wind.clear()

    glMatrixMode(GL_PROJECTION)
    # glPushMatrix()
    ux = degrees(asin(z / ((2) ** 0.5)))
    uz = degrees(asin(z / (2 - z ** 2) ** 0.5))
    print(ux, uz)

    glLoadIdentity()

    glRotatef(uz, 1, 0, 0)
    glRotatef(ux, 0, 1, 0)
    glOrtho(-size, size, -size, size, -size, size)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_cube(0, 0, 0, 100)
    glTranslatef(*pos)
    draw_prizme(100, 100, 100, edge, side_polygon)


    #glRotatef(rot_y, 0, 1, 0)
    #draw_cube(0, 0, 0, 10)
    # glBegin(GL_POLYGON)
    # glVertex3f(-5,-5,0)
    # glVertex3f(5,-5,0)
    # glVertex3f(0,5,0)
    # glEnd()

    glFlush()

@wind.event
def on_key_press(s,m):
    global pos, z, status, delta, data, edge, side_polygon
    if s == pyglet.window.key.ENTER:
        if status:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            status = False
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            status = True
    if s == pyglet.window.key.EQUAL:
        edge += 1
        make_prizme(delta, 0, edge)
    if s == pyglet.window.key.MINUS:
        edge -= 1
        make_prizme(delta, 0, edge)

    if s == pyglet.window.key.A:
        pos[0] -= 9
    if s == pyglet.window.key.D:
        pos[0] += 9
    if s == pyglet.window.key.LEFT:
        pos_prizme[0] += 3
        #make_prizme(*pos_prizme)
    if s == pyglet.window.key.RIGHT:
        pos_prizme[0] -= 3
        #make_prizme(*pos_prizme)
    if s == pyglet.window.key.UP:
        delta += 3
        make_prizme(delta, 0, edge)
    if s == pyglet.window.key.DOWN:
        if delta >= 3:
            delta -= 3
            make_prizme(delta, 0, edge)
    if s == pyglet.window.key.W:
        pos[2] -= 9
    if s == pyglet.window.key.S:
        pos[2] += 9
    if s == pyglet.window.key._0:
        side_polygon += 1
    if s == pyglet.window.key._9:
        if side_polygon > 1:
            side_polygon -= 1
    if s == pyglet.window.key.Q:
        if (z <= 0.9):
            z += 0.1
    if s == pyglet.window.key.E and z >= 0.1:
        z -= 0.1

@wind.event()
def on_resize(width, height):
    global size
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    # glPushMatrix()
    ux = degrees(asin(z / ((2) ** 0.5)))
    uz = degrees(asin(z / (2 - z ** 2) ** 0.5))
    glLoadIdentity()

    glRotatef(uz, 1, 0, 0)
    glRotatef(ux, 0, 1, 0)
    u = max(width, height)
    size = u
    glOrtho(-u, u, -u, u, -u, u)
    glMatrixMode(GL_MODELVIEW)

pyglet.app.run()