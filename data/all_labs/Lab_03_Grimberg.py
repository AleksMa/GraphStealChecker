import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from math import *

width1 = 800
height1 = 800

ALPHA = 0
BETA = 0
GAMMA = 0

points = [
    [0, 0, 0],
    [0.15, -0.1, 0],
    [0.3, 0.25, 0],
    [0.15, 0.2, 0],
    [0.2, 0.1, 0],
    [0.05, 0.35, 0],
    [-0.03, 0.1, 0],
    [-0.3, 0.4, 0]

]

l = 1
O = 45
mat = [1, 0, 0, 0,
       0, 1, 0, 0,
       -l * cos(O), -l * sin(O), -1, 0,
       0, 0, 0, 1]


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


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
        pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2) + pow(b[2] - a[2], 2)
    )
    return [((b[0] - a[0]) / len_xyz), ((b[1] - a[1]) / len_xyz), ((b[2] - a[2]) / len_xyz)]


def defaultCube():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(-12, -12, -4)

    glBegin(GL_QUADS)
    # 1
    glColor3ub(232, 68, 1)
    glVertex3f(0, 0, 0)
    glColor3ub(189, 245, 68)
    glVertex3f(1, 0, 0)
    glColor3ub(245, 197, 68)
    glVertex3f(1, 1, 0)
    glColor3ub(245, 68, 92)
    glVertex3f(0, 1, 0)

    # 2
    glColor3ub(6, 245, 138)
    glVertex3f(0, 0, 0)
    glColor3ub(36, 234, 89)
    glVertex3f(1, 0, 0)
    glColor3ub(234, 36, 36)
    glVertex3f(1, 0, 1)
    glColor3ub(36, 49, 234)
    glVertex3f(0, 0, 1)

    # 3
    glColor3ub(59, 100, 250)
    glVertex3f(1, 1, 0)
    glColor3ub(255, 140, 0)
    glVertex3f(0, 1, 0)
    glColor3ub(78, 95, 150)
    glVertex3f(0, 1, 1)
    glColor3ub(153, 190, 250)
    glVertex3f(1, 1, 1)

    # 4
    glColor3ub(59, 100, 250)
    glVertex3f(1, 0, 0)
    glColor3ub(255, 0, 0)
    glVertex3f(1, 1, 0)
    glColor3ub(234, 201, 36)
    glVertex3f(1, 1, 1)
    glColor3ub(36, 234, 132)
    glVertex3f(1, 0, 1)

    # 5
    glColor3ub(255, 255, 0)
    glVertex3f(0, 0, 0)
    glColor3ub(255, 155, 0)
    glVertex3f(0, 1, 0)
    glColor3ub(155, 255, 0)
    glVertex3f(0, 1, 1)
    glColor3ub(255, 255, 150)
    glVertex3f(0, 0, 1)

    # 6
    glColor3ub(10, 175, 246)
    glVertex3f(1, 0, 1)
    glColor3ub(204, 9, 248)
    glVertex3f(0, 0, 1)
    glColor3ub(244, 248, 9)
    glVertex3f(0, 1, 1)
    glColor3ub(248, 255, 150)
    glVertex3f(1, 1, 1)

    glEnd()
    glPopMatrix()


class Figure:

    def __init__(self, point):
        self.alpha = 0
        self.betta = 0
        self.gamma = 0
        self.size = len(point)
        self.points = point
        self.start_point = self.points[0]
        self.end_point = self.points[self.size - 1]
        self.xyz = get_n(self.start_point, self.end_point)
        self.angle_mode = 3
        self.mode = False
        self.scale = 10
        self.wire = self.func()

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

    def func(self):
        print("Cheeeb")
        wire = []
        for i in range(1, len(self.points) - 1):
            angle = 0
            rotate_points = []
            while angle <= 2 * pi:
                m = self.rotate(angle)  # !!!! peredelat` tak cto bi ne schital kuchu raz
                point = Point(self.points[i][0], self.points[i][1], self.points[i][2])
                rotate_points.append(mat_mult(m, point))
                angle += (2 * pi) / self.angle_mode
            wire.append(rotate_points)
        return wire

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMultMatrixd((GLdouble * len(mat))(*mat))
        glOrtho(-20, 20, -20, 20, -20, 20)

        glMatrixMode(GL_MODELVIEW)
        if self.mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(0, 0, -1)
        glScalef(40, 40, 40)
        glRotatef(self.alpha, 1, 0, 0)
        glRotatef(self.betta, 0, 1, 0)

        size = len(self.wire[0])
        for i in range(0, size - 1):
            glBegin(GL_TRIANGLES)
            glColor3ub(0, 255, 0)
            glVertex3d(self.start_point[0], self.start_point[1], self.start_point[2])
            glVertex3d(self.wire[0][i].x, self.wire[0][i].y, self.wire[0][i].z)
            glColor3ub(232, 68, 1)
            glVertex3d(self.wire[0][i + 1].x, self.wire[0][i + 1].y, self.wire[0][i + 1].z)
            glEnd()

        glBegin(GL_TRIANGLES)
        glColor3ub(0, 255, 0)
        glVertex3d(self.start_point[0], self.start_point[1], self.start_point[2])
        glColor3ub(232, 68, 1)
        glVertex3d(self.wire[0][0].x, self.wire[0][0].y, self.wire[0][0].z)
        glVertex3d(self.wire[0][size - 1].x, self.wire[0][size - 1].y, self.wire[0][size - 1].z)
        glEnd()

        size = len(self.wire[len(self.wire) - 1])

        for i in range(0, len(self.wire) - 1):
            wire_1 = self.wire[i]
            wire_2 = self.wire[i + 1]
            for j in range(0, len(wire_1) - 1):
                point_1_1 = wire_1[j]
                point_1_2 = wire_1[j + 1]
                point_2_1 = wire_2[j]
                point_2_2 = wire_2[j + 1]
                glBegin(GL_QUADS)
                glColor3d(0, 0, 255)
                glVertex3d(point_1_1.x, point_1_1.y, point_1_1.z)
                glColor3ub(255, 155, 0)
                glVertex3d(point_2_1.x, point_2_1.y, point_2_1.z)
                glColor3ub(255, 155, 143)
                glVertex3d(point_2_2.x, point_2_2.y, point_2_2.z)
                glColor3ub(200, 129, 67)
                glVertex3d(point_1_2.x, point_1_2.y, point_1_2.z)
                glEnd()

        for i in range(0, len(self.wire) - 1):
            wire_1 = self.wire[i]
            wire_2 = self.wire[i + 1]

            point_1_1 = wire_1[0]
            point_1_2 = wire_1[len(wire_1) - 1]
            point_2_1 = wire_2[0]
            point_2_2 = wire_2[len(wire_1) - 1]
            glBegin(GL_QUADS)
            glColor3d(0, 0, 255)
            glVertex3d(point_1_1.x, point_1_1.y, point_1_1.z)
            glColor3ub(255, 155, 0)
            glVertex3d(point_2_1.x, point_2_1.y, point_2_1.z)
            glColor3ub(255, 155, 143)
            glVertex3d(point_2_2.x, point_2_2.y, point_2_2.z)
            glColor3ub(200, 129, 67)
            glVertex3d(point_1_2.x, point_1_2.y, point_1_2.z)
            glEnd()

        for i in range(0, size - 1):
            glBegin(GL_TRIANGLES)
            glColor3ub(255, 0, 0)
            glVertex3d(self.end_point[0], self.end_point[1], self.end_point[2])
            glVertex3d(self.wire[len(self.wire) - 1][i].x, self.wire[len(self.wire) - 1][i].y,
                       self.wire[len(self.wire) - 1][i].z)
            glVertex3d(self.wire[len(self.wire) - 1][i + 1].x, self.wire[len(self.wire) - 1][i + 1].y,
                       self.wire[len(self.wire) - 1][i + 1].z)
            glEnd()

        glBegin(GL_TRIANGLES)
        glColor3ub(255, 0, 0)
        glVertex3d(self.end_point[0], self.end_point[1], self.end_point[2])
        glVertex3d(self.wire[len(self.wire) - 1][0].x, self.wire[len(self.wire) - 1][0].y,
                   self.wire[len(self.wire) - 1][0].z)
        glVertex3d(self.wire[len(self.wire) - 1][size - 1].x, self.wire[len(self.wire) - 1][size - 1].y,
                   self.wire[len(self.wire) - 1][size - 1].z)
        glEnd()

        glPopMatrix()


class RealWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(100, 100)
        self.set_maximum_size(1920, 1080)
        glClearColor(0, 0, 0, 0)
        self.Figure = Figure(points)

    def on_draw(self):
        self.clear()
        self.Figure.draw()
        defaultCube()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.Figure.alpha -= dy
        self.Figure.betta += dx

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.Figure.angle_mode += scroll_y
        if self.Figure.angle_mode <= 1:
            self.Figure.angle_mode = 1
        self.Figure.wire = self.Figure.func()

    def on_key_press(self, symbol, modifiers):
        self.Figure.mode = symbol == 119
        self.Figure.scale += int(symbol == 65362)
        self.Figure.scale -= int(symbol == 65364)


if __name__ == "__main__":
    window = RealWindow(width1, height1, "lab3", resizable=True)
    pyglet.app.run()
