from pyglet.window import key, mouse
from pyglet.gl import *
import pyglet

window = pyglet.window.Window(500, 500, resizable=True)
window.set_minimum_size(100, 100)
glClearColor(0, 0, 0, 0)
change = False
change2 = True
cut = False
fff = False
massCut = []
massTriangle = []
coordsCut = []
linesD = []
linesU = []
coordsLine = []
non = True


class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.pU = []
        self.pD = []
        self.cMt = [[]]
        self.fullIn = False
        self.fallOut = False
        self.pU, self.pD, self.fullIn, self.fallOut, self.cMt = check(self)


secCoordsLine = []


@window.event
def on_mouse_press(x, y, button, modifiers):
    global change, coordsLine, coordsCut
    if change and button == mouse.LEFT:
        coordsLine.append([x, y])
        if len(coordsLine) % 2 == 0:
            secCoordsLine.append(Line(coordsLine[len(coordsLine) - 2], coordsLine[len(coordsLine) - 1]))
    if not change and button == mouse.LEFT:
        coordsCut.append([x, y])


def triang():
    global coordsCut, massCut, massTriangle, non, mass
    massCut = coordsCut
    while non:
        mass = []
        non = False
        for i in range(len(massCut)):
            if i == len(massCut) - 1:
                ABx = massCut[i][0] - massCut[i - 1][0]
                ABy = massCut[i][1] - massCut[i - 1][1]
                BCx = massCut[0][0] - massCut[i][0]
                BCy = massCut[0][1] - massCut[i][1]
            else:
                ABx = massCut[i][0] - massCut[i - 1][0]
                ABy = massCut[i][1] - massCut[i - 1][1]
                BCx = massCut[i + 1][0] - massCut[i][0]
                BCy = massCut[i + 1][1] - massCut[i][1]
            form = ABx * BCy - ABy * BCx
            if form <= 0:
                mass.append([massCut[i][0], massCut[i][1]])
            else:
                non = True
                if i != len(massCut) - 1:
                    massTriangle.append([[massCut[i][0], massCut[i][1]], [massCut[i - 1][0], massCut[i - 1][1]],
                                         [massCut[i + 1][0], massCut[i + 1][1]]])
                else:
                    massTriangle.append([[massCut[i][0], massCut[i][1]], [massCut[i - 1][0], massCut[i - 1][1]],
                                         [massCut[0][0], massCut[0][1]]])

        massCut = mass


@window.event
def on_key_press(symbol, modifiers):
    global change, cut, fff, coordsCut, coordsLine
    if symbol == key.SPACE:
        change = True
        triang()
    if symbol == key.C:
        cut = not cut


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)


def my_sort(n):
    return n[0]


@window.event
def on_draw():
    global change
    window.clear()
    glBegin(GL_LINE_LOOP)
    glColor3ub(0, 91, 86)
    for i in coordsCut:
        glVertex2f(*i)
    glEnd()

    if not cut:
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)
        for i in coordsLine:
            glVertex2f(*i)
        glEnd()
    if cut:
        glBegin(GL_LINES)
        glColor3f(4, 68, 38)
        for i in secCoordsLine:
            if not i.fallOut:
                glVertex2f(*i.pD)
                for j in i.cMt:
                    glVertex2f(*j)
                glVertex2f(*i.pU)
        glEnd()


def normal(x1, y1, x2, y2):
    normCoords = []
    x = y2 - y1
    y = x1 - x2
    normCoords.append(x)
    normCoords.append(y)
    return normCoords


def multi(D, normCoords):
    return D[0] * normCoords[0] + D[1] * normCoords[1]


def check(line):
    global massTriangle, massCut
    crossMassTriang, massTDTU, secMassTDTU = [], [], []
    tDb, tUb, state = crsBck(line, massCut)

    if not state:
        line.fallOut = True
        return line.pU, line.pD, line.fullIn, line.fallOut, crossMassTriang
    else:
        for i in massTriangle:
            tD, tU, state = crsBck(line, i)
            if tD == 0.0 and tU == 1.0:
                line.fallOut = True
                return line.pU, line.pD, line.fullIn, line.fallOut, crossMassTriang
            elif state:
                if tD == 0.0:
                    tDb = tU
                elif tU == 1.0:
                    tUb = tD
                else:
                    massTDTU.append([tD, tU])

        if tDb != 0.0:
            piska = True
            while piska:
                piska = False
                j = 0
                while j < len(massTDTU):
                    if tDb == massTDTU[j][0]:
                        tDb = massTDTU[j][1]
                        piska = True
                        massTDTU.pop(j)
                    else:
                        j += 1
        if tUb != 1.0:
            piska = True
            while piska:
                piska = False
                j = 0
                while j < len(massTDTU):
                    if tUb == massTDTU[j][1]:
                        tUb = massTDTU[j][0]
                        piska = True
                        massTDTU.pop(j)
                    else:
                        j += 1
        xD = line.p1[0] + int(float(line.p2[0] - line.p1[0]) * tDb)
        yD = line.p1[1] + int(float(line.p2[1] - line.p1[1]) * tDb)
        line.pD.append(xD)
        line.pD.append(yD)
        xU = line.p1[0] + int(float(line.p2[0] - line.p1[0]) * tUb)
        yU = line.p1[1] + int(float(line.p2[1] - line.p1[1]) * tUb)
        line.pU.append(xU)
        line.pU.append(yU)

        massTDTU.sort(key=my_sort)

        if len(massTDTU) == 1 or len(massTDTU) == 0:
            secMassTDTU = massTDTU
        else:
            h = 0
            while h < len(massTDTU) - 1:
                if massTDTU[h][1] != massTDTU[h + 1][0]:
                    secMassTDTU.append(massTDTU[h])
                else:
                    k = h
                    while h < len(massTDTU) - 1 and massTDTU[h][1] == massTDTU[h + 1][0]:
                        h += 1
                    secMassTDTU.append([massTDTU[k][0], massTDTU[h][1]])
                h += 1
            if massTDTU[len(massTDTU) - 1][0] != massTDTU[len(massTDTU) - 2][1]:
                    secMassTDTU.append(massTDTU[h])

        for i in secMassTDTU:
            xD = line.p1[0] + int(float(line.p2[0] - line.p1[0]) * i[0])
            yD = line.p1[1] + int(float(line.p2[1] - line.p1[1]) * i[0])
            crossMassTriang.append([xD, yD])
            xU = line.p1[0] + int(float(line.p2[0] - line.p1[0]) * i[1])
            yU = line.p1[1] + int(float(line.p2[1] - line.p1[1]) * i[1])
            crossMassTriang.append([xU, yU])
        return line.pU, line.pD, line.fullIn, line.fallOut, crossMassTriang


def crsBck(line, mass):
    D = [line.p2[0] - line.p1[0], line.p2[1] - line.p1[1]]
    tD = 0.0
    tU = 1.0
    for i in range(len(mass)):
        normCoords = normal(mass[i - 1][0], mass[i - 1][1], mass[i][0], mass[i][1])
        Di = multi(D, normCoords)
        vec = [line.p1[0] - mass[i][0], line.p1[1] - mass[i][1]]
        wi = multi(vec, normCoords)
        if Di == 0:
            if wi >= 0:
                continue
            else:
                return 666, 666, False
        else:
            t = float(-wi) / float(Di)
            if Di > 0:
                if t <= 1.0:
                    tD = max(tD, t)
                else:
                    return 666, 666, False
            else:
                if t >= 0.0:
                    tU = min(tU, t)
                else:
                    return 666, 666, False
    if tD <= tU: return tD, tU, True
    return 666, 666, False


pyglet.app.run()