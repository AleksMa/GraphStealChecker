import math
from OpenGL.GL import glRasterPos
from pyglet.window import key
from pyglet.gl import *
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

class Cor():
    def __init__(self, x, y):
        self.x = x
        self.y = y

coor_array = []
list_pixel = [[]]
max_line = Cor
edges = [[]]
check_edge = []

def origSort(n):
    return n[0]

def algorithm():
    global max_line, list_pixel, edges
    list = [[] for x in range(0, max_line.y + 1)]
    list2 = list_pixel
    for edge in edges:
        for line in range(edge[0].y, edge[1].y):
            k = cross(edge, line + 0.5)
            list[int(line)] += [[int(k.x), 255]]
    newList = []
    for g in range(len(list)):
        newList.append(list[g].sort(key=origSort))
    for i in range(len(list)):
        for j in range(0, len(list[i]), 2):
            l = list[i][j][0]
            r = list[i][j + 1][0]
            li = [[int(x), 255] for x in range(int(l) + 1, math.ceil(r+1))]
            k = list2[i]
            n = k + li
            list2[i] = n

    list_pixel = list2
    make_buf(list_pixel)

def find_edge(vers):
    mas1 = []
    mas2 = []
    for i in range(len(vers)):
            v1 = vers[i]
            v2 = vers[(i+1)%len(vers)]
            if v1.y<=v2.y and v2.y-v1.y != 0:
                mas1.append([v1, v2])
                mas2.append(False)
            elif v2.y-v1.y != 0:
                mas1.append([v2, v1])
                mas2.append(True)
            else:
                mas1.append([v1, v2])
                mas2.append(False)
    global edges, check_edge
    edges = mas1
    check_edge = mas2

def max_ver():
    global coor_array, max_line
    m = coor_array[0]
    for v in coor_array:
        if v.y > m.y:
            m = v
    max_line = m

def cross(edge, line):
    v1 = edge[0]
    v2 = edge[1]
    dx_dy = (edge[1].x-edge[0].x)/(edge[1].y-edge[0].y)
    if line < v1.y or line > v2.y:
        return False
    x_cross = dx_dy*(line-v1.y)+v1.x
    return Cor(x_cross, line)

def sign(a):
    if a>0:
        return 1
    if a<0:
        return -1
    if a==0:
        return 0

def line_smooth_brezen():
    global list_pixel, edges
    temp_pixels = list_pixel
    for i in range(len(edges)):
        if check_edge[i]:
            edge = [edges[i][1], edges[i][0]]
        else:
            edge = edges[i]
        dx = abs(edge[1].x-edge[0].x)
        dy = abs(edge[1].y-edge[0].y)
        s1 = sign(edge[1].x-edge[0].x)
        s2 = sign(edge[1].y-edge[0].y)
        x = edge[0].x
        y = edge[0].y
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
            if not change:
                if (edge[0].x > edge[1].x) != (edge[0].y > edge[1].y):
                    param = 255 - int(e)
                else: param = int(e)
            else:
                flag = (edge[0].x > edge[1].x) != (edge[0].y > edge[1].y)
                if flag: param = int(e)
                else: param = 255 - int(e)
            temp_pixels[y] += [[x, param]]
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
    list_pixel = temp_pixels
    make_buf(list_pixel)


def line_brezen():
    global list_pixel, edges
    temp_pixels = list_pixel
    for edge in edges:
        dx = int(math.fabs(edge[1].x-edge[0].x))
        dy = int(math.fabs(edge[1].y-edge[0].y))
        s1 = sign(edge[1].x-edge[0].x)
        s2 = sign(edge[1].y-edge[0].y)
        x = edge[0].x
        y = edge[0].y
        if dy == 0:
            for i in range(dx):
                temp_pixels[y] += [[x, 255]]
                x += s1
        elif dx == 0:
            for i in range(dy):
                list_pixel[y] += [[x, 255]]
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
            list_pixel[y] += [[x, 255]]
            for i in range(0, dx):
                while 0 <= e:
                    list_pixel[y] += [[x, 255]]
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
                list_pixel[y] += [[x, 255]]
    list_pixel = temp_pixels
    make_buf(list_pixel)




def set_pixel(buf, x, y, r, g, b, i,  w):
    buf[(x + y * w) * 3 + 0] = (r+(255-i)).to_bytes(1, 'big')
    buf[(x + y * w) * 3 + 1] = (g+(255-i)).to_bytes(1, 'big')
    buf[(x + y * w) * 3 + 2] = (b+(255-i)).to_bytes(1, 'big')


def make_buf(list_pixel):
    k = w * h * 3
    buf = [b'\xff'] * k
    for i in range(len(list_pixel)):
        for j in list_pixel[i]:
            set_pixel(buf, j[0], i, 0, 0, 0, j[1], w)
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
        global max_line, list_pixel, edges
        max_ver()
        find_edge(coor_array)
        list_pixel = [[] for x in range(0, max_line.y + 1)]
        if not fill and not smooth: line_brezen()
        if not fill and smooth: line_smooth_brezen()
        if fill and not smooth: algorithm()
        if fill and smooth: algorithm(), line_smooth_brezen()


@window.event
def on_resize(w0, h0):
    global buff
    global w, h
    if w != int(w0 / zoom) or h != int(h0 / zoom):
        buff = ''
        w = int(w0 / zoom)
        h = int(h0 / zoom)



pyglet.app.run()