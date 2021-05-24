import pyglet
from pyglet.gl import *
from math import *
import os
import pickle

pos = [-150, 0, 250]
animation = False
first_b = False
texture = False
pos_prizme = [0, 0, 0]
status = False
delta = 178
side_polygon = 30
inside_polygon = 15
delta_b = 0
t_start = 0
v = -100
g = 10
cutoff = 90
cutoff_delta = 20


wind = pyglet.window.Window(height=700, width=700, resizable=True, vsync=False)
#wind.maximize()
z = 0.75
ux = 0
uz = 0
data = []
size = 1000
edge = 15
t = 0
dt = 0

def vector(a, b):
    data = [-(a[1] * b[2] - b[1] * a[2]),
            -(b[0] * a[2] - a[0] * b[2]),
            -(a[0] * b[1] - b[0] * a[1])]
    #print(a, b, data)
    return bev(data, sqrt(data[0] ** 2 + data[1] ** 2 + data[2] ** 2))

def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def bev(a, b):
    #print(a)
    return [a[0] / b, a[1] / b, a[2] / b]

spotlight = False
def make_prizme(ux, uz, n):
    global data, inside_polygon
    u = inside_polygon

    angle = radians(360 / n)
    data = [[] for i in range(u + 1)]
    for i in range(u + 1):
        data[i].append([ux * (u - i) / u, 0, uz * (u - i) / u])
    #print(data)
    for j in range(n):
        ux, uz = ux * cos(angle) - uz * sin(angle), ux * sin(angle) + uz * cos(angle)
        for i in range(u + 1):
            data[i].append([ux * (u - i) / u, 0, uz * (u - i) / u])
    #print(data)

make_prizme(delta, 0, edge)

def upd(delta):
    global t, dt
    dt = delta
    t += delta
up = False
def animate(dt):
    global v, g, t_start, delta_b, tb, pos, up
    #print(delta_b, v, t, t_start)
    if delta_b < -300:
        up = True
        v = -v
        t_start = t
    tb = t - t_start
    v -= g * dt
    if up:
        delta_b = -300 + tb * v - g * tb * tb / 2
    else:
        delta_b = tb * v - g * tb * tb / 2
    pos[1] = delta_b
def draw_cube(x, y, z, u):
    glBegin(GL_QUAD_STRIP)
    glNormal3fv((GLfloat*3)(*[0,1,0]))
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + u)
    glNormal3fv((GLfloat * 3)(*[-1, 0, 0]))
    glVertex3f(x + u, y, z)
    glVertex3f(x + u, y, z + u)
    glNormal3fv((GLfloat * 3)(*[0, -1, 0]))
    glVertex3f(x + u, y + u, z)
    glVertex3f(x + u, y + u, z + u)
    glNormal3fv((GLfloat * 3)(1, 0, 0))
    glVertex3f(x, y + u, z)
    glVertex3f(x, y + u, z + u)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + u)

    glEnd()
    glBegin(GL_QUAD_STRIP)
    glNormal3fv((GLfloat*3)(0, 0, 1))
    glVertex3f(x, y, z)
    glVertex3f(x + u, y, z)
    glVertex3f(x, y + u, z)
    glVertex3f(x + u, y + u, z)
    glEnd()

    glBegin(GL_QUAD_STRIP)
    glNormal3fv((GLfloat*3)(0, 0, -1))
    glVertex3f(x, y + u, z + u)
    glVertex3f(x + u, y + u, z + u)
    glVertex3f(x, y, z + u)
    glVertex3f(x + u, y, z + u)
    glEnd()
    glFlush()

def draw_prizme(dx, dy, dz, n, u):

    #glLoadIdentity()
    glTranslatef(*pos)
    glRotatef(pos_prizme[0], 1, 0, 0)
    glRotatef(pos_prizme[1], 0, 1, 0)
    glRotatef(pos_prizme[2], 0, 0, 1)

    if texture:
        for j in range(len(data) - 1):
            glBegin(GL_QUAD_STRIP)
            u = len(data)
            for i in range(n + 1):
                if i != n:
                    glNormal3f(*vector(sub(data[j][(i + 1) % n], data[j][i]), sub(data[j + 1][i], data[j][i]), ))
                i = i % n
                alpha = 2 * i * pi / (n)

                glTexCoord2f(0.5 * cos(alpha) * (u - j) / u + 0.5, 0.5 * sin(alpha) * (u - j) / u + 0.5)
                glVertex3d(*data[j][i])
                glTexCoord2f(0.5 * cos(alpha) * (u - j - 1) / u + 0.5, 0.5 * sin(alpha) * (u - j - 1) / u + 0.5)
                glVertex3d(*data[j + 1][i])
            glEnd()
        # glBegin(GL_POLYGON)
        # for i in range(n):
        #     glVertex3d(data[i][0] + dx, data[i][1] + dy, data[i][2] + dz)
        # glEnd()
        for i in range(1, u + 1):
            a, b = (i - 1) / u * 1, i / u * 1
            glBegin(GL_QUAD_STRIP)
            for j in range(n):
                a2, b2 = j / n * 2, (j + 1) / n * 2.5
                glTexCoord2d(a2, a)
                glVertex3d(data[0][j][0] + dx * (i - 1) / u, data[0][j][1] + dy * (i - 1) / u, data[0][j][2] + dz * (i - 1) / u)
                glTexCoord2d(a2, b)
                glVertex3d(data[0][j][0] + dx * i / u, data[0][j][1] + dy * i / u, data[0][j][2] + dz * i / u)
            glTexCoord2d(0, a)
            glVertex3d(data[0][0][0] + dx * (i - 1) / u, data[0][0][1] + dy * (i - 1) / u, data[0][0][2] + dz * (i - 1) / u)
            glTexCoord2d(0, b)
            glVertex3d(data[0][0][0] + dx * i / u, data[0][0][1] + dy * i / u, data[0][0][2] + dz * i / u)
            glEnd()

        for j in range(len(data) - 1):
            glBegin(GL_QUAD_STRIP)
            u = len(data)
            for i in range(n + 1):
                i = i % n
                alpha = 2 * i * pi / (n)
                if i != n:
                    glNormal3f(*vector(sub(data[j][(i + 1) % n], data[j][i]), sub(data[j + 1][i], data[j][i])))
                glTexCoord2f(0.5 * cos(alpha) * (u - j) / u + 0.5, 0.5 * sin(alpha) * (u - j) / u + 0.5)
                glVertex3d(data[j][i][0] + dx, data[j][i][1] + dy, data[j][i][2] + dz)
                glTexCoord2f(0.5 * cos(alpha) * (u - j - 1) / u + 0.5, 0.5 * sin(alpha) * (u - j  - 1) / u + 0.5)
                glVertex3d(data[j + 1][i][0] + dx, data[j + 1][i][1] + dy, data[j + 1][i][2] + dz)

            glEnd()
    else:
        for i in range(len(data) - 1):
            glBegin(GL_QUAD_STRIP)
            for j in range(n):
                glNormal3f(*[0, -1, 0]) #*vector(sub(data[i + 1][j], data[i][j]), sub(data[i][(j + 1) % n], data[i][j])))
                glVertex3f(*data[i][j])
                glVertex3f(*data[i + 1][j])

            glVertex3f(*data[i][0])
            glVertex3f(*data[i + 1][0])
            glEnd()
        # glBegin(GL_POLYGON)
        # for i in range(n):
        #     glVertex3d(data[i][0] + dx, data[i][1] + dy, data[i][2] + dz)
        # glEnd()
        for i in range(1, u + 1):
            a, b = (i - 1) / u * 1, i / u * 1
            glBegin(GL_QUAD_STRIP)
            for j in range(n):
                a2, b2 = j / n, (j + 1) / n
                glNormal3f(*vector(sub(data[0][(j + 1) % n], data[0][j]), sub([data[0][j][0] + dx, data[0][j][1] + dy, data[0][j][2] + dz], data[0][j])))
                #print(*vector(sub(data[0][(j + 1) % n], data[0][j]), sub([data[0][j][0] + dx, data[0][j][1] + dy, data[0][j][2] + dz], data[0][j])))
                glVertex3f(data[0][j][0] + dx * (i - 1) / u, data[0][j][1] + dy * (i - 1) / u, data[0][j][2] + dz * (i - 1) / u)
                glVertex3f(data[0][j][0] + dx * i / u, data[0][j][1] + dy * i / u, data[0][j][2] + dz * i / u)
            glVertex3f(data[0][0][0] + dx * (i - 1) / u, data[0][0][1] + dy * (i - 1) / u, data[0][0][2] + dz * (i - 1) / u)
            glVertex3f(data[0][0][0] + dx * i / u, data[0][0][1] + dy * i / u, data[0][0][2] + dz * i / u)
            glEnd()
            # glBegin(GL_LINES)
            # for j in range(n):
            #     glVertex3d(*data[0][j])
            #     glVertex3d(*add(data[0][j], bev(vector(sub(data[0][(j + 1) % n], data[0][j]), sub([data[0][j][0] + dx, data[0][j][1] + dy, data[0][j][2] + dz], data[0][j])), 0.0030)))
            # glEnd()
        for i in range(len(data) - 1):
            glBegin(GL_QUAD_STRIP)
            for j in range(n):
                glNormal3f(*[0, 1, 0]) #(*vector(sub(data[i][(j + 1) % n], data[i][j]), sub(data[i + 1][j], data[i][j]))))
                glVertex3f(data[i][j][0] + dx, data[i][j][1] + dy, data[i][j][2] + dz)
                glVertex3f(data[i + 1][j][0] + dx, data[i + 1][j][1] + dy, data[i + 1][j][2] + dz)
            glVertex3f(data[i][0][0] + dx, data[i][0][1] + dy, data[i][0][2] + dz)
            glVertex3f(data[i + 1][0][0] + dx, data[i + 1][0][1] + dy, data[i + 1][0][2] + dz)
            glEnd()
    #glFlush()
class light(object):
    def __init__(self):
        global cutoff_delta, cutoff
        self.color_light = [0.1, 0, 0, 1]

        self.diffuse_light = [0, 0.4, 0.4, 1.0]
        self.position_light = [-50, 350.0, 250, 1.0]
        self.ambient_light = [0, 0.3, 0.1, 1.0]
        self.specular_light = [0, 0.1, 0.3, 1.0]

        self.spot_cutoff_light = cutoff
        self.spot_spot_exponent_light = cutoff_delta
        self.spot_direction_light = [0, -1.0, 0]

        self.diffuse_material = [1, 1, 1, 1.0]
        self.ambient_material = [0.2, 0.2, 0.2, 1.0]
        #self.emission_material = [0, 0.3, 0.2, 1.0]
        self.specular_material = [0, 1, 1, 1]
        self.shininess_material = 90

    def lightning(self):
        global spotlight
        glEnable(GL_LIGHTING)

        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        #glEnable(GL_LIGHT1)
        glEnable(GL_COLOR_MATERIAL)

        #glShadeModel(GL_SMOOTH)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (GLfloat * 4)(*self.color_light))

        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(*self.position_light))
        #glLightfv(GL_LIGHT1, GL_POSITION, (GLfloat * 4)(*self.position_light))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 4)(*self.diffuse_light))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat * 4)(*self.ambient_light))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(*self.specular_light))
        if spotlight:
            glLightfv(GL_LIGHT0,GL_SPOT_CUTOFF,(GLfloat)(self.spot_cutoff_light))
            glLightfv(GL_LIGHT0,GL_SPOT_EXPONENT,(GLfloat)(self.spot_spot_exponent_light))
            glLightfv(GL_LIGHT0,GL_SPOT_DIRECTION,(GLfloat * 3)(*self.spot_direction_light))
        else:
            glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, (GLfloat)(180))
            glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, (GLfloat)(0))
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (GLfloat * 3)(*self.spot_direction_light))
        glMaterialfv(GL_FRONT,GL_SHININESS,(GLfloat)(self.shininess_material))

        glMaterialfv(GL_FRONT, GL_DIFFUSE, (GLfloat * 4)(*self.diffuse_material))
        glMaterialfv(GL_FRONT, GL_AMBIENT, (GLfloat * 4)(*self.ambient_material))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (GLfloat * 4)(*self.specular_material))
        #glMaterialfv(GL_FRONT,GL_EMISSION,(GLfloat * 4)(*self.emission_material))

        #glColorMaterial(GL_FRONT_AND_BACK, GL_SPECULAR)
        #glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
        #glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT)

class Sav:
    def __init__(self, name="save.pickle"):
        self.name = name
    def save(self):
        global data, pos, pos, animation, first_b, texture, Light, pos_prizme, delta_b, t_start, v, g, cutoff, cutoff_delta
        with open(self.name, "wb") as file:
            pickle.dump(data, file)
            pickle.dump(pos, file)
            pickle.dump(animation, file)
            pickle.dump(first_b, file)
            pickle.dump(texture, file)
            pickle.dump(Light, file)
            pickle.dump(pos_prizme, file)
            pickle.dump(delta_b, file)
            pickle.dump(t_start, file)
            pickle.dump(v, file)
            pickle.dump(g, file)
            pickle.dump(cutoff, file)
            pickle.dump(cutoff_delta, file)
            pickle.dump(spotlight, file)


    def load(self):
        global data, pos, animation, first_b, texture, Light, pos_prizme, delta_b, t_start, v, g, cutoff, cutoff_delta, spotlight
        with open(self.name, "rb") as file:
            data = pickle.load(file)
            pos = pickle.load(file)
            animation = pickle.load(file)
            first_b = pickle.load(file)
            texture = pickle.load(file)
            Light = pickle.load(file)
            pos_prizme = pickle.load(file)
            delta_b = pickle.load(file)
            t_start = pickle.load(file)
            v = pickle.load(file)
            g = pickle.load(file)
            cutoff = pickle.load(file)
            cutoff_delta = pickle.load(file)
            print(data)
            spotlight = pickle.load(file)


image = pyglet.image.load(os.path.join(os.getcwd(),"3.bmp"))
tex = image.get_texture()
glBindTexture(tex.target,tex.id)

glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,
                     GL_RGBA,GL_UNSIGNED_BYTE,image.get_image_data().get_data("RGBA",image.width*4))

def tence(a, b):
    return
glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

Light = light()

save = Sav("data.pickle")
@wind.event
def on_draw():
    global pos, edge, t_start, first_b
    if texture:
        glEnable(tex.target)
    else:
        glDisable(tex.target)
    wind.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    # glPushMatrix()
    ux = degrees(asin(z / ((2) ** 0.5)))
    uz = degrees(asin(z / (2 - z ** 2) ** 0.5))
    #print(ux, uz)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glRotatef(-uz, 1, 0, 0)
    glRotatef(-ux, 0, 1, 0)
    glOrtho(-size, size, -size, size, -size, size)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glTranslatef(0, -400, 0)
    if True:
        Light = light()
        Light.lightning()
    draw_cube(*Light.position_light[:-1], 10)
    #draw_cube(0, 0, 0, 100)
    if animation:
        if first_b:
            t_start = t
            first_b = False
        animate(dt)
    draw_prizme(100, 100, 50, edge, side_polygon)


    #glRotatef(rot_y, 0, 1, 0)
    #draw_cube(0, 0, 0, 10)
    # glBegin(GL_POLYGON)
    # glVertex3f(-5,-5,0)
    # glVertex3f(5,-5,0)
    # glVertex3f(0,5,0)
    # glEnd()

    #glFlush()


@wind.event
def on_key_press(s,m):
    global pos, z, status, delta, data, edge, side_polygon, save, cutoff, cutoff_delta, spotlight
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
        global animation, first_b
        animation = not animation
        first_b = not first_b
    if s == pyglet.window.key._9:
        global texture
        texture = not texture
    if s == pyglet.window.key.Q:
        if (z <= 0.9):
            z += 0.1
    if s == pyglet.window.key.E and z >= 0.1:
        z -= 0.1
    if s == pyglet.window.key._1 and cutoff > 5:
        cutoff -= 5
    if s == pyglet.window.key._2 and cutoff < 90:
        cutoff += 5
    if s == pyglet.window.key._3 and cutoff_delta > 1:
        cutoff_delta -= 1
    if s == pyglet.window.key._4 and cutoff_delta < 100:
        print(cutoff, cutoff_delta)
        cutoff_delta += 1
    if s == pyglet.window.key._5:
        spotlight = not spotlight
    if s == pyglet.window.key.L:
        save.load()
    if s == pyglet.window.key.K:
        save.save()

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
    glLoadIdentity()

if __name__ == '__main__':
    pyglet.clock.schedule(func=upd)
    pyglet.app.run()
