import pyglet
from pyglet.gl import *
from pyglet.window import mouse, FPSDisplay
from math import *
import pickle
import copy
from time import time


class Point:  # точка
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.normal = None
        self.count_normal = 0

    def addNormal(self, normal):  # добавление к точке нормали
        if self.normal is None:
            self.normal = normal
            self.count_normal += 1
        else:
            self.normal.x += normal.x
            self.normal.y += normal.y
            self.normal.z += normal.z
            self.count_normal += 1

    def getNormal(self):
        size = sqrt(self.normal.x ** 2 + self.normal.y ** 2 + self.normal.z ** 2)
        self.normal.x /= size
        self.normal.y /= size
        self.normal.z /= size
        n = [self.normal.x / self.count_normal, self.normal.y / self.count_normal, self.normal.z / self.count_normal]
        return n


points = []
point_animation = [Point(0, 0, 0)]


###################################
def f():
    R = 10
    t = pi / 2
    while t >= 0:
        x = R * cos(t)
        y = R * (sin(t) - 1)
        t -= pi / 30
        points.append(Point(x, y, 0))
    points.append(Point(1, -10, 0))
    points.append(Point(1, -20, 0))
    points.append(Point(0, -20, 0))
    size = len(points) - 2
    dy = 30 / size
    for i in range(size):
        point_animation.append(Point(10, -dy * i, 0))
    point_animation.append(Point(0, -(30 - dy), 0))


f()
print(len(points), "points")


########################################


class Texture:

    def __init__(self):
        self.texture = None

    def open_texture(self, name):
        self.texture = pyglet.image.load(name)
        self.load_texture()

    def load_texture(self):
        glBindTexture(self.texture.get_texture().target, self.texture.get_texture().id)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGBA,
                     self.texture.width,
                     self.texture.height,
                     0,
                     GL_RGBA,
                     GL_UNSIGNED_BYTE,
                     self.texture.get_image_data().get_data("RGBA", 4 * self.texture.width)
                     )
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)


def mat_mult(matrix, points):
    point = []
    point.append(points.x)
    point.append(points.y)
    point.append(points.z)
    new_point = []
    for i in range(3):
        elem = 0
        for j in range(3):
            elem += matrix[i][j] * point[j]
        new_point.append(elem)
    return Point(new_point[0], new_point[1], new_point[2])


def get_n(a, b):
    len_xyz = sqrt(
        (b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2
    )
    return [((b.x - a.x) / len_xyz), ((b.y - a.y) / len_xyz), ((b.z - a.z) / len_xyz)]


class TwiningAnimation:
    def __init__(self, startFigure, startPoint_old, endPoint_old, endFigure, startPoint_new, endPoint_new,
                 currentFigure):
        self.startFigure = copy.deepcopy(startFigure)

        self.endFigure = copy.deepcopy(endFigure)

        self.startPoint_old = copy.deepcopy(startPoint_old)

        self.endPoint_old = copy.deepcopy(endPoint_old)

        self.startPoint_new = copy.deepcopy(startPoint_new)

        self.endPoint_new = copy.deepcopy(endPoint_new)

        self.startpoint = copy.deepcopy(startPoint_old)

        self.endpoint = copy.deepcopy(endPoint_old)

        self.ptr_to_currentFigure = currentFigure

        self.t = 0

        self.reverse = True

        self.animation_on = False

    def changeVal(self, startFigure, startPoint_old, endPoint_old, endFigure, startPoint_new, endPoint_new,
                  currentFigure):
        self.startFigure = copy.deepcopy(startFigure)

        self.endFigure = copy.deepcopy(endFigure)

        self.startPoint_old = copy.deepcopy(startPoint_old)

        self.endPoint_old = copy.deepcopy(endPoint_old)

        self.startPoint_new = copy.deepcopy(startPoint_new)

        self.endPoint_new = copy.deepcopy(endPoint_new)

        self.startpoint = copy.deepcopy(startPoint_old)

        self.endpoint = copy.deepcopy(endPoint_old)

        self.ptr_to_currentFigure = currentFigure

    def startAnimation(self):
        self.animation_on = True

    def endAnimation(self):
        self.animation_on = False

    def B(self, t, p0, p1, p2, p3):
        x = ((1 - t) ** 3) * p0.x + p1.x * (3 * t * ((1 - t) ** 2)) + p2.x * (3 * (t ** 2) * (1 - t)) + (t ** 3) * p3.x
        y = ((1 - t) ** 3) * p0.y + p1.y * (3 * t * ((1 - t) ** 2)) + p2.y * (3 * (t ** 2) * (1 - t)) + (t ** 3) * p3.y
        z = ((1 - t) ** 3) * p0.z + p1.z * (3 * t * ((1 - t) ** 2)) + p2.z * (3 * (t ** 2) * (1 - t)) + (t ** 3) * p3.z
        return Point(x, y, z)

    def animationStartPoint(self, t, point_end):
        s1 = self.startpoint
        s2 = Point(s1.x + 0.1, s1.y + 0.1, s1.z)
        s3 = Point(s1.x + 0.2, s1.y + 0.1, s1.z)
        s4 = point_end
        s = self.B(t, s1, s2, s3, s4)
        self.ptr_to_currentFigure.start_point = s

    def animationEndPoint(self, t, point_end):
        s1 = self.endpoint
        s2 = Point(s1.x + 0.1, s1.y + 0.1, s1.z)
        s3 = Point(s1.x + 0.2, s1.y + 0.1, s1.z)
        s4 = point_end
        s = self.B(t, s1, s2, s3, s4)
        self.ptr_to_currentFigure.end_point = s

    def animation_wall(self, t, a_wire):
        for k in range(len(self.startFigure)):
            wire1 = self.startFigure[k]
            for j in range(len(wire1)):
                p1 = wire1[j]
                p2 = Point(p1.x + 0.1, p1.y + 0.1, p1.z)
                p3 = Point(p1.x + 0.2, p1.y + 0.1, p1.z)
                p4 = a_wire[k][j]
                self.ptr_to_currentFigure.wire[k][j] = self.B(t, p1, p2, p3, p4)

    def animation(self):
        if self.animation_on:
            self.animationStartPoint(self.t, self.startPoint_new)
            self.animationEndPoint(self.t, self.endPoint_new)
            self.animation_wall(self.t, self.endFigure)
            self.ptr_to_currentFigure.prepareVertex()
            if self.reverse:
                self.t += 0.01
            else:
                self.t -= 0.01
            if self.t >= 1 or self.t <= 0:
                self.reverse = not self.reverse

class FPS():

    def __init__(self, display):
        self.display = display
        self.width = display.width
        self.height = display.height
        self.time = 0
        self.timedelay = 0.1
        self.label = pyglet.text.Label('', x=self.width//2, y=self.height//2,
                                       font_size=24, bold=False,
                                       color=(0, 255, 0, 255))
        self.count = 0
        self.dt = 0
        self.FPS = ""

    def start(self):
        self.count += 1
        self.time = time()

    def end(self):
        self.dt += time() - self.time
        if self.count >= 100:
            self.showFPS(100 / self.dt, self.dt)
            self.dt = 0
            self.count = 0

    def showFPS(self, FPS, t):
        print("FPS : ", ceil(FPS), " ms :", (1000 * t))

class Figure:

    def __init__(self, point, w, h):
        # Model
        self.width = w
        self.height = h
        self.alpha = 0
        self.betta = 0
        self.gamma = 0
        self.size = len(point)
        self.points = point
        self.scale = 40
        self.start_point = self.points[0]
        self.end_point = self.points[self.size - 1]
        self.xyz = get_n(self.start_point, self.end_point)
        self.angle_mode = 30
        self.mode = False
        self.wire = self.makeWire()
        self.move = 0

        # Animation
        self.Animation = None
        self.t = 0

        # Light
        self.light_on = False
        self.light_pos = [500, 0, 500, 0]
        self.light_dir = [-1, 0, -1]
        self.ambient = [0.5, 0.5, 0.5, 1]
        self.diffuse = [0.7, 0.7, 0.7, 1]

        # ModelLight
        self.model_ambient = [0.3, 0.3, 0.3, 1]
        self.model_diffuse = [0.1, 0.1, 0.1, 1]
        self.model_specular = [0.25, 0.25, 0.25]
        self.model_shininess = 0.2

        # Texture
        self.texture = Texture()
        self.texture_name = "B:/21/" + "1234.bmp"
        self.texture.open_texture("B:/21/" + "1234.bmp")
        self.texture_on = False

        self.prepareVertex()
        print("wire: ", len(self.wire))

    def prepareNormal(self, p1, p2, p3, p4, mark):
        n = self.makeNormal(p1, p2, p3, mark)
        n = Point(n[0], n[1], n[2])
        p1.addNormal(n)
        p2.addNormal(n)
        p3.addNormal(n)
        p4.addNormal(n)

    def prepareVertex(self):
        size1 = len(self.wire[0])
        ######
        for k in range(0, size1 - 1):
            self.prepareNormal(self.start_point, self.wire[0][k], self.wire[0][k + 1], self.start_point, True)
        self.prepareNormal(self.start_point, self.wire[0][size1 - 1], self.wire[0][0], self.start_point, True)
        ######
        size2 = len(self.wire[len(self.wire) - 1])
        for k in range(0, len(self.wire) - 1):
            wire_1 = self.wire[k]
            wire_2 = self.wire[k + 1]
            for j in range(0, len(wire_1) - 1):
                point_1_1 = wire_1[j]
                point_1_2 = wire_1[j + 1]
                point_2_1 = wire_2[j]
                point_2_2 = wire_2[j + 1]
                self.prepareNormal(point_1_1, point_2_1, point_1_2, point_2_2, True)
        for k in range(0, len(self.wire) - 1):
            wire_1 = self.wire[k]
            wire_2 = self.wire[k + 1]
            point_1_1 = wire_1[0]
            point_1_2 = wire_1[len(wire_1) - 1]
            point_2_1 = wire_2[0]
            point_2_2 = wire_2[len(wire_1) - 1]
            self.prepareNormal(point_1_2, point_2_2, point_2_1, point_1_1, True)
        ######
        for k in range(0, size2 - 1):
            self.prepareNormal(self.end_point, self.wire[len(self.wire) - 1][k],
                               self.wire[len(self.wire) - 1][k + 1],
                               self.end_point,
                               False)
        self.prepareNormal(self.end_point,
                           self.wire[len(self.wire) - 1][size2 - 1],
                           self.wire[len(self.wire) - 1][0],
                           self.end_point,
                           False)

    def save(self):
        with open("data.pickle", "wb") as write_file:
            print("Saving")
            # Model
            pickle.dump(self.width, write_file)
            pickle.dump(self.height, write_file)
            pickle.dump(self.alpha, write_file)
            pickle.dump(self.betta, write_file)
            pickle.dump(self.gamma, write_file)
            pickle.dump(self.size, write_file)
            pickle.dump(self.points, write_file)
            pickle.dump(self.scale, write_file)
            pickle.dump(self.start_point, write_file)
            pickle.dump(self.end_point, write_file)
            pickle.dump(self.xyz, write_file)
            pickle.dump(self.angle_mode, write_file)
            pickle.dump(self.mode, write_file)
            pickle.dump(self.wire, write_file)
            pickle.dump(self.move, write_file)

            # Animation
            pickle.dump(self.Animation, write_file)
            pickle.dump(self.t, write_file)

            # light
            pickle.dump(self.light_on, write_file)
            pickle.dump(self.light_pos, write_file)
            pickle.dump(self.light_dir, write_file)
            pickle.dump(self.ambient, write_file)
            pickle.dump(self.diffuse, write_file)
            pickle.dump(self.spec, write_file)
            pickle.dump(self.specreflection, write_file)
            pickle.dump(self.light_fov, write_file)
            pickle.dump(self.exponent, write_file)

            # ModelLight
            pickle.dump(self.model_ambient, write_file)
            pickle.dump(self.model_diffuse, write_file)
            pickle.dump(self.model_specular, write_file)
            pickle.dump(self.model_shininess, write_file)

            # Texture
            pickle.dump(self.texture, write_file)
            pickle.dump(self.texture_name, write_file)
            pickle.dump(self.texture_on, write_file)
            print("Scene Saved!")

    def load(self):
        with open("data.pickle", "rb") as read_file:
            print("Load....")
            # Model
            self.width = pickle.load(read_file)
            self.height = pickle.load(read_file)
            self.alpha = pickle.load(read_file)
            self.betta = pickle.load(read_file)
            self.gamma = pickle.load(read_file)
            self.size = pickle.load(read_file)
            self.points = pickle.load(read_file)
            self.scale = pickle.load(read_file)
            self.start_point = pickle.load(read_file)
            self.end_point = pickle.load(read_file)
            self.xyz = pickle.load(read_file)
            self.angle_mode = pickle.load(read_file)
            self.mode = pickle.load(read_file)
            self.wire = pickle.load(read_file)
            self.move = pickle.load(read_file)

            # Animation
            self.Animation = pickle.load(read_file)
            self.t = pickle.load(read_file)

            # light
            self.light_on = pickle.load(read_file)
            self.light_pos = pickle.load(read_file)
            self.light_dir = pickle.load(read_file)
            self.ambient = pickle.load(read_file)
            self.diffuse = pickle.load(read_file)
            self.spec = pickle.load(read_file)
            self.specreflection = pickle.load(read_file)
            self.light_fov = pickle.load(read_file)
            self.exponent = pickle.load(read_file)

            # ModelLight
            self.model_ambient = pickle.load(read_file)
            self.model_diffuse = pickle.load(read_file)
            self.model_specular = pickle.load(read_file)
            self.model_shininess = pickle.load(read_file)

            # Texture
            self.texture = pickle.load(read_file)
            self.texture_name = pickle.load(read_file)
            self.texture_on = pickle.load(read_file)

            self.texture.open_texture(self.texture_name)
            print("Scene Load!")

    def rotate(self, angle):
        rotate = [[cos(angle) + (1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[0]),
                   (1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[1]) - float(self.xyz[2]) * sin(angle),
                   (1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[2]) + float(self.xyz[1]) * sin(angle)],
                  [(1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[1]) + float(self.xyz[2]) * sin(angle),
                   cos(angle) + (1.0 - cos(angle)) * float(self.xyz[1] * self.xyz[1]),
                   (1.0 - cos(angle)) * float(self.xyz[1] * self.xyz[2]) - float(self.xyz[0]) * sin(angle)],
                  [(1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[2]) - float(self.xyz[1]) * sin(angle),
                   (1.0 - cos(angle)) * float(self.xyz[1] * self.xyz[2]) + float(self.xyz[0]) * sin(angle),
                   cos(angle) + (1.0 - cos(angle)) * float(self.xyz[2] * self.xyz[2])]]
        return rotate

    def makeWire(self):
        wire = []
        count = 0
        for i in range(1, len(self.points) - 1):
            angle = 0
            rotate_points = []
            point = Point(self.points[i].x, self.points[i].y, self.points[i].z)
            while angle < 2 * pi:
                m = self.rotate(angle)  # !!!! peredelat` tak cto bi ne schital kuchu raz
                p_new = mat_mult(m, point)
                rotate_points.append(p_new)
                count += 1
                angle += (2 * pi) / self.angle_mode
            wire.append(rotate_points)
        return wire

    def scalMult(self, p1, p2):
        return (p1.x * p2.x + p1.y * p2.y + p1.z * p2.z) < 0

    def light(self):
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (4 * GLfloat)(*self.ambient))

        glLightfv(GL_LIGHT0, GL_DIFFUSE, (4 * GLfloat)(*self.diffuse))


        glLightfv(GL_LIGHT0, GL_POSITION, (4 * GLfloat)(*self.light_pos))

        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (3 * GLfloat)(*self.light_dir))


    def makeNormal(self, p1, p2, p3, mode):
        v1 = [p1.x - p2.x, p1.y - p2.y, p1.z - p2.z]
        v2 = [p3.x - p1.x, p3.y - p1.y, p3.z - p1.z]
        A = v1[1] * v2[2] - v1[2] * v2[1]
        B = v1[2] * v2[0] - v1[0] * v2[2]
        C = v1[0] * v2[1] - v1[1] * v2[0]
        sizeA = A * A
        sizeB = B * B
        sizeC = C * C
        size1 = sqrt(sizeA + sizeB + sizeC)
        if size1 == 0:
            size1 = 1
        # A /= size1
        # B /= size1
        # C /= size1
        # print(A, B, C)
        if mode:
            return [A, B, C]
        else:
            return [-A, -B, -C]

    def draw_lamp(self):
        x0 = self.light_pos[0]
        y0 = self.light_pos[1]
        z0 = self.light_pos[2]

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(x0, y0, z0)
        glColor3ub(255, 255, 255)
        glScalef(self.scale, self.scale, self.scale)
        glBegin(GL_QUADS)
        # 1
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(0, 1, 0)
        # 2
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0, 1)
        glVertex3f(0, 0, 1)

        # 3
        glVertex3f(1, 1, 0)
        glVertex3f(0, 1, 0)
        glVertex3f(0, 1, 1)
        glVertex3f(1, 1, 1)

        # 4
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 0, 1)

        # 5
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 0, 1)

        # 6
        glVertex3f(1, 0, 1)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 1, 1)
        glVertex3f(1, 1, 1)

        glEnd()
        glPopMatrix()

    def initialize(self):
        if self.light_on:
            glEnable(GL_LIGHTING)
            self.light()
        else:
            glDisable(GL_LIGHTING)

        if self.texture_on:
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)
        # glEnable(GL_CULL_FACE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.width, self.width, -self.height, self.height, -self.width, self.width)

        glMatrixMode(GL_MODELVIEW)
        if self.mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(self.move, 0, -10)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(self.alpha, 1, 0, 0)
        glRotatef(self.betta, 0, 1, 0)

    def draw2(self):
        self.initialize()
        for i in range(0, len(self.wire)):
            glColor3ub(255, 0, 0)
            for j in range(0, len(self.wire[i])):
                n = self.wire[i][j].getNormal()
                glBegin(GL_LINES)
                glVertex3d(self.wire[i][j].x, self.wire[i][j].y, self.wire[i][j].z)
                glVertex3d(self.wire[i][j].x + n[0], self.wire[i][j].y + n[1], self.wire[i][j].z + n[2])
                glEnd()
        glColor3ub(255, 255, 255)
        glPopMatrix()


    def draw(self):
        self.initialize()

        ############################################
        size1 = len(self.wire[0])
        for r in range(0, size1 - 1):
            glBegin(GL_QUADS)
            glNormal3fv((3 * GLfloat)(*self.start_point.getNormal()))
            glVertex3d(self.start_point.x, self.start_point.y, self.start_point.z)

            glNormal3fv((3 * GLfloat)(*self.wire[0][r].getNormal()))
            glVertex3d(self.wire[0][r].x, self.wire[0][r].y, self.wire[0][r].z)

            glNormal3fv((3 * GLfloat)(*self.wire[0][r + 1].getNormal()))
            glVertex3d(self.wire[0][r + 1].x, self.wire[0][r + 1].y, self.wire[0][r + 1].z)

            glNormal3fv((3 * GLfloat)(*self.start_point.getNormal()))
            glVertex3d(self.start_point.x, self.start_point.y, self.start_point.z)

            glEnd()
        glBegin(GL_QUADS)

        glNormal3fv((3 * GLfloat)(*self.start_point.getNormal()))
        glVertex3d(self.start_point.x, self.start_point.y, self.start_point.z)

        glNormal3fv((3 * GLfloat)(*self.wire[0][size1 - 1].getNormal()))
        glVertex3d(self.wire[0][size1 - 1].x, self.wire[0][size1 - 1].y, self.wire[0][size1 - 1].z)

        glNormal3fv((3 * GLfloat)(*self.wire[0][0].getNormal()))
        glVertex3d(self.wire[0][0].x, self.wire[0][0].y, self.wire[0][0].z)

        glNormal3fv((3 * GLfloat)(*self.start_point.getNormal()))
        glVertex3d(self.start_point.x, self.start_point.y, self.start_point.z)

        glEnd()
        ############################################

        size = len(self.wire[len(self.wire) - 1])
        # glColor3d(0, 0, 255)
        for r in range(0, len(self.wire) - 1):
            wire_1 = self.wire[r]
            wire_2 = self.wire[r + 1]
            for j in range(0, len(wire_1) - 1):
                point_1_1 = wire_1[j]
                point_1_2 = wire_1[j + 1]
                point_2_1 = wire_2[j]
                point_2_2 = wire_2[j + 1]
                glBegin(GL_QUADS)
                # 1_1, 2_1, 2_2, 1_2
                glNormal3fv((3 * GLfloat)(*point_1_1.getNormal()))
                glVertex3d(point_1_1.x, point_1_1.y, point_1_1.z)

                glNormal3fv((3 * GLfloat)(*point_2_1.getNormal()))
                glVertex3d(point_2_1.x, point_2_1.y, point_2_1.z)

                glNormal3fv((3 * GLfloat)(*point_2_2.getNormal()))

                glVertex3d(point_2_2.x, point_2_2.y, point_2_2.z)

                glNormal3fv((3 * GLfloat)(*point_1_2.getNormal()))
                glVertex3d(point_1_2.x, point_1_2.y, point_1_2.z)
                glEnd()
            point_1_1 = wire_1[len(wire_1) - 1]
            point_1_2 = wire_1[0]
            point_2_1 = wire_2[len(wire_2) - 1]
            point_2_2 = wire_2[0]
            glBegin(GL_QUADS)
            # 1_1, 2_1, 2_2, 1_2
            glNormal3fv((3 * GLfloat)(*point_1_1.getNormal()))
            glVertex3d(point_1_1.x, point_1_1.y, point_1_1.z)

            glNormal3fv((3 * GLfloat)(*point_2_1.getNormal()))
            glVertex3d(point_2_1.x, point_2_1.y, point_2_1.z)

            glNormal3fv((3 * GLfloat)(*point_2_2.getNormal()))

            glVertex3d(point_2_2.x, point_2_2.y, point_2_2.z)

            glNormal3fv((3 * GLfloat)(*point_1_2.getNormal()))
            glVertex3d(point_1_2.x, point_1_2.y, point_1_2.z)
            glEnd()

        # glColor3ub(255, 0, 0)
        ############################################

        for r in range(0, size - 1):
            glBegin(GL_QUADS)

            glNormal3fv((3 * GLfloat)(*self.wire[len(self.wire) - 1][r].getNormal()))
            glVertex3d(self.wire[len(self.wire) - 1][r].x, self.wire[len(self.wire) - 1][r].y,
                       self.wire[len(self.wire) - 1][r].z)

            glNormal3fv((3 * GLfloat)(*self.end_point.getNormal()))
            glVertex3d(self.end_point.x, self.end_point.y, self.end_point.z)

            glNormal3fv((3 * GLfloat)(*self.end_point.getNormal()))
            glVertex3d(self.end_point.x, self.end_point.y, self.end_point.z)

            glNormal3fv((3 * GLfloat)(*self.wire[len(self.wire) - 1][r + 1].getNormal()))

            glVertex3d(self.wire[len(self.wire) - 1][r + 1].x, self.wire[len(self.wire) - 1][r + 1].y,
                       self.wire[len(self.wire) - 1][r + 1].z)

            glEnd()

        glBegin(GL_QUADS)
        glNormal3fv((3 * GLfloat)(*self.wire[len(self.wire) - 1][size - 1].getNormal()))
        glVertex3d(self.wire[len(self.wire) - 1][size - 1].x, self.wire[len(self.wire) - 1][size - 1].y,
                   self.wire[len(self.wire) - 1][size - 1].z)

        glNormal3fv((3 * GLfloat)(*self.end_point.getNormal()))
        glVertex3d(self.end_point.x, self.end_point.y, self.end_point.z)

        glNormal3fv((3 * GLfloat)(*self.end_point.getNormal()))
        glVertex3d(self.end_point.x, self.end_point.y, self.end_point.z)

        glNormal3fv((3 * GLfloat)(*self.wire[len(self.wire) - 1][0].getNormal()))
        glVertex3d(self.wire[len(self.wire) - 1][0].x, self.wire[len(self.wire) - 1][0].y,
                   self.wire[len(self.wire) - 1][0].z)

        glEnd()
        ############################################
        glPopMatrix()




class RealWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_minimum_size(100, 100)

        self.set_maximum_size(1920, 1080)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_DEPTH_TEST)

        glClearColor(0, 0, 0, 0)

        self.Figure = Figure(points, self.width, self.height)

        self.Figure_animation = Figure(point_animation, self.width, self.height)

        self.Figure.Animation = TwiningAnimation(self.Figure.wire,
                                                 self.Figure.start_point,
                                                 self.Figure.end_point,
                                                 self.Figure_animation.wire,
                                                 self.Figure_animation.start_point,
                                                 self.Figure_animation.end_point,
                                                 self.Figure)

        self.FPS = FPS(self)

    def on_draw(self):
        self.clear()
        #self.FPS.start()
        self.Figure.draw()
        self.Figure.draw2()
        #elf.FPS.end()

    def update(self, dt):
        self.Figure.Animation.animation()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.Figure.alpha += dy
            self.Figure.betta += dx

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if not self.Figure.Animation.animation_on:
            self.Figure.angle_mode += scroll_y
            if self.Figure.angle_mode <= 3:
                self.Figure.angle_mode = 3

            self.Figure.wire = self.Figure.makeWire()
            self.Figure_animation.angle_mode = self.Figure.angle_mode
            self.Figure_animation.wire = self.Figure_animation.makeWire()
            self.Figure.start_point = self.Figure.points[0]
            self.Figure.end_point = self.Figure.points[len(self.Figure.points) - 1]
            self.Figure.Animation.changeVal(self.Figure.wire,
                                            self.Figure.start_point,
                                            self.Figure.end_point,
                                            self.Figure_animation.wire,
                                            self.Figure_animation.start_point,
                                            self.Figure_animation.end_point,
                                            self.Figure)
            self.Figure.prepareVertex()

    def on_key_press(self, symbol, modifiers):
        if symbol == 119:
            self.Figure.mode = not self.Figure.mode
        self.Figure.scale += int(symbol == 65362)
        self.Figure.scale -= int(symbol == 65364)
        if symbol == 108:  # L
            self.Figure.light_on = not self.Figure.light_on
        if symbol == 65361 and self.Figure.light_fov >= 5:
            self.Figure.light_fov -= 5
            self.Figure.light()
        if symbol == 65363 and self.Figure.light_fov <= 85:
            self.Figure.light_fov += 5
            self.Figure.light()
        if symbol == 65460:  # num4
            self.Figure.move -= 50
        if symbol == 65462:  # num6
            self.Figure.move += 50
        if symbol == 97:  # A
            self.Figure.Animation.startAnimation()
        if symbol == 122:  # Z
            self.Figure.Animation.endAnimation()
        if symbol == 65474:  # f5
            self.Figure.save()
        if symbol == 65478:  # f9
            self.Figure.load()
        if symbol == 116:  # T
            self.Figure.texture_on = not self.Figure.texture_on
        if symbol == 65464:
            self.Figure.exponent -= 1
            if self.Figure.exponent < 0:
                self.Figure.exponent = 0
        if symbol == 65458:
            self.Figure.exponent += 1


if __name__ == "__main__":
    window = RealWindow(800, 800, "lab3", resizable=True)
    pyglet.clock.schedule_interval(window.update, .1)
    pyglet.app.run()
