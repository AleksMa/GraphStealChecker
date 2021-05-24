from math import sqrt, pi, cos, sin
from mathutils import Matrix
from pyglet import image
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from OpenGL.GLUT import *
from numpy import array, cross
import json


window = pyglet.window.Window(1400, 1400, resizable = True)
window.set_minimum_size(144, 144)
gl.glClearColor(0, 0.6, 0.8, 1)
glutInit()

Width = 1000
Height = 1000
ratio = 1
pos = array([0.0, 0.0, 0.0])
rot = [0, 0, 0]
isFramedMode = False
Horizontal = 5
Vertical = 7
Points = [[array([0.0, 0.0, 0.0]) for i in range(Vertical)] for j in range(Horizontal)]
heightOfParaboloid = 1
P = 0.25
Q = 0.5
Changed = False
border = array([[-0.4, -0.4, -0.4], [1.1, 1.1, 1.1]])
figure = array([[-0.2, -sqrt(0.5) / 5.0, 0.4], [0.2, sqrt(0.5) / 5.0, 0.6]])
chess = image.load("wood5.bmp")
texture = chess.get_texture()


# speed = 0.3 / 60
# vector = array([speed, speed, speed])
# coordx, coordy, coordz, is_infinity_light = 1, 1, 1, True
# type_of_light = GL_AMBIENT
# type_of_light = GL_DIFFUSE
# type_of_light = GL_SPECULAR
ambient_color = (GLfloat * 4)()
# ambient_color[0], ambient_color[1], ambient_color[2], ambient_color[3] = 0.2, 0.2, 0.2, 1
local_viewer = (GLfloat * 3)()
# local_viewer[0], local_viewer[1], local_viewer[2] = 0, 0, 2
two_side = (GLfloat * 1)()
# two_side[0] = 1
# face = GL_FRONT_AND_BACK
# face = GL_FRONT
# face = GL_BACK
# pname = GL_AMBIENT
# pname =  GL_DIFFUSE
# pname = GL_AMBIENT_AND_DIFFUSE
# pname = GL_SPECULAR
# pname = GL_EMISSION
# pname = GL_SHININESS
# parameters = (GLfloat * 4)()
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.2, 0.2, 0.2, 1.0
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.8, 0.8, 0.8, 1.0
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.0, 0.0, 0.0, 1.0
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.0, 0.0, 0.0, 1.0
# parameters = (GLfloat * 1)()
# parameters[0] = 10.0
speed, vector, coordx, coordy, coordz, is_infinity_light, face, is_local, is_animated, is_lighted, is_textured, is_material = None, None, None, None, None, None, None, None, None, None, None, None
ambient, diffuse, specular, shininess, emission = (GLfloat * 4)(), (GLfloat * 4)(), (GLfloat * 4)(), 0, (GLfloat * 4)()


def load():
    with open('data.txt') as json_file:
        global speed, vector, coordx, coordy, coordz, is_infinity_light, face, pname, ambient_color, local_viewer, two_side, parameters, is_local, is_animated, is_lighted, is_textured
        global ambient, diffuse, specular, shininess, emission, is_material
        result = json.load(json_file)
        is_textured = result['is_textured']
        is_lighted = result['is_lighted']
        is_animated = result['is_animated']
        speed = result['speed']
        vector = array([speed, speed, speed])
        coordx, coordy, coordz, is_infinity_light = result['light1'][0]['coordx'], result['light1'][0]['coordy'], \
                                                    result['light1'][0]['coordz'], result['light1'][0][
                                                        'is_infinity_light']
        ambient_color[0], ambient_color[1], ambient_color[2], ambient_color[3] = result['light3'][0]["ambient_color"][
                                                                                     0], \
                                                                                 result['light3'][0]["ambient_color"][
                                                                                     1], \
                                                                                 result['light3'][0]["ambient_color"][
                                                                                     2], \
                                                                                 result['light3'][0]["ambient_color"][3]
        is_local = result['light4'][0]["is_local"]
        local_viewer[0], local_viewer[1], local_viewer[2] = result['light4'][0]["local_viewer"][0], \
                                                            result['light4'][0]["local_viewer"][1], \
                                                            result['light4'][0]["local_viewer"][2]
        two_side[0] = result["light5"][0]["two_side"]
        face = result["light6"][0]['face']
        ambient[0], ambient[1], ambient[2], ambient[3] = result["ambient"][0], result["ambient"][1], result["ambient"][2], result["ambient"][3]
        diffuse[0], diffuse[1], diffuse[2], diffuse[3] = result["diffuse"][0], result["diffuse"][1], result["diffuse"][2], result["diffuse"][3]
        specular[0], specular[1], specular[2], specular[3] = result["specular"][0], result["specular"][1], result["specular"][2], result["specular"][3]
        shininess = result["shininess"]
        emission[0], emission[1], emission[2], emission[3] = result["emission"][0], result["emission"][1], result["emission"][2], result["emission"][3]
        is_material = result["is_material"]


def save():
    global speed, coordx, coordy, coordz, is_infinity_light, face, pname, ambient_color, local_viewer, two_side, parameters, is_local, is_animated, is_lighted, is_textured
    global ambient, diffuse, specular, shininess, emission, is_material
    data = {}

    data["is_textured"] = is_textured
    data['is_lighted'] = is_lighted
    data['is_animated'] = is_animated
    data['speed'] = speed
    data['light1'] = []
    data['light1'].append({
        'coordx': coordx,
        'coordy': coordy,
        'coordz': coordz,
        'is_infinity_light': is_infinity_light
    })
    data['light3'] = []
    data['light3'].append({
        'ambient_color': [ambient_color[0], ambient_color[1], ambient_color[2], ambient_color[3]]
    })
    data['light4'] = []
    data['light4'].append({
        'is_local': is_local,
        'local_viewer': [local_viewer[0], local_viewer[1], local_viewer[2]]
    })
    data['light5'] = []
    data['light5'].append({
        'two_side': two_side[0]
    })
    data['light6'] = []
    data['light6'].append({
        'face': face,
    })
    data["ambient"] = [] * 4
    data["ambient"][0], data["ambient"][1], data["ambient"][2], data["ambient"][3] = ambient[0], ambient[1], ambient[2], ambient[3]
    data["diffuse"] = [] * 4
    data["diffuse"][0], data["diffuse"][1], data["diffuse"][2], data["diffuse"][3] = diffuse[0], diffuse[1], diffuse[2], diffuse[3]
    data["specular"] = [] * 4
    data["specular"][0], data["specular"][1], data["specular"][2], data["specular"][3] = specular[0], specular[1], specular[2], specular[3]
    data["shininess"] = shininess
    data["emission"] = [] * 4
    data["emission"][0], data["emission"][1], data["emission"][2], data["emission"][3] = emission[0], emission[1], emission[2], emission[3]
    data["is_material"] = is_material
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


load()


def which(first, second, third, fourth):
    glBegin(GL_LINE_LOOP)
    glColor3f(0, 0, 0)
    glVertex3f(*first)
    glVertex3f(*second)
    glVertex3f(*third)
    glVertex3f(*fourth)
    glEnd()


def baseCube():
    lbf = [-0.5, -0.5, -0.5]
    rbf = [0.5, -0.5, -0.5]
    rtf = [0.5, 0.5, -0.5]
    ltf = [-0.5, 0.5, -0.5]

    lbn = [-0.5, -0.5, 0.5]
    rbn = [0.5, -0.5, 0.5]
    rtn = [0.5, 0.5, 0.5]
    ltn = [-0.5, 0.5, 0.5]

    # BOTTOM
    which(lbn, rbn, rbf, lbf)

    # BACK
    which(lbf, rbf, rtf, ltf)

    # LEFT
    which(ltf, ltn, lbn, lbf)

    # RIGHT
    which(rtn, rtf, rbf, rbn)

    # TOP
    which(ltn, ltf, rtf, rtn)

    # FRONT
    which(lbn, ltn, rtn, rbn)


def sectorOfParaboloid(framed, i, j, top):
    global heightOfParaboloid, Vertical, Horizontal, Points

    # print(i, Vertical, j, Horizontal)
    if framed:
        glBegin(GL_LINE_LOOP)
        # glColor3f(0, 0, 0)
    else:
        glBegin(GL_POLYGON)
        # glColor3f(random(), random(), random())
        glColor3f(1, 1, 1)

    a = None
    b = None
    c = None
    d = None

    if not top:
        a = Points[i][j]
        if j + 1 == Vertical:
            b = Points[i][0]
        else:
            b = Points[i][j + 1]
        if i == 0:
            c = array([0, 0, 0])
            d = array([0, 0, 0])
        else:
            if j + 1 == Vertical:
                c = Points[i - 1][0]
            else:
                c = Points[i - 1][j + 1]
            d = Points[i - 1][j]
    else:
        a = Points[i][j]
        a[1] = heightOfParaboloid
        if i == 0:
            b = array([0, 0, 0])
            c = array([0, 0, 0])
            b[1] = heightOfParaboloid
            c[1] = heightOfParaboloid
        else:
            b = Points[i - 1][j]
            b[1] = heightOfParaboloid
            if j + 1 == Vertical:
                c = Points[i - 1][0]
                c[1] = heightOfParaboloid
            else:
                c = Points[i - 1][j + 1]
                c[1] = heightOfParaboloid
        if j + 1 == Vertical:
            d = Points[i][0]
            d[1] = heightOfParaboloid
        else:
            d = Points[i][j + 1]
            d[1] = heightOfParaboloid

    normal = cross(c - a, d - b)
    x = normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2
    if x != 1:
        length = sqrt(x) * 1.0
        if length > 0:
            normal[0] /= length
            normal[1] /= length
            normal[2] /= length
    glNormal3f(*normal)

    glTexCoord2f(i * 1.0 / Horizontal, j * 1.0 / Vertical)
    glVertex3f(*a)
    if not top:
        glTexCoord2f(i * 1.0 / Horizontal, (j + 1 % Vertical) * 1.0 / Vertical)
        glVertex3f(*b)
        if i == 0:
            glTexCoord2f((i - 1) * 1.0 / Horizontal, (j + 1 % Vertical) * 1.0 / Vertical)
            glVertex3f(*c)
        else:
            glTexCoord2f((i - 1) * 1.0 / Horizontal, (j + 1 % Vertical) * 1.0 / Vertical)
            glVertex3f(*c)
            glTexCoord2f((i - 1) * 1.0 / Horizontal, j * 1.0 / Vertical)
            glVertex3f(*d)
    else:
        if i == 0:
            glTexCoord2f((i - 1) * 1.0 / Horizontal, j * 1.0 / Vertical)
            glVertex3f(*b)
        else:
            glTexCoord2f((i - 1) * 1.0 / Horizontal, j * 1.0 / Vertical)
            glVertex3f(*b)

            glTexCoord2f((i - 1) * 1.0 / Horizontal, (j + 1 % Vertical) * 1.0 / Vertical)
            glVertex3f(*c)
        glTexCoord2f(i * 1.0 / Horizontal, (j + 1 % Vertical) * 1.0 / Vertical)
        glVertex3f(*d)

    glEnd()


def EllepticalParaboloid(framed):
    global Points, Horizontal, Vertical, heightOfParaboloid
    for i in range(Horizontal):
        for j in range(Vertical):
            sectorOfParaboloid(framed, i, j, False)

    for i in range(Horizontal):
        for j in range(Vertical):
            sectorOfParaboloid(framed, i, j, True)


def resetPoints(dt):
    global Points, P, Q, Vertical, Horizontal, heightOfParaboloid, vector, pos, border, figure, is_animated
    Points = [[array([0.0, 0.0, 0.0]) for i in range(Vertical)] for j in range(Horizontal)]
    stepy = float(heightOfParaboloid) / Horizontal
    anglexz = 2 * pi / Vertical
    curangle = 0
    h = 0.0

    for i in range(Horizontal):
        h += stepy
        for j in range(Vertical):
            Points[i][j][0] = sqrt(2 * Q * h) * cos(curangle)
            Points[i][j][1] = h
            Points[i][j][2] = sqrt(2 * P * h) * sin(curangle)
            curangle += anglexz

    if is_animated:
        if figure[0][0] > border[0][0] and figure[0][1] > border[0][1] and figure[0][2] > border[0][2] and figure[1][0] < border[1][0] and figure[1][1] < border[1][1] and figure[1][2] < border[1][2]:
            pos += vector
            figure += vector
        else:
            # print("-------\n", figure, "\n---\n", border, "\n---\n", vector, "\n-------")
            if figure[0][0] < border[0][0] or figure[1][0] > border[1][0]:
                vector[0] *= -1
            if figure[0][1] < border[0][1] or figure[1][1] > border[1][1]:
                vector[1] *= -1
            if figure[0][2] < border[0][2] or figure[1][2] > border[1][2]:
                vector[2] *= -1
            pos += vector
            figure += vector


@window.event
def on_draw():
    global Width, Height
    global ratio
    global isFramedMode, Changed
    global Horizontal, Vertical, heightOfParaboloid, P, Q
    global texture, chess
    global coordx, coordy, coordz, is_infinity_light, ambient_color, local_viewer, two_side, face, is_local, is_lighted, is_textured
    global ambient, diffuse, specular, shininess, emission, is_material
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    if not is_textured:
        glDisable(GL_TEXTURE_2D)

    if is_textured:
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, chess.width, chess.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     chess.get_data())
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_NORMALIZE)

    if not is_lighted:
        glDisable(GL_LIGHTING)

    if is_lighted:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        if not is_material:
            glEnable(GL_COLOR_MATERIAL)
        else:
            glDisable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glLightiv(GL_LIGHT0, GL_POSITION, (GLint * 4)(coordx, coordy, coordz, is_infinity_light))

        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat * 4)(0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 4)(0.2, 0.2, 0.2, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat * 4)(0.2, 0.2, 0.2, 1))

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_color)
        if is_local:
            glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, local_viewer)
        glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, two_side)

        if is_material:
            glMaterialfv(face, GL_AMBIENT, ambient)
            glMaterialfv(face, GL_DIFFUSE, diffuse)
            glMaterialfv(face, GL_SPECULAR, specular)
            glMaterialfv(face, GL_SHININESS, (GLfloat * 1)(shininess))
            glMaterialfv(face, GL_EMISSION, emission)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    # ------------------------------------------------------------

    cx = 3
    cy = 3
    cz = 3

    p = float(-1) / float(cx)
    q = float(-1) / float(cy)
    r = float(-1) / float(cz)

    matrixShift = Matrix([(1, 0, 0, 0),
                          (0, 1, 0, 0),
                          (0, 0, 1, 0),
                          (0.175, 0.175, 0.175, 1)])
    matrixRatio = Matrix([(1 / ratio, 0, 0, 0),
                          (0, 1, 0, 0),
                          (0, 0, 1, 0),
                          (0, 0, 0, 1)])
    matrixPerspective = Matrix([(1, 0, 0, p),
                                (0, 1, 0, q),
                                (0, 1, 0, r),
                                (0, 0, 0, 1)])
    matrixProjection = Matrix([(1, 0, 0, 0),
                               (0, 1, 0, 0),
                               (0, 0, 0, 0),
                               (0, 0, 0, 1)])
    matrixFinal = matrixProjection @ matrixPerspective @ matrixShift @ matrixRatio
    Matrix.transpose(matrixFinal)

    glMatrixMode(GL_PROJECTION)
    value = (GLfloat * 16)()
    for i in range(4):
        for j in range(4):
            value[i * 4 + j] = matrixFinal[i][j]
    glLoadMatrixf(value)

    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CW)

    glLoadIdentity()

    glPushMatrix()
    glScaled(1.5, 1.5, 1.5)
    glTranslated(0.35, 0.35, 0.35)
    glRotatef(30, 1, 0, 0)
    glRotatef(-30, 0, 1, 0)
    glRotatef(0, 0, 0, 1)
    baseCube()
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CW)

    glLoadIdentity()

    glPushMatrix()
    glScaled(0.2, 0.2, 0.2)
    glTranslated(*pos)
    glRotatef(rot[0], 1, 0, 0)
    glRotatef(rot[1], 0, 1, 0)
    glRotatef(rot[2], 0, 0, 1)
    EllepticalParaboloid(isFramedMode)
    Changed = False

    glPopMatrix()


@window.event
def on_resize(width, height):
    global ratio
    glViewport(0, 0, width, height)
    ratio = width / height
    resetPoints(0)


@window.event
def on_mouse_press(x, y, button, modifiers):
    resetPoints(0)

    global isFramedMode
    if button == mouse.LEFT:
        isFramedMode = not isFramedMode


@window.event
def on_key_press(symbol, modifiers):
    global pos, rot, Horizontal, Vertical, Changed
    global speed, vector, is_infinity_light, two_side, face, is_local, is_animated, is_lighted, is_textured, is_material
    if symbol == key.S:
        pos[1] -= 0.05
    elif symbol == key.W:
        pos[1] += 0.05
    elif symbol == key.D:
        pos[0] += 0.05
    elif symbol == key.A:
        pos[0] -= 0.05
    elif symbol == key.UP:
        pos[2] += 0.05
    elif symbol == key.DOWN:
        pos[2] -= 0.05

    elif symbol == key.Z:
        rot[0] -= 5
    elif symbol == key.X:
        rot[0] += 5
    elif symbol == key.C:
        rot[1] -= 5
    elif symbol == key.V:
        rot[1] += 5
    elif symbol == key.B:
        rot[2] -= 5
    elif symbol == key.N:
        rot[2] += 5

    elif symbol == key.O:
        Horizontal -= 1
    elif symbol == key.P:
        Horizontal += 1
    elif symbol == key.K:
        Vertical -= 1
    elif symbol == key.L:
        Vertical += 1

    elif symbol == key.Q:
        save()
    elif symbol == key.E:
        load()

    elif symbol == key.R:
        is_material = not is_material
    elif symbol == key.T:
        is_infinity_light = not is_infinity_light
    elif symbol == key.U:
        if two_side[0] == 0:
            two_side[0] = 1
        elif two_side[0] == 1:
            two_side[0] = 0
    elif symbol == key.I:
        if face == GL_FRONT_AND_BACK:
            face = GL_FRONT
        elif face == GL_FRONT:
            face = GL_BACK
        elif face == GL_BACK:
            face = GL_FRONT_AND_BACK
    elif symbol == key.H:
        is_local = not is_local
    elif symbol == key.G:
        is_animated = not is_animated
    elif symbol == key.F:
        is_lighted = not is_lighted
    elif symbol == key.M:
        is_textured = not is_textured

    resetPoints(0)


# speed = 0.3 / 60
# vector = array([speed, speed, speed])
# coordx, coordy, coordz, is_infinity_light = 1, 1, 1, True
# type_of_light = GL_AMBIENT
# type_of_light = GL_DIFFUSE
# type_of_light = GL_SPECULAR
# ambient_color = (GLfloat * 4)()
# ambient_color[0], ambient_color[1], ambient_color[2], ambient_color[3] = 0.2, 0.2, 0.2, 1
# local_viewer = (GLfloat * 3)()
# local_viewer[0], local_viewer[1], local_viewer[2] = 0, 0, 2
# two_side = (GLfloat * 1)()
# two_side[0] = 1
# face = GL_FRONT_AND_BACK
# face = GL_FRONT
# face = GL_BACK
# pname = GL_AMBIENT
# pname = GL_DIFFUSE
# pname = GL_SPECULAR
# pname = GL_EMISSION
# pname = GL_SHININESS
# parameters = (GLfloat * 4)()
# parameters[0], parameters[1], parameters[2], parameters[3] = 1.0, 0.0, 0.0, 1.0
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.8, 0.8, 0.8, 1.0
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.0, 0.0, 0.0, 1.0
# parameters[0], parameters[1], parameters[2], parameters[3] = 0.0, 0.0, 0.0, 1.0
# parameters = (GLfloat * 1)()
# parameters[0] = 10.0


resetPoints(0)
pyglet.clock.schedule_interval(resetPoints, 1.0 / 60)
pyglet.app.run()
