import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from math import *

width = 500
height = 500

class Display:
    def __init__(self, w, h):
        self.height = h
        self.width = w
        self.pixels = [0] * (h * w * 3)
        self.points = []
        self.pixelIsRastered = [[False] * h for i in range(w)]
        self.sampPixels = [0] * (h * w * 3)
        self.shapeIsDrawn = False
        self.weight = [[0] * h for i in range(w)]
        self.fill = False

    def clear(self):
        self.resize(self.width, self.height)

    def resize(self, w, h):
        self.height = h
        self.width = w
        self.pixels = [0] * (h * w * 3)
        self.sampPixels = [0] * (h * w * 3)
        self.points = []
        self.pixelIsRastered = [[False] * h for i in range(w)]
        self.shapeIsDrawn = False
        self.weight = [[0] * h for i in range(w)]
        self.fill = False

    def setColor(self, i, j, r, g, b):
        self.pixels[(3 * self.width * i) + (3 * j)] = r
        self.pixels[(3 * self.width * i) + (3 * j) + 1] = g
        self.pixels[(3 * self.width * i) + (3 * j) + 2] = b

    def getPixel(self, i, j):
        return [self.pixels[(3 * self.width * i) + (3 * j)],
                self.pixels[(3 * self.width * i) + (3 * j) + 1],
                self.pixels[(3 * self.width * i) + (3 * j) + 2]]

    def append_point(self, x, y):
        self.points.append(self.Point(x, y))
        self.setColor(y, x, 1, 1, 1)

    def clearPixels(self):
        self.pixels = self.pixels = [0] * (self.height * self.width * 3)
        self.pixelIsRastered = [[False] * self.height for i in range(self.width)]
        self.shapeIsDrawn = False
        self.weight = [[0] * self.height for i in range(self.width)]

    def setWeight(self, x, y):

        self.weight[x][y] += 4

        self.weight[x + 1][y] += 2

        self.weight[x - 1][y] += 2

        self.weight[x][y + 1] += 2

        self.weight[x][y - 1] += 2

        self.weight[x + 1][y + 1] += 1

        self.weight[x - 1][y - 1] += 1

        self.weight[x - 1][y + 1] += 1

        self.weight[x + 1][y - 1] += 1

    def setColor_sampling(self,i, j, r, g, b):
        self.sampPixels[(3 * self.width * i) + (3 * j)] = r
        self.sampPixels[(3 * self.width * i) + (3 * j) + 1] = g
        self.sampPixels[(3 * self.width * i) + (3 * j) + 2] = b

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def fillShape(self):
        if not self.shapeIsDrawn:
            for y in range(self.height):
                for x in range(self.width - 1):
                    self.pixelIsRastered[x + 1][y] ^= self.pixelIsRastered[x][y]
                    if self.pixelIsRastered[x][y]:
                        self.setColor(y, x, 1, 1, 1)
                        self.setWeight(x, y)
            self.shapeIsDrawn = True

    def brezenhem(self, p1, p2):
        A = p2.x - p1.x
        B = p2.y - p1.y

        if abs(A) > abs(B):  # delta x > delta y

            if A < 0:
                p1, p2 = p2, p1
                A *= -1
                B *= -1

            signb = -1 if B < 0 else 1
            B = abs(B)
            y = p1.y
            f = A // 2

            self.setColor(p1.y, p1.x, 1, 1, 1)
            self.setColor(p2.y, p2.x, 1, 1, 1)
            self.setWeight(p1.x, p1.y)
            self.setWeight(p2.x, p2.y)

            for x in range(p1.x, p2.x + 1):
                self.setColor(y, x, 1, 1, 1)
                self.setWeight(x, y)
                f -= B
                if f < 0:

                    if y != p1.y and y != p2.y:
                        self.pixelIsRastered[x][y] ^= True
                    y += signb
                    f += A

            if signb > 0:
                self.pixelIsRastered[p2.x][p2.y] ^= True
            else:
                self.pixelIsRastered[p1.x][p1.y] ^= True
        else:  # delta y > delta x
            if B < 0:
                p1, p2 = p2, p1
                A *= -1
                B *= -1
            signa = -1 if A < 0 else 1
            A = abs(A)
            x = p1.x
            f = B // 2
            self.setColor(p1.y, p1.x, 1, 1, 1)
            self.setColor(p2.y, p2.x, 1, 1, 1)
            self.setWeight(p1.x, p1.y)
            self.setWeight(p2.x, p2.y)

            for y in range(p1.y, p2.y + 1):

                self.setColor(y, x, 1, 1, 1)
                self.setWeight(x, y)

                if y != p2.y and y != p1.y:
                    self.pixelIsRastered[x][y] ^= True

                f -= A

                if f < 0:
                    x += signa
                    f += B
            self.pixelIsRastered[p2.x][p2.y] ^= True

    def sampling(self):
        for i in range(self.height):
            for j in range(self.width):
                k = self.weight[j][i]
                self.setColor_sampling(i, j, k/16, k/16, k/16)

class RealWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_minimum_size(100, 100)

        self.set_maximum_size(1920, 1080)

        self.D = Display(width, height)

        self.figure = True

        self.show_sampl = False

        glClearColor(0, 0, 0, 0)

    def draw_lines(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)

        if self.figure and len(self.D.points) > 1:
            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 1.0)
            for i in range(0, len(self.D.points) - 1):
                glVertex2i(self.D.points[i].x, self.D.points[i].y)
                glVertex2i(self.D.points[i + 1].x, self.D.points[i + 1].y)
            glVertex2i(self.D.points[0].x, self.D.points[0].y)
            glVertex2i(self.D.points[len(self.D.points) - 1].x, self.D.points[len(self.D.points) - 1].y)
            glEnd()

    def on_draw(self):
        self.clear()
        if not self.show_sampl:
            glDrawPixels(self.D.width, self.D.height, GL_RGB, GL_FLOAT, (GLfloat * len(self.D.pixels))(*self.D.pixels))
        else:
            glDrawPixels(self.D.width, self.D.height, GL_RGB, GL_FLOAT, (GLfloat * len(self.D.sampPixels))(*self.D.sampPixels))
        self.draw_lines()

    def on_resize(self, width1, height1):
        glViewport(0, 0, width1, height1)
        self.D.resize(width1, height1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width1, 0, height1)
        self.D.resize(width1, height1)

    def on_key_press(self, symbol, modifiers):
        if symbol == 108:
            self.show_sampl = not self.show_sampl
        if symbol == 110:
            self.D.clear()
        if symbol == 102:
            self.D.fill = symbol == 102
            self.D.fillShape()
            self.D.sampling()

    def on_mouse_press(self, x, y, button, modifiers):

        if button == mouse.LEFT:

            self.D.append_point(x, y)

            if len(self.D.points) > 1:

                glBegin(GL_LINES)

                glColor3f(1.0, 1.0, 1.0)

                for i in range(0, len(self.D.points) - 1):
                    glVertex2i(self.D.points[i].x, self.D.points[i].y)

                    glVertex2i(self.D.points[i + 1].x, self.D.points[i + 1].y)

                    glVertex2i(self.D.points[0].x, self.D.points[0].y)

                glVertex2i(self.D.points[len(self.D.points) - 1].x, self.D.points[len(self.D.points) - 1].y)
                glEnd()

        elif button == mouse.RIGHT:
            self.figure = False
            self.D.clearPixels()
            for i in range(0, len(self.D.points) - 1):
                self.D.brezenhem(self.D.points[i], self.D.points[i + 1])
            if len(self.D.points) > 2:
                self.D.brezenhem(self.D.points[0], self.D.points[len(self.D.points) - 1])


if __name__ == "__main__":
    window = RealWindow(width, height, "lab3", resizable=True)
    pyglet.app.run()
