import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from math import *
import copy


def vectMult(e1, e2):  # Векторное произведение
    return e1.x * e2.y - e1.y * e2.x > 0


def scalmult(p1, p2):
    return p1.x * p2.x + p1.y * p2.y


def len_vect(x, y):
    return sqrt(x ** 2 + y ** 2)


class Field:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.fields = [p3, p2, p1]
        self.start = 0
        self.end = 0

    def draw(self):
        glBegin(GL_LINE_STRIP)
        glColor3d(255, 0, 0)
        glVertex2f(self.p1.x, self.p1.y)
        glVertex2f(self.p2.x, self.p2.y)
        glVertex2f(self.p3.x, self.p3.y)
        # for p in self.fields:
        # print(p.x, p.y, end=" ")
        glEnd()


class Point:
    def __init__(self, x, y, mark):
        self.x = x
        self.y = y
        self.mark = mark


class Collection:
    def __init__(self):
        self.collection = []

    def addInCollectis(self, p, p1):
        self.collection.append([p, p1])
        print("( ", p.x, p.y, " ) ---> (", p1.x, p1.y, " )")


class RealWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_minimum_size(100, 100)

        self.set_maximum_size(1920, 1080)

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glClearColor(0, 0, 0, 0)

        self.points = []
        self.edge = []
        self.fields = []
        self.line = []
        self.convexCheck = True
        self.draw_line = False
        self.segmentOn = False
        self.collection = Collection()
        self.clip = True
        self.normal = []
        self.draw = []
        self.copy_line = []

    def Clipping(self, clipper, flag):
        self.normal = []
        clipper.append(clipper[0])
        for i in range(0, len(clipper) - 1):  # построение нормалей
            x = (clipper[i + 1].y - clipper[i].y)
            y = (clipper[i].x - clipper[i + 1].x)
            size = len_vect(x, y)
            x /= size
            y /= size
            self.normal.append(Point(x, y, False))

        for k in range(0, len(self.line) // 2):
            v1 = copy.deepcopy(self.line[2 * k + 1])
            v0 = copy.deepcopy(self.line[2 * k])
            t1, t0 = 1.0, 0
            visible = True
            for i in range(0, len(clipper) - 1):
                Qx = v0.x - clipper[i].x
                Qy = v0.y - clipper[i].y
                Nx = self.normal[i].x
                Ny = self.normal[i].y
                Pn = (v1.x - v0.x) * Nx + Ny * (v1.y - v0.y)
                Qn = Qx * Nx + Qy * Ny

                if Pn == 0:
                    if Qn < 0:
                        visible = False
                        break
                else:
                    t = - Qn / Pn
                    if Pn < 0:
                        if t < t0:
                            visible = False
                            break
                        if t <= t1:
                            t1 = t
                    else:
                        if t > t1:
                            visible = False
                            break
                        if t >= t0:
                            t0 = t
            print(t0, t1, visible)
            if not visible and not flag:
                self.draw.append([v0, v1])
            if visible:
                if t0 > t1:
                    visible = False
                else:
                    fx, fy = v1.x, v1.y
                    v1.x = v0.x + t1 * (v1.x - v0.x)
                    v1.y = v0.y + t1 * (v1.y - v0.y)
                    v0.x = v0.x + t0 * (fx - v0.x)
                    v0.y = v0.y + t0 * (fy - v0.y)
                    if flag:
                        self.draw.append([v0, v1])
                    else:
                        self.draw.append([self.line[2 * k], v0])
                        self.draw.append([self.line[2 * k + 1], v1])

        self.clip = False

    def Convex(self, edges):  # дополняет многоугольник до выпуклого и собирает области дополнения в массив
        self.convexCheck = False
        for i in range(0, len(edges) - 1):

            if vectMult(edges[i], edges[i + 1]):
                self.convexCheck |= True
                self.points[i + 1].mark = False

                if i != len(self.points) - 2:

                    self.fields.append(Field(
                        self.points[i], self.points[i + 1], self.points[i + 2])
                    )
                else:

                    self.fields.append(Field(
                        self.points[i], self.points[i + 1], self.points[0])
                    )

        if vectMult(edges[len(edges) - 1], edges[0]):
            self.convexCheck |= True
            self.points[0].mark = False
            self.fields.append(Field(
                self.points[1], self.points[0], self.points[len(self.points) - 1]
            ))

        arr = []
        for elem in self.points:
            if elem.mark:
                arr.append(elem)
        self.points = arr

    def on_draw(self):
        self.clear()
        self.draw_figure()
        if len(self.line) >= 2 and self.clip:
            for i in range(0, len(self.line) // 2):
                glBegin(GL_LINES)
                glColor3d(0, 255, 0)
                glVertex2f(self.line[2 * i].x, self.line[2 * i].y)
                glVertex2f(self.line[2 * i + 1].x, self.line[2 * i + 1].y)
                glEnd()

        for i in range(len(self.normal)):
            glBegin(GL_LINES)
            glColor3d(200, 0, 0)
            glVertex2f(self.points[i].x, self.points[i].y)
            glColor3d(200, 200, 200)
            glVertex2f(self.normal[i].x + self.points[i].x, self.normal[i].y + self.points[i].y)
            glEnd()

        for elem in self.draw:
            glColor3d(255, 255, 255)
            glBegin(GL_LINES)
            glVertex2f(elem[0].x, elem[0].y)
            glVertex2f(elem[1].x, elem[1].y)
            glEnd()

        for elem in self.fields:
            elem.draw()

    def on_resize(self, width1, height1):
        glViewport(0, 0, width1, height1)

    def on_key_press(self, symbol, modifiers):
        if symbol == 102:
            self.Clipping(self.points, False)
            for field in self.fields:
                self.Clipping(field.fields, True)
        if symbol == 119:
            self.points = []
            self.edge = []
            self.fields = []
            self.line = []
            self.convexCheck = True
            self.draw_line = False
            self.segmentOn = False
            self.collection = Collection()
            self.clip = True
            self.normal = []
            self.draw = []
            self.copy_line = []

    def draw_figure(self):  # Рисует фигуру и составляет ребра
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        if len(self.points) >= 2:

            glBegin(GL_LINE_STRIP)
            glColor3d(0, 0, 255)
            self.edge = []

            for i in range(0, len(self.points) - 1):
                self.edge.append(Point(
                    self.points[i + 1].x - self.points[i].x,
                    self.points[i + 1].y - self.points[i].y,
                    True
                ))

                glVertex2f(self.points[i].x, self.points[i].y)

            if len(self.points) >= 3:
                self.edge.append(Point(
                    self.points[0].x - self.points[len(self.points) - 1].x,
                    self.points[0].y - self.points[len(self.points) - 1].y,
                    True
                ))

            glVertex2f(self.points[len(self.points) - 1].x, self.points[len(self.points) - 1].y)

            glVertex2f(self.points[0].x, self.points[0].y)
            glEnd()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT and not self.draw_line:
            self.points.append(Point(x, y, True))
        elif button == mouse.LEFT and self.draw_line:
            self.line.append(Point(x, y, True))

        if button == mouse.RIGHT:
            self.draw_line = True
            while self.convexCheck:
                self.draw_figure()
                self.Convex(self.edge)


if __name__ == "__main__":
    window = RealWindow(500, 500, "lab5", resizable=True)
    pyglet.app.run()
