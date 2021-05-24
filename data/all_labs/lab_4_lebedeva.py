import math

import numpy
from OpenGL.GL import glRasterPos
from pyglet.gl import glPixelStorei, glDrawPixels
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet
zoom = 2
w = int(500/zoom)
h = int(500/zoom)
window = pyglet.window.Window(500, 500, resizable=True)
window.set_minimum_size(100, 100)
glClearColor(1, 1, 1, 1)

fill = False
smooth = False
buff = ""

class x_and_smooth:
    def __init__(self, x, smooth):
        self.x = x
        self.smooth = smooth


class Cor():
    def __init__(self, x, y):
        self.x = x
        self.y = y

coor_array = []


class Edge():
    def __init__(self, v1, v2, mah):
        self.v1 = v1
        self.v2 = v2
        self.dx = v2.x-v1.x
        self.dy = v2.y-v1.y
        self.mah = mah

def find_edge(vers):
    mas = []
    for i in range(len(vers)):
            v1 = vers[i]
            v2 = vers[(i+1)%len(vers)]
            if v1.y<=v2.y and v2.y-v1.y != 0:
                mas.append(Edge(v1, v2, False))
            elif v2.y-v1.y != 0:
                mas.append(Edge(v2, v1, True))
            else:
                mas.append(Edge(v1, v2, False))
    return mas


def max_ver(plgn):
    m = plgn.max_line
    for v in plgn.ver:
        if v.y > m.y:
            m = v
    plgn.max_line = m

class Plgn():
    def __init__(self, lst):
        self.n = len(lst)
        self.ver = lst
        self.max_line = lst[0]
        max_ver(self)
        self.edge = find_edge(lst)
        self.cross = []
        self.list_pixel = [[] for x in range(0, self.max_line.y + 1)]

def cross(edge, line):
    v1 = edge.v1
    v2 = edge.v2
    dx_dy = edge.dx/edge.dy
    if line < v1.y or line > v2.y:
        return False
    x_cross = dx_dy*(line-v1.y)+v1.x
    return Cor(x_cross, line)


def scan(plgn, line):
    cor_cross = []
    for edge in plgn.edge:
        c = cross(edge, line)
        if c != False:
            cor_cross.append(c)
    return cor_cross


def sort_my(d):
    return d[0]


def sign(a):
    if a>0:
        return 1
    if a<0:
        return -1
    if a==0:
        return 0

def line_smooth_brezen(plgn):
    list_pixel = plgn.list_pixel
    for edge1 in plgn.edge:
        if edge1.mah: edge = Edge(edge1.v2, edge1.v1, False)
        else: edge = edge1
        dx = abs(edge.dx)
        dy = abs(edge.dy)
        s1 = sign(edge.dx)
        s2 = sign(edge.dy)
        x = edge.v1.x
        y = edge.v1.y
        try:
            h = dy / dx
        except ZeroDivisionError:
            h = 0
        change = False

        if dy > dx:
            dx, dy = dy, dx
            change = True
            if h:
                h = 1 / h
        i_max = 255
        h *= i_max
        e = i_max / 2
        w = i_max - h
        i = 1
        while i <= dx:
            param = int(e)
            if not change:
                if (edge.v1.x > edge.v2.x) != (edge.v1.y > edge.v2.y):
                    param = 255 - int(e)
                else: param = int(e)
            else:
                flag = (edge.v1.x > edge.v2.x) != (edge.v1.y > edge.v2.y)
                if flag: param = int(e)
                else: param = 255 - int(e)


            list_pixel[y] += [x_and_smooth(x, param)]
            if e <= w:
                if change:
                    y += s2
                else:
                    x += s1
                e += h
            else:
                x += s1
                y += s2
                e -= w
            i += 1
    make_buf(plgn)


def line_brezen(plgn):
    list_pixel = plgn.list_pixel
    for edge in plgn.edge:
        dx = int(math.fabs(edge.dx))
        dy = int(math.fabs(edge.dy))
        s1 = sign(edge.dx)
        s2 = sign(edge.dy)
        x = edge.v1.x
        y = edge.v1.y
        if dy == 0:
            for i in range(dx):
                list_pixel[y] += [x_and_smooth(x, 255)]
                x += s1
        elif dx == 0:
            for i in range(dy):
                list_pixel[y] += [x_and_smooth(x, 255)]
                y += s2

        else:
            if dy < dx:
                t = dx
                dx = dy
                dy = t
                f = 1
            else:
                f = 0
            e = 2 * dy - dx
            list_pixel[y] += [x_and_smooth(x, 255)]
            for i in range(0, dx):
                while 0 <= e:
                    list_pixel[y] += [x_and_smooth(x, 255)]
                    if f == 1:
                        x = x + s1
                    else:
                        y = y + s2
                    e = e - 2 * dx
                if f == 1:
                    y = y + s2
                else:
                    x = x + s1
                e = e + 2 * dy
                list_pixel[y] += [x_and_smooth(x, 255)]
    plgn.list_pixel = list_pixel
    make_buf(plgn)

def active_edge(plgn):
    d = dict()
    for i in range(plgn.max_line.y+1, -1, -1):
        d[i] = []
    for edge in plgn.edge:
        if edge.dy != 0:
            for line in range(plgn.max_line.y + 1, -1, -1):
                c = cross(edge, line + 0.5)
                if c != False:
                    d[line].append([c.x, (edge.v1.x - edge.v2.x) / edge.dy, edge.dy - 1])
                    break
    for i in d:
        for z in d[i]:
            if z[2] != 0:
                n = [z[0]+z[1], z[1], z[2]-1]
                d[i-1].append(n)
        d[i].sort(key=sort_my)
    list_pixel = plgn.list_pixel
    for i in d:
        for j in range(0, len(d[i]), 2):
            l = d[i][j][0]
            r = d[i][j + 1][0]
            li = [x_and_smooth(x, 255) for x in range(int(l)+1, math.ceil(r))]
            k = list_pixel[i]
            n = k + li
            list_pixel[i] = n
    plgn.list_pixel = list_pixel
    make_buf(plgn)

def set_pixel(buf, x, y, r, g, b, i,  w):
    buf[(x + y * w) * 3 + 0] = (r+(255-i)).to_bytes(1, 'big')
    buf[(x + y * w) * 3 + 1] = (g+(255-i)).to_bytes(1, 'big')
    buf[(x + y * w) * 3 + 2] = (b+(255-i)).to_bytes(1, 'big')

def make_buf(plgn):
    k = w * h * 3
    buf = [b'\xff'] * k
    for i in range(len(plgn.list_pixel)):
        for j in plgn.list_pixel[i]:
            set_pixel(buf, j.x, i, 0, 0, 0, j.smooth, w)
    y = b''
    for i in buf:
        y = y+i
    global buff
    buff = y

@window.event
def on_draw():
    window.clear()
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glEnable(GL_DITHER)
    glRasterPos(0, 0)
    glPixelZoom(zoom, zoom)
    if buff != '':
        glDrawPixels(w, h, GL_RGB, GL_UNSIGNED_BYTE, buff)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global coor_array
    coor_array.append(Cor(int(x/zoom), int(y/zoom)))

@window.event
def on_key_press(symbol, modifiers):
    global coor_array
    global fill, zoom, smooth, buff
    if symbol == key.D:
        coor_array = []
    if symbol == key.SPACE:
        fill = not fill
    if symbol == key.ENTER and coor_array != []:
        buff = ''
    if symbol == key.UP:
        zoom += 1
    if symbol == key.DOWN:
        zoom -= 1
    if symbol == key.S:
        smooth = not smooth
    if coor_array != []:
        plgn = Plgn(coor_array)
        if not fill and not smooth: line_brezen(plgn)
        if not fill and smooth: line_smooth_brezen(plgn)
        if fill and not smooth: active_edge(plgn)
        if fill and smooth: active_edge(plgn), line_smooth_brezen(plgn)


@window.event
def on_resize(w0, h0):
    global buff
    global w, h
    if w != int(w0 / zoom) or h != int(h0 / zoom):
        buff = ''
        w = int(w0 / zoom)
        h = int(h0 / zoom)



# def main():
    # plgn1 = Plgn([Cor(10, 10), Cor(80, 10), Cor(80, 60), Cor(50, 30), Cor(10, 70)])
    # plgn2 = Plgn([Cor(90, 10), Cor(140, 30), Cor(110, 100), Cor(70, 80), Cor(20, 20)])


# main()
# # plgn1 = Plgn([Cor(10, 10), Cor(80, 10), Cor(80, 60), Cor(50, 30), Cor(10, 70)])
# plgn = Plgn([Cor(28, 50), Cor(15, 70)])
# line_smooth_brezen(plgn)
pyglet.app.run()

