# горизонтальная изометрия
import ctypes
import numpy
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet


try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True, )
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)
glClearColor(0, 0, 0, 1)
colors = [[0.17, 0.01, 0.04], [0.2, 0, 0.22], [0.01, 0.06, 0.17], [0, 0.22, 0.2], [0.1, 0.15, 0.7], [1, 1, 1]]
vertex = [[[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [0.1, -0.1, -0.1], [0.1, -0.1, 0.1]],
          [[-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, -0.1, -0.1]],
          [[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [-0.1, 0.1, 0.1]],
          [[0.1, -0.1, 0.1], [0.1, -0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1]],
          [[-0.1, 0.1, 0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1]],
          [[-0.1, -0.1, 0.1], [-0.1, 0.1, 0.1], [0.1, 0.1, 0.1], [0.1, -0.1, 0.1]]]

vertex2 = [[-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [0.1, -0.1, -0.1], [0.1, -0.1, 0.1],
          [-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, -0.1, -0.1],
          [-0.1, -0.1, 0.1], [-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [-0.1, 0.1, 0.1],
          [0.1, -0.1, 0.1], [0.1, -0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1],
          [-0.1, 0.1, 0.1], [-0.1, 0.1, -0.1], [0.1, 0.1, -0.1], [0.1, 0.1, 0.1],
          [-0.1, -0.1, 0.1], [-0.1, 0.1, 0.1], [0.1, 0.1, 0.1], [0.1, -0.1, 0.1]]

pos = [0, -0.6, 0]
fi = [0, 0, 0]
k = 0.1
n = 8
mat = 0
light = False
cyanPlastic = False
chrome = False
pearl = False
shine = False
vC = []
coord = []
cubeModeSec = GL_FILL
polygMass = []
show_tex = False
startM = False


class Point:
    def __init__(self, piskCoords, normCoords, texCoords):
        self.piskCoords = piskCoords
        self.normCoords = normCoords
        self.texCoords = texCoords


class Polygon:
    def __init__(self, points):
        self.massPoints = points


class Antiprizm:
    def __init__(self, nl):
        self.nl = n
        turnAngle = pi / nl
        for i in range(nl):
            topX1 = cos(2 * pi * i / nl)
            topZ1 = sin(2 * pi * i / nl)
            topX2 = cos(2 * pi * (i + 1) / nl)
            topZ2 = sin(2 * pi * (i + 1) / nl)
            botX1 = topX1 * cos(turnAngle) - topZ1 * sin(turnAngle)
            botZ1 = topX1 * sin(turnAngle) + topZ1 * cos(turnAngle)
            botX2 = topX2 * cos(turnAngle) - topZ2 * sin(turnAngle)
            botZ2 = topX2 * sin(turnAngle) + topZ2 * cos(turnAngle)
            norm1 = normalize(topZ2 - topZ1, (sqrt(botZ1 ** 2 + botX1 ** 2) - sqrt(
                (topX1 + (topX2 - topX1) / 2) ** 2 + (topZ1 + (topZ2 - topZ1) / 2) ** 2)), topX1 - topX2)
            norm2 = normalize(botZ2 - botZ1, (sqrt((botX1 + (botX2 - botX1) / 2) ** 2 + (botZ1 + (botZ2 - botZ1) / 2) ** 2) - sqrt(
                    topZ2 ** 2 + topX2 ** 2)), botX1 - botX2)
            polygt = Polygon([Point([topX1, 0.5, topZ1], [0, 1, 0], [topX1, topZ1]), Point([0, 0.5, 0], [0, 1, 0], [0, 0]),
                Point([topX2, 0.5, topZ2], [0, 1, 0], [topX2, topZ2])])
            polygb = Polygon([Point([botX2, -0.5, botZ2], [0, -1, 0], [topX1, topZ1]), Point([0, -0.5, 0], [0, -1, 0], [0, 0]),
                 Point([botX1, -0.5, botZ1], [0, -1, 0], [topX2, topZ2])])
            polyg1s = Polygon(
                [Point([topX1, 0.5, topZ1], norm1, [i / nl, 1]), Point([topX2, 0.5, topZ2], norm1, [(i + 1) / nl, 1]),
                 Point([botX1, -0.5, botZ1], norm1, [i / nl, 0])])
            polyg2s = Polygon([Point([topX2, 0.5, topZ2], norm2, [(i + 1) / nl, 1]),
                               Point([botX2, -0.5, botZ2], norm2, [(i + 1) / nl, 0]),
                               Point([botX1, -0.5, botZ1], norm2, [i / nl, 0])])
            polygMass.append(polygt)
            polygMass.append(polygb)
            polygMass.append(polyg1s)
            polygMass.append(polyg2s)
            vC.append([topX1, 0.5, topZ1])
            vC.append([topX2, 0.5, topZ2])
            vC.append([botX1, -0.5, botZ1])
            vC.append([botX2, -0.5, botZ2])
        self.vertttt = polygMass
        np_ar = numpy.array(vC)
        self.max_pr = numpy.amax(np_ar, axis=0)
        self.min_pr = numpy.amin(np_ar, axis=0)


    def draw(self, mode):
        global polygMass, vC
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslated(0 + pos[0], 0 + pos[1], 0 + pos[2])
        glRotated(fi[0], 1, 0, 0)
        glRotated(fi[1], 0, 1, 0)
        glRotated(fi[2], 0, 0, 1)
        glScaled(k, k, k)
        glPolygonMode(GL_FRONT_AND_BACK, mode)
        glBegin(GL_TRIANGLES)
        glColor3f(1, 1, 1)
        for i in self.vertttt:
            for point in i.massPoints:
                glNormal3f(*point.normCoords)
                glTexCoord2f(*point.texCoords)
                glVertex3f(*point.piskCoords)
        glEnd()
        polygMass = []
        vC = []
        glPopMatrix()

    def intersection_w_b(self):
        max_pr = self.max_pr
        min_pr = self.min_pr
        min_box = [-0.4, 0.1, -0.5]
        max_box = [0.4, 0.11, 0.5]
        for i in range(3):
            if pos[i] + max_pr[i] * k >= max_box[i]:
                speed_vec[i] *= -1
        for i in range(3):
            if pos[i] + min_pr[i] * k <= min_box[i]:
                speed_vec[i] *= -1


def draw_cube(mode, first, second, third, fourth, color):
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glEnd()


def normalize(x, y, z):
    leng = sqrt(x**2 + y**2 + z**2)
    new_coords = []
    x = x/leng
    y = y/leng
    z = z/leng
    new_coords.append(x)
    new_coords.append(y)
    new_coords.append(z)
    return new_coords


def coords_static_cube(painted):
    draw_cube(painted, vertex[0][0], vertex[0][1], vertex[0][2], vertex[0][3], colors[5])  # Bottom
    draw_cube(painted, vertex[1][0], vertex[1][1], vertex[1][2], vertex[1][3], colors[5])  # Back
    draw_cube(painted, vertex[2][0], vertex[2][1], vertex[2][2], vertex[2][3], colors[5])  # Left
    draw_cube(painted, vertex[3][0], vertex[3][1], vertex[3][2], vertex[3][3], colors[5])  # Right
    draw_cube(painted, vertex[4][0], vertex[4][1], vertex[4][2], vertex[4][3], colors[5])  # Top
    draw_cube(painted, vertex[5][0], vertex[5][1], vertex[5][2], vertex[5][3], colors[5])  # Front


def vec(*args):
    return (GLfloat * len(args))(*args)


def setup_light():
    glPushMatrix()
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, vec(1.5, 2, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, vec(0, 0, -1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(0.5, 0.5, 0.4))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.9, 0.9, 0.9))
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0.5, 0.5, 0.5))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec(0.2, 0.2, 0.2, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, vec(0.8, 0.8, 0.8, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(0, 0, 0, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128)
    if chrome:
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec(0.2125, 0.1275, 0.054, 0.2))
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, vec(0.714, 0.4284, 0.18144, 0.2))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(0.393548, 0.271906, 0.166721, 0.2))
        glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0.7, 1.5, 0.5, 1.0))
    elif cyanPlastic:
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec(0.0, 0.1, 0.06, 0.25))
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, vec(0.0, 0.50980392, 0.50980392, 0.25))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(0.50980392, 0.50196078, 0.50196078, 0.25))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1.1, 0.4, 0.3, 1.0))
    elif pearl:
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec(0.25, 0.20725, 0.20725, 0.088))
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, vec(1, 0.829, 0.829, 0.088))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(0.296648, 0.296648, 0.296648, 0.088))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1.0, 0.4, 0.2, 1.0))
    glPopMatrix()


textures = GLuint()


def load_textures():
    img = pyglet.image.load('textu (1).bmp')
    glGenTextures(1, ctypes.pointer(textures))
    glBindTexture(GL_TEXTURE_2D, textures)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    data = img._current_data
    glTexImage2D(GL_TEXTURE_2D, 0, 3, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glBindTexture(GL_TEXTURE_2D, 0)


def static_cube():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslated(0, -0.6, -0.0)
    glScaled(4, 5, 5)
    coords_static_cube(GL_LINE)
    glPopMatrix()


def settings():
    if show_tex:
        glEnable(GL_TEXTURE_2D)
    else: glDisable(GL_TEXTURE_2D)
    if light:
        glEnable(GL_LIGHTING)
    else: glDisable(GL_LIGHTING)


def projection():
    glMatrixMode(GL_PROJECTION)
    angle = -cos(pi / 4.0)
    m = (GLfloat * 16)(1, 0, 0, 0,
                       0, 1, 0, 0,
                       angle, angle, -1, 0,
                       0, 0, 0, 1)
    glLoadIdentity()
    glScaled(1, 1, 1)
    glOrtho(-1, 1, -1, 1, -1, 100)
    glLoadMatrixf(m)

@window.event
def on_draw():
    #window.clear()
    settings()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    if window.height > window.width:
        glViewport(0, 0, window.height, window.height)
    else:
        glViewport(0, 0, window.width, window.width)
    projection()
    setup_light()
    glBindTexture(GL_TEXTURE_2D, textures)
    antipr.draw(cubeModeSec)
    glBindTexture(GL_TEXTURE_2D, 0)
    static_cube()
    #0900save()


speed_vec = [0.01, 0.01, 0.01]


def update(dt):
    if startM:
        antipr.intersection_w_b()
        for i in range(3):
            pos[i] += speed_vec[i]


def save():
    global pos, fi, k
    file = open('load.txt', 'w')
    file.write(str(pos[0]) + '\n')
    file.write(str(pos[1]) + '\n')
    file.write(str(pos[2]) + '\n')
    file.write(str(fi[0]) + '\n')
    file.write(str(fi[1]) + '\n')
    file.write(str(fi[2]) + '\n')
    file.write(str(k) + '\n')
    file.write(str(show_tex) + '\n')
    file.write(str(light) + '\n')
    file.write(str(cyanPlastic) + '\n')
    file.write(str(pearl) + '\n')
    file.write(str(chrome) + '\n')
    file.write(str(startM) + '\n')


def open_file():
    global pos, show_tex, light, cyanPlastic, pearl, chrome, fi, k, startM
    file = open('load.txt', 'r')
    text = file.read()
    param = text.split('\n')
    pos = [float(param[0]), float(param[1]), float(param[2])]
    fi = [float(param[3]), float(param[4]), float(param[5])]
    k = float(param[6])
    if param[7] == 'True':
        show_tex = True
    else: show_tex = False
    if param[8] == 'True':
        light = True
    else: light = False
    if param[9] == 'True':
        cyanPlastic = True
    else: cyanPlastic = False
    if param[10] == 'True':
        pearl = True
    else: pearl = False
    if param[11] == 'True':
        chrome = True
    else: chrome = False
    if param[12] == 'True':
        startM = True
    else: startM = False


@window.event
def on_resize(width, height):
    glViewport(0, 0, height, width)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global cubeModeSec
    if button == mouse.LEFT:
        if cubeModeSec == GL_LINE:
            cubeModeSec = GL_FILL
        else:
            cubeModeSec = GL_LINE


@window.event
def on_key_press(symbol, modifiers):
    global k, n, light, show_tex, cyanPlastic, chrome, pearl, roll, pitch, yaw, startM, antipr
    if symbol == key.W:
        pos[1] += 0.1
    elif symbol == key.S:
        pos[1] -= 0.1
    elif symbol == key.Q:
        pos[2] -= 0.1
    elif symbol == key.E:
        pos[2] += 0.1
    elif symbol == key.A:
        pos[0] -= 0.1
    elif symbol == key.D:
        pos[0] += 0.1
    elif symbol == key.R:
        fi[0] += 5
    elif symbol == key.T:
        fi[0] -= 5
    elif symbol == key.F:
        fi[1] += 5
    elif symbol == key.G:
        fi[1] -= 5
    elif symbol == key.X:
        fi[2] += 5
    elif symbol == key.C:
        fi[2] -= 5
    elif symbol == key.UP:
        k += 0.1
    elif symbol == key.DOWN:
        k -= 0.1
    elif symbol == key.N:
        n += 1
        antipr = Antiprizm(n)
    elif symbol == key.M and n > 3:
        n -= 1
        antipr = Antiprizm(n)
    elif symbol == key.L:
        light = not light
    elif symbol == key._8:
        show_tex = not show_tex
    elif symbol == key._1:
        cyanPlastic = not cyanPlastic
    elif symbol == key._2:
        chrome = not chrome
    elif symbol == key._3:
        pearl = not pearl
    elif symbol == key.SPACE:
        startM = not startM
    elif symbol == key._0:
        save()
        print(pos)
    elif symbol == key._9:
        open_file()
        print(pos)
        antipr = Antiprizm(n)





load_textures()
antipr = Antiprizm(n)
pyglet.clock.schedule(update)
#open_file()
pyglet.app.run()