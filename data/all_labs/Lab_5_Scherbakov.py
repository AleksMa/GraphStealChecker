from pyglet import *
from pyglet.gl import *
from collections import deque


def cw(a, b, c):
    return (b[1] - a[1]) * \
           (c[0] - a[0]) - \
           (b[0] - a[0]) * \
           (c[1] - a[1]) > 0


def graham_scan(points):
    hull = []
    p0 = min(points, key=lambda a: a[1] + 0.0000001 * a[0])
    hull.append(p0)
    points.remove(p0)
    points.sort(key=lambda a: (a[0] - p0[0]) / (((a[0] - p0[0]) ** 2 + (a[1] - p0[1]) ** 2) ** 0.5))
    for point in points:
        while len(hull) > 1 and cw(hull[-1], hull[-2], point):
            hull.pop()
        hull.append(point)
    return hull


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cyrus_beck(polygon):
    p0 = line[0]
    p1 = line[1]
    D = (p1[0] - p0[0], p1[1] - p0[1])
    n = dict()
    for i in range(len(polygon)):
        n[i] = (polygon[i][1] - polygon[(i + 1) % len(polygon)][1], polygon[(i + 1) % len(polygon)][0] - polygon[i][0])
    te = 0
    to = 1
    for i in range(len(n)):
        w = (p1[0] - polygon[i][0], p1[1] - polygon[i][1])
        t = dot(n[i], w) / dot(n[i], D)
        if dot(n[i], D) == 0 and dot(w, n[i]) < 0:
            return (0, 0), (0, 0)
        if dot(n[i], D) < 0:
            to = min(to, t)
        if dot(n[i], D) > 0:
            te = max(te, t)
    if te > to:
        te = to = 0
    return (p1[0] - D[0] * te, p1[1] - D[1] * te), (p1[0] - D[0] * to, p1[1] - D[1] * to)


def IsConvex(a, b, c):
    # only convex if traversing anti-clockwise!
    crossp = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if crossp >= 0:
        return True
    return False


def InTriangle(a, b, c, p):
    L = [0, 0, 0]
    eps = 0.0000001
    # calculate barycentric coefficients for point p
    # eps is needed as error correction since for very small distances denom->0
    L[0] = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) \
           / (((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])) + eps)
    L[1] = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) \
           / (((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])) + eps)
    L[2] = 1 - L[0] - L[1]
    # check if p lies in triangle (a, b, c)
    for x in L:
        if x > 1 or x < 0:
            return False
    return True


def IsClockwise(poly):
    # initialize sum with last element
    sum = (poly[0][0] - poly[len(poly) - 1][0]) * (poly[0][1] + poly[len(poly) - 1][1])
    # iterate over all other elements (0 to n-1)
    for i in range(len(poly) - 1):
        sum += (poly[i + 1][0] - poly[i][0]) * (poly[i + 1][1] + poly[i][1])
    if sum > 0:
        return True
    return False


def triangulate(poly):
    size = len(poly)
    if size < 3:
        return []
    if size == 3:
        tri = [(poly[0], poly[1], poly[2])]
        del poly[:]
        return tri
    for i in range(size):
        tritest = False
        p1 = poly[(i - 1) % size]
        p2 = poly[i % size]
        p3 = poly[(i + 1) % size]
        if IsConvex(p1, p2, p3):
            for x in poly:
                if not (x in (p1, p2, p3)) and InTriangle(p1, p2, p3, x):
                    tritest = True
            if not tritest:
                del poly[i % size]
                rest = triangulate(poly)
                rest.append((p1, p2, p3))
                return rest
    print('GetEar(): no ear found')
    return []


tela = pyglet.window.Window(height=500, width=500, resizable=True)


@tela.event
def on_draw():
    global vertices, line
    glClear(GL_COLOR_BUFFER_BIT)
    if len(vertices) < 3:
        return
    glColor3f(1, 0, 0)
    hull = graham_scan(vertices.copy())
    glBegin(GL_LINE_LOOP)
    for i in hull:
        glVertex2i(i[0], i[1])
    glEnd()
    i = 0
    while hull[i] != vertices[0]:
        i += 1
    drawing = False
    glColor3f(1, 1, 1)
    figure = []
    points = []
    triangles = []
    for v in vertices:
        if not drawing:
            if v != hull[i]:
                glBegin(GL_LINE_LOOP)
                glVertex2i(hull[i - 1][0], hull[i - 1][1])
                glVertex2i(v[0], v[1])
                figure.append((hull[i - 1][0], hull[i - 1][1]))
                figure.append((v[0], v[1]))
                i -= 1
                drawing = True
            i += 1
            i %= len(hull)
        else:
            glVertex2i(v[0], v[1])
            figure.append((v[0], v[1]))
            if v == hull[i]:
                if len(line) == 2:
                    temp = triangulate(figure)
                    triangles.extend(temp)
                    figure.clear()
                drawing = False
                glEnd()
                i += 1
                i %= len(hull)
    if drawing:
        glVertex2i(vertices[0][0], vertices[0][1])
        figure.append((vertices[0][0], vertices[0][1]))
        if len(line) == 2:
            temp = triangulate(figure)
            triangles.extend(temp)
            figure.clear()
        glEnd()
    if len(line) < 2:
        return
    for i in triangles:
        temp = (i[2], i[1], i[0])
        points.extend(cyrus_beck(temp))
    pe, po = cyrus_beck(hull)
    points.append(pe)
    points.append(po)
    points.sort(key=lambda x: x[0])
    glBegin(GL_LINES)
    for i in points:
        glVertex2i(round(i[0]), round(i[1]))
    glEnd()


@tela.event
def on_mouse_press(x, y, button, modifiers):
    global vertices, line
    if button == window.mouse.LEFT:
        vertices.append((x, y))
    if button == window.mouse.RIGHT:
        line.append((x, y))


@tela.event
def on_key_press(s, m):
    global vertices, line
    if s == window.key.A:
        line.clear()
        vertices.clear()
    if s == window.key.S:
        line.clear()


vertices = []
line = deque(maxlen=2)
app.run()
