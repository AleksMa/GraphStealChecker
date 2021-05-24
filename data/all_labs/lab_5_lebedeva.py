import math

from pyglet.window import key
from pyglet.gl import *
from math import *
import pyglet

screenWidth, screenHeight = 500, 500

window = pyglet.window.Window(500, 500, resizable=True)
window.set_minimum_size(100, 100)
glClearColor(34, 1, 1, 1)

EPS =  1e-6

ratio = 1
fill = GL_LINE
Rotate_x = 0.0
Rotate_y = 0.0
Rotate_z = 0.0
x = 0
y = 0
z = 0
scale = 90
circle = 9
triag = 9
fz = 0.25
phi = asin(fz / sqrt(2.0))
teta = asin(fz / sqrt(2.0 - fz * fz))
windowW = 500
windowH = 500
matrix = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1))

updated = True
cuting = False

edges = []
triangles = []

class Edge():
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1  # нормализованы
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.dx = x2 - x1  # направляющий вектор
        self.dy = y2 - y1
        self.dz = z2 - z1
        self.intersections = []  # параметр точек
        self.enterPoints = []
        self.exitPoints = []
        self.ins = False

polo = 0
otr = 0


class Triangle():
    def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        self.x1, self.y1, self.z1 = x1, y1, z1
        self.x2, self.y2, self.z2 = x2, y2, z2
        self.x3, self.y3, self.z3 = x3, y3, z3
        self.a = [x3 - x2, y3 - y2, z3 - z2]
        self.b = [x1 - x2, y1 - y2, z1 - z2]
        self.nx = self.a[1] * self.b[2] - self.a[2] * self.b[1]  # нормали
        self.ny = self.a[2] * self.b[0] - self.a[0] * self.b[2]
        self.nz = self.a[0] * self.b[1] - self.a[1] * self.b[0]
        self.d = -(self.nx * self.x1 + self.ny * y1 + self.nz * z1)  # свободный коэф из уравнения прямой
    def contains(self, x, y, z):
        inPlane = abs(self.nx * x + self.ny * y + self.nz * z + self.d) < EPS
        if inPlane:
            inside = True
            if (crossScalarProduct(self.x2 - self.x1, self.y2 - self.y1, self.z2 - self.z1, x - self.x1, y - self.y1,
                                   z - self.z1, self.nx, self.ny, self.nz) < EPS):
                inside = False
            if (crossScalarProduct(x - self.x1, y - self.y1, z - self.z1, self.x3 - self.x1, self.y3 - self.y1,
                                   self.z3 - self.z1, self.nx, self.ny, self.nz) < EPS):
                inside = False
            if (crossScalarProduct(self.x2 - x, self.y2 - y, self.z2 - z, self.x3 - x, self.y3 - y, self.z3 - z,
                                   self.nx, self.ny, self.nz) < EPS):
                inside = False
            # print(inside)
            return inside
        else:
            print("oshibka, tochka vne ploskosti")
            return False
    def intersect(self, edg):
        h = (self.nx * edg.dx + self.ny * edg.dy + self.nz * edg.dz)
        if (abs(h) < EPS):
            return
        t = -(self.nx * edg.x1 + self.ny * edg.y1 + self.nz * edg.z1 + self.d) / h
        print("t " + str(t))
        global polo, otr
        if t > 0: polo +=1
        if t < 0: otr +=1
        if (t > 0 and t < 1 and self.contains(edg.x1 + t * edg.dx, edg.y1 + t * edg.dy, edg.z1 + t * edg.dz)):
            print("all ok t " + str(t))
            vMult = self.nx * edg.dx + self.ny * edg.dy + self.nz * edg.dz
            edg.intersections.append(t)
            if (vMult > 0):
                edg.exitPoints.append(t)
            else:
                edg.enterPoints.append(t)


def triangle_square(a, b, c):
    p = (a + b + c) / 2
    return sqrt(p * (p - a) * (p - b) * (p - c))

def crossScalarProduct(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    x4 = y1 * z2 - z1 * y2
    y4 = z1 * x2 - x1 * z2
    z4 = x1 * y2 - y1 * x2
    return x4 * x3 + y4 * y3 + z4 * z3

def checkInside(edge):
    r = 0.3
    R = 0.7
    rad1 = sqrt(edge.x1 * edge.x1 + edge.y1 * edge.y1)
    rad2 = sqrt(edge.x2 * edge.x2 + edge.y2 * edge.y2)
    if (rad1 >= r and rad1 <= R) and (rad2 >= r and rad2 <= R) and abs(edge.z1) < 0.2 and abs(edge.z2) < 0.2:
        edge.ins = True

def Draw(circle, triag, circle_rad_big, circle_rad_min):
    majorStep = 2.0 * math.pi / circle
    minorStep = 2.0 * math.pi / triag
    glColor3f(255, 0.0, 80)

    for i in range(circle):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)
        glBegin(GL_TRIANGLE_STRIP)

        for j in range(triag + 1):
            b = j * minorStep
            r_big = circle_rad_min * cos(b) + circle_rad_big
            r_small = circle_rad_min * sin(b)
            glVertex3d(x0 * r_big, y0 * r_big, r_small)
            glVertex3d(x1 * r_big, y1 * r_big, r_small)
        glEnd()



class Vert():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def makeTriangles(circle, triag, circle_rad_big, circle_rad_min):
    majorStep = 2.0 * math.pi / circle
    minorStep = 2.0 * math.pi / triag
    verts = []
    for i in range(circle):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(triag + 1):
            b = j * minorStep
            r_big = circle_rad_min * cos(b) + circle_rad_big
            r_small = circle_rad_min * sin(b)
            verts.append(Vert(x0 * r_big, y0 * r_big, r_small))
            verts.append(Vert(x1 * r_big, y1 * r_big, r_small))
        glEnd()
    # print("verts size " + str(len(verts)))
    for i in range(0, len(verts), 4):
        v0 = verts[i]
        v1 = verts[i + 1]
        v2 = verts[i + 2]
        v3 = verts[i + 3]
        triangles.append(Triangle(v0.x, v0.y, v0.z, v1.x, v1.y, v1.z, v2.x, v2.y, v2.z))
        triangles.append(Triangle(v1.x, v1.y, v1.z, v3.x, v3.y, v3.z, v2.x, v2.y, v2.z))


def Draw_Tor():
    glPolygonMode(GL_FRONT_AND_BACK, fill)
    Draw(circle, triag, 0.5, .2)


def MakeTriangles():
    makeTriangles(circle, triag, 0.5, .2)


def cut():
    global edges
    for tr in triangles:
        for i in range(len(edges)):
            tr.intersect(edges[i])
    newEdges = []
    for edg in edges:
        if (len(edg.intersections) > 0):
            print("found intersections "+str(len(edg.intersections)))
            edg.intersections.sort()
            edg.enterPoints.sort()
            edg.exitPoints.sort()
            i = 0
            # если начинается с точки входа, то один цикл, если с точки выхода, то другой
            if len(edg.enterPoints) > 0 and abs(edg.enterPoints[0] - edg.intersections[0]) < EPS:
                i = 0
            else:
                i = 1
            edg.intersections.append(0)
            edg.intersections.append(1)
            edg.intersections.sort()
            while i+1 < len(edg.intersections):
                t1 = edg.intersections[i]
                t2 = edg.intersections[i+1]
                i += 2
                newEdges.append(Edge(edg.x1 + edg.dx * t1, edg.y1 + edg.dy * t1, edg.z1 + edg.dz * t1, edg.x1 + t2 * edg.dx, edg.y1 + t2 * edg.dy, edg.z1 + t2 * edg.dz))
        else:
            print("no intersections")
            checkInside(edg)
            print(edg.ins)
            if not edg.ins:
                newEdges.append(edg)
    edges = newEdges


def drawLines():
    glColor3f(0.0, 0, 255)
    for e in edges:
        glBegin(GL_LINES)
        glVertex3f(e.x1, e.y1, e.z1)
        glVertex3f(e.x2, e.y2, e.z2)
        glEnd()

@window.event
def on_resize(w, h):
    glViewport(w, h, 0, 0)
    global ratio
    ratio = w/h

@window.event
def on_draw():
    global cuting, updated
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if updated:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, windowW, windowH)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glOrtho(-ratio, ratio, -1, 1, 0.1, -500)
        glTranslatef(x+250, y+250, z+250)
        glRotatef(Rotate_x, 0, 1, 0)
        glRotatef(Rotate_y, 1, 0, 0)
        glRotatef(Rotate_z, 0, 0, 1)
        glScaled(scale, scale, scale)
        Draw_Tor()
        drawLines()
        updated = False

def init():
    global cuting, triangles, edges
    edges = []
    triangles = []
    # 0.3 0.7
    edges.append(Edge(0.061, -1.5, 0.05, 0.0488, 1.5, 0.03)) # насковозь
    edges.append(Edge(0.0, 0.0, 0.0, 0.8, 0.1, 0.03)) # из центра и проходит через одну половину
    edges.append(Edge(-0.8, 0.43, 0.05, 0.1, 0.8, 0.04)) # касается
    edges.append(Edge(-1, 0.1, 0.05, 1, 0.8, 0.04)) # проходит по половине
    edges.append(Edge(-0.8, -0.9, -0.03, -0.8, -0.1, -0.03)) # полностью снаружи
    edges.append(Edge(-0.4, -0.2, -0.03, -0.6, -0.1, 0.03)) # полностью внутри
    edges.append(Edge(-0.2, 0.1, -0.03, 0.0, 0.1, 0.03))  # в центре
    edges.append(Edge(-0.2, -0.5, -0.03, 0.2, 0.5, 0.03))  # из одной половинки в другую
    edges.append(Edge(-1, -0.6, 1, 1, -0.5, 1))  # проходит по половине но ближе

    MakeTriangles()
    if (cuting):
        cut()



@window.event
def on_key_press(symbol, modifiers):
    global updated, Rotate_x, Rotate_y, Rotate_z, fill, matrix, scale, x, y, z, cuting, circle, triag
    updated = True
    tr = 1
    ro = 5
    if key.SPACE == symbol:
        if fill == GL_FILL:
            fill = GL_LINE
        else: fill = GL_FILL
    if symbol == key.RIGHT:
        x += tr
    if symbol == key.LEFT:
        x -= tr
    if symbol == key.UP:
        y += tr
    if symbol == key.DOWN:
        y -= tr
    if symbol == key.M:
        z -= tr
    if symbol == key.K:
        z += tr
    if key.W == symbol:
        Rotate_x += ro
    if key.Q == symbol:
        Rotate_x -= ro
    if key.A == symbol:
        Rotate_y -= ro
    if key.S == symbol:
        Rotate_y += ro
    if key.Z == symbol:
        Rotate_z -= ro
    if key.X == symbol:
        Rotate_z += ro
    if key.EQUAL == symbol:
        scale += 2
    if key.MINUS == symbol:
        scale -= 2
    if key.C == symbol:
        cuting = not cuting
    if key.T == symbol:
        circle+=2
    if key.G == symbol:
        circle-=2
    if key.Y == symbol:
        triag+=2
    if key.H == symbol:
        triag-=2
    init()




init()
pyglet.app.run()