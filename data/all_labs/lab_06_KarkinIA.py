import math

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import numpy as np
import json
from PIL import Image

dt = 0
xpos = 0
ypos = 0
zpos = 0
vx = vy = vz = 0
oxtr = oytr = oztr = 0
xscale = yscale = zscale = 1
world_xpos = world_ypos = world_zpos = 0
world_oxtr = world_oytr = world_oztr = 0
world_change = False
scale = 0.03
texmode = False
vertex_height_count = 4  # кол-во эллипсов в единицу t 6
vertex_lenght_count = 8  # общее кол-во вершин(3) 12
t_param = 20  # высота спирали 8
ellipse_param = 2
radius = 5  # радиус спирали
changes = True
normals = None
figure = None
move = False
pos0 = [0, 0, 1, 0]
pos1 = [0, 0, 2, 1]
dir1 = [0, 0, -1]
dif_c1 = [1, 1, 0.5, 0]
amb_c0 = [1, 1, 1, 0]
dif_c0 = [0.2, 0.2, 0.2, 0]
box = [(-1, 1), (-1, 1), (-1, 1)]
collider = None
cutoff = 20
exp = 50
tex = None
tex_coord = None


def calc_trang_normal(p1, p2, p3):
    v1 = (p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])
    v2 = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
    return (v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0])


def v3minus(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])


def round3(v, n):
    return round(v[0], n), round(v[1], n), round(v[2], n)


def loadTexture(fileName):
    glEnable(GL_TEXTURE_2D)
    image = Image.open(fileName)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGBA").tobytes()
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    return texture


def calc():
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
    normals = []
    ellipse = []
    collider = []
    tex_coord = []
    for t in range(8):
        collider.append(((radius + ellipse_param) / radius * x(t) * scale,
                         (radius + ellipse_param) / radius * y(t) * scale,
                          -scale))
        collider.append(((radius + ellipse_param) / radius * x(t) * scale,
                         (radius + ellipse_param) / radius * y(t) * scale,
                         1 * (t_param + 1) * scale))

    for i in range(vertex_lenght_count):
        ellipse.append(np.array([math.cos(2 * math.pi * i / vertex_lenght_count) * ellipse_param,
                                 math.sin(2 * math.pi * i / vertex_lenght_count), 0]))
    ellipse.append(np.array([ellipse_param, 0, 0]))
    t = 0
    delta_t_param = 1 / vertex_height_count
    align = 0  # параметр выравнивания t по целым числам
    tmp = None
    last_center = None
    is_first_point = True
    prev_t = t
    last_el = None
    while t <= t_param:
        align += 1
        pos = np.array([x(t), y(t), z(t)])
        cur_pos = list(pos)
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
            for i in range(vertex_lenght_count):
                cur_p = list(trans_matrix.dot(ellipse[i]) + pos)
                next_p = list(trans_matrix.dot(ellipse[i + 1]) + pos)
                if i == 0:
                    if is_first_point:
                        is_first_point = False
                        last_el = round3(v3minus(cur_p, cur_pos), 3), (t / t_param, 0)
                        # normals.append(round3(v3minus(tmp[i], last_center), 3))
                        # tex_coord.append((prev_t / t_param, 0))
                    quads_poly.append(tmp[i])
                    quads_poly.append(cur_p)
                    normals.append(round3(v3minus(tmp[i], last_center), 3))
                    normals.append(round3(v3minus(cur_p, cur_pos), 3))
                    tex_coord.append((prev_t / t_param, 0))
                    tex_coord.append((t / t_param, 0))
                quads_poly.append(tmp[i + 1])
                quads_poly.append(next_p)
                normals.append(round3(v3minus(tmp[i + 1], last_center), 3))
                normals.append(round3(v3minus(next_p, cur_pos), 3))
                tex_coord.append((prev_t / t_param, (i + 1) / vertex_lenght_count))
                tex_coord.append((t / t_param, (i + 1) / vertex_lenght_count))

        tmp = []
        for i in range(vertex_lenght_count):
            tmp.append(list(trans_matrix.dot(ellipse[i]) + pos))
        tmp.append(list(trans_matrix.dot(ellipse[0]) + pos))
        last_center = list(pos)
        prev_t = t
        t += delta_t_param
        if align == vertex_height_count:
            align = 0
            t = int_r(t)
    normals.append(last_el[0])
    tex_coord.append(last_el[1])
    return quads_poly, normals, collider, tex_coord


def mainbox():
    global changes
    global figure, normals, collider, tex_coord
    glMultMatrixd([1, 0, 0, 0,
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   xpos, ypos, zpos, 1])
    glMultMatrixd([scale * xscale, 0, 0, 0,  # back center + scale
                   0, scale * yscale, 0, 0,
                   0, 0, scale * zscale, 0,
                   0, 0, 0, 1])
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
                   0, 0, 0, 1])
    if changes:
        changes = False
        figure, normals, collider, tex_coord = calc()
    glColor(0, 0.4, 0.4)
    if texmode:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    for k in range(t_param * vertex_height_count):
        glBegin(GL_TRIANGLE_STRIP)
        for n in range(k * 2 * (vertex_lenght_count + 1), (k + 1) * 2 * (vertex_lenght_count + 1)):
            glVertex3f(figure[n][0], figure[n][1], figure[n][2])
            glNormal(normals[n + 1][0], normals[n + 1][1], normals[n + 1][2])
            glTexCoord2f(tex_coord[n + 1][0], tex_coord[n + 1][1])
        glEnd()
    if texmode:
        glDisable(GL_TEXTURE_2D)
        glColor(0, 0.4, 0.4)


    # write collider
    # glBegin(GL_LINE_STRIP)
    # for n in collider:
    #     glVertex3f(n[0] / scale, n[1] / scale, n[2] / scale)
    # glEnd()

    # write normals
    # glBegin(GL_LINES)
    # for n in range(len(figure)):
    #     glVertex3f(figure[n][0], figure[n][1], figure[n][2])
    #     glVertex3f(figure[n][0] + normals[n][0], figure[n][1] + normals[n][1], figure[n][2] + normals[n][2])
    # glEnd()


def ortograph():
    glViewport(0, 0, size_x, size_y)
    glLoadIdentity()
    glMultMatrixd([0.87, 0, 1, 0.5,  # double point perspective
                   0, 1, 0, 0,
                   0.5, 0, -1.73, -0.87,
                   0, 0, 1, 2])
    glMultMatrixd([1, 0, 0, 0,
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   world_xpos, world_ypos, world_zpos, 1])
    oxtr, oytr, oztr = world_oxtr, world_oytr, world_oztr
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
    glLightfv(GL_LIGHT0, GL_DIFFUSE, dif_c0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, amb_c0)
    glLightfv(GL_LIGHT0, GL_POSITION, pos0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, dif_c1)
    glLightfv(GL_LIGHT1, GL_POSITION, pos1)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, dir1)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, cutoff)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, exp)
    print('cutoff', cutoff, 'exp', exp)
    draw_box()
    mainbox()


def load():
    global xpos, ypos, zpos, vx, vy, vz, oxtr, oytr, oztr, world_xpos, world_ypos, world_zpos, \
        world_oxtr, world_oytr, world_oztr, world_change, move, cutoff, exp
    file = open('data.txt', 'r')
    data = file.read()
    file.close()
    d = json.loads(data)
    xpos, ypos, zpos = d['xpos'], d['ypos'], d['zpos']
    vx, vy, vz = d['vx'], d['vy'], d['vz']
    oxtr, oytr, oztr = d['oxtr'], d['oytr'], d['oztr']
    world_xpos, world_ypos, world_zpos = d['world_xpos'], d['world_ypos'], d['world_zpos']
    world_oxtr, world_oytr, world_oztr = d['world_oxtr'], d['world_oytr'], d['world_oztr']
    world_change = d['world_change']
    move = d['move']
    cutoff = d['cutoff']
    exp = d['exp']


def save():
    print(234)
    data = {
        'xpos': xpos,
        'ypos': ypos,
        'zpos': zpos,
        'vx': vx,
        'vy': vy,
        'vz': vz,
        'oxtr': oxtr,
        'oytr': oytr,
        'oztr': oztr,
        'world_xpos': world_xpos,
        'world_ypos': world_ypos,
        'world_zpos': world_zpos,
        'world_oxtr': world_oxtr,
        'world_oytr': world_oytr,
        'world_oztr': world_oztr,
        'world_change': world_change,
        'move': move,
        'cutoff': cutoff,
        'exp': exp
    }
    file = open('data.txt', 'w')
    file.write(json.dumps(data))
    file.close()


def moveevent(window, key, scancode, action, mods):
    global scale, colormode, world_xpos, world_ypos, world_zpos, cutoff, exp,\
        oxtr, oytr, oztr, move, vx, vy, vz, world_oxtr, world_oytr, world_oztr, \
        world_change, xpos, ypos, zpos, texmode
    if chr(key) == 'Z':
        cutoff += dt * 10
    if chr(key) == 'X':
        cutoff -= dt * 10
    if chr(key) == 'C':
        exp += dt * 100
    if chr(key) == 'V':
        exp -= dt * 100
    if chr(key) == 'Q' and world_change:
        world_xpos += dt
    if chr(key) == 'A' and world_change:
        world_xpos -= dt
    if chr(key) == 'W' and world_change:
        world_ypos += dt
    if chr(key) == 'S' and world_change:
        world_ypos -= dt
    if chr(key) == 'E' and world_change:
        world_zpos += dt
    if chr(key) == 'D' and world_change:
        world_zpos -= dt
    if chr(key) == 'Q' and not world_change:
        xpos += dt
    if chr(key) == 'A' and not world_change:
        xpos -= dt
    if chr(key) == 'W' and not world_change:
        ypos += dt
    if chr(key) == 'S' and not world_change:
        ypos -= dt
    if chr(key) == 'E' and not world_change:
        zpos += dt
    if chr(key) == 'D' and not world_change:
        zpos -= dt
    if chr(key) == 'R' and world_change:
        world_oxtr += dt
    if chr(key) == 'F' and world_change:
        world_oxtr -= dt
    if chr(key) == 'T' and world_change:
        world_oytr += dt
    if chr(key) == 'G' and world_change:
        world_oytr -= dt
    if chr(key) == 'Y' and world_change:
        world_oztr += dt
    if chr(key) == 'H' and world_change:
        world_oztr -= dt
    if chr(key) == 'R' and not world_change:
        oxtr += dt
    if chr(key) == 'F' and not world_change:
        oxtr -= dt
    if chr(key) == 'T' and not world_change:
        oytr += dt
    if chr(key) == 'G' and not world_change:
        oytr -= dt
    if chr(key) == 'Y' and not world_change:
        oztr += dt
    if chr(key) == 'H' and not world_change:
        oztr -= dt
    if chr(key) == 'B' and action == 1:
        move = not move
    if chr(key) == 'N' and action == 1:
        world_change = not world_change
    if chr(key) == 'U':
        vx += dt
    if chr(key) == 'J':
        vx -= dt
    if chr(key) == 'I':
        vy += dt
    if chr(key) == 'K':
        vy -= dt
    if chr(key) == 'O':
        vz += dt
    if chr(key) == 'L':
        vz -= dt
    if chr(key) == 'M' and action == 1:
        save()
    if chr(key) == ',' and action == 1:
        load()
    if chr(key) =='.' and action == 1:
        texmode = not texmode
    print(chr(key))

    if cutoff > 90:
        cutoff = 90
    if cutoff < 0:
        cutoff = 0
    if exp > 128:
        exp = 128
    if exp < 0:
        exp = 0


def movement():
    if not move:
        return
    global xpos, ypos, zpos, vx, vy, vz
    xpos += vx * dt
    ypos += vy * dt
    zpos += vz * dt
    tr_z = np.array([[math.cos(oztr), -math.sin(oztr), 0],
                [math.sin(oztr), math.cos(oztr), 0],
                [0, 0, 1]])
    tr_y = np.array([[math.cos(oytr), 0, -math.sin(oytr)],
                [0, 1, 0],
                [math.sin(oytr), 0, math.cos(oytr)]])
    tr_x = np.array([[1, 0, 0],
                [0, math.cos(oxtr), math.sin(oxtr)],
                [0, -math.sin(oxtr), math.cos(oxtr)]])
    trans_matrix = tr_z.dot(tr_y.dot(tr_x))
    for c_raw in collider:
        c = list(trans_matrix.dot(c_raw))
        if xpos + c[0] > box[0][1]:
            vx = - math.fabs(vx)
        if xpos + c[0] < box[0][0]:
            vx = math.fabs(vx)
        if ypos + c[1] > box[1][1]:
            vy = - math.fabs(vy)
        if ypos + c[1] < box[1][0]:
            vy = math.fabs(vy)
        if zpos + c[2] > box[2][1]:
            vz = - math.fabs(vz)
        if zpos + c[2] < box[2][0]:
            vz = math.fabs(vz)


def draw_box():
    glBegin(GL_QUADS)
    glColor(0.5,0,0)
    glVertex3f(box[0][0], box[1][0], box[2][0])
    glVertex3f(box[0][1], box[1][0], box[2][0])
    glVertex3f(box[0][1], box[1][0], box[2][1])
    glVertex3f(box[0][0], box[1][0], box[2][1])

    glColor(0,0,0.5)
    glVertex3f(box[0][0], box[1][0], box[2][0])
    glVertex3f(box[0][0], box[1][1], box[2][0])
    glVertex3f(box[0][1], box[1][1], box[2][0])
    glVertex3f(box[0][1], box[1][0], box[2][0])

    glColor(0,0.5,0)
    glVertex3f(box[0][1], box[1][0], box[2][0])
    glVertex3f(box[0][1], box[1][0], box[2][1])
    glVertex3f(box[0][1], box[1][1], box[2][1])
    glVertex3f(box[0][1], box[1][1], box[2][0])
    glEnd()
    glBegin(GL_LINES)
    glColor(0,0,0)
    glVertex3f(box[0][0], box[1][1], box[2][1])
    glVertex3f(box[0][1], box[1][1], box[2][1])
    glVertex3f(box[0][0], box[1][1], box[2][1])
    glVertex3f(box[0][0], box[1][0], box[2][1])
    glVertex3f(box[0][0], box[1][1], box[2][1])
    glVertex3f(box[0][0], box[1][1], box[2][0])
    glEnd()


def init_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
    glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.5, 0.5, 0.5, 1))
    glMaterialfv(GL_FRONT, GL_AMBIENT, (1, 1, 1))
    glMaterialfv(GL_FRONT, GL_SHININESS, (0.7, 0.7, 0.7))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.3, 0.3, 0.3))


size_x, size_y = 1000, 1000


def main():
    global dt, tex
    if not glfw.init():
        return
    window = glfw.create_window(size_x, size_y, "lab", None, None)
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

    init_light()
    tex = loadTexture('C:/Users/ilya/PycharmProjects/graphLabs/tex.bmp')

    cur_time = time.time()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ortograph()
        movement()
        glfw.swap_buffers(window)
        glfw.poll_events()
        new_time = time.time()
        dt = new_time - cur_time
        # print(zpos)
        cur_time = new_time

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
