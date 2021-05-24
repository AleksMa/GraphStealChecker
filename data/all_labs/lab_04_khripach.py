import pyglet as pgl
from pyglet.gl import *
from pyglet.window import key, mouse
import math as m

S = 600

coords = []
edges = []
minX = minY = S
maxX = maxY = 0
color = False
win = pgl.window.Window(S, S, "lab4", resizable=True)
win.set_minimum_size(200, 200)
buf = (GLubyte * (3 * win.width * win.height))(0)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

def cross(x1, x2, y1, y2, y):
    k = (x2-x1)/(y2-y1)
    b = -y1*k + x1
    return k*y + b

def inv(x, y, buf):
    i = (win.width*y + x)*3
    c = 255 if buf[i+1] == 0 else 0
    buf[i+1] = c
    buf[i+2] = c

def counting():
    global coords, edges
    for i in range(len(coords)):
        x1, y1 = coords[i][0], coords[i][1]
        x2, y2 = coords[i-1][0], coords[i-1][1]
        if y1 == y2:
            break
        points = []
        r = range(y1, y2) if y1 < y2 else range(y2, y1)
        for j in r:
            points.append([cross(x1, x2, y1, y2, j+0.5), j+0.5])
        edges.append(points)
    return edges

def coloring(edges):
    global color, buf
    buf = (GLubyte * (3 * win.width * win.height))(0)
    if color:
        global minX, maxX
        s = (maxX + minX)//2
        for edge in edges:
            for point in edge:
                x1, y = m.ceil(point[0]), int(point[1])
                x2 = m.floor(point[0] + 1)
                r = range(x2, s) if x1 < s else range(s, x1)
                for i in r:
                    inv(i, y, buf)
    glDrawPixels(win.width, win.height, GL_RGB, GL_UNSIGNED_BYTE, buf)
    if not color:
        draw_lines()
'''           
def draw_lines(edges):
    buf = (GLubyte * (3 * win.width * win.height))(0)
    for edge in edges:
        for point in edge:
            x, y = m.floor(point[0]), int(point[1] - 0.5)
            i = (win.width*y + x)*3
            buf[i+1] = 255
            buf[i+2] = 255
    glDrawPixels(win.width, win.height, GL_RGB, GL_UNSIGNED_BYTE, buf)
'''
def draw_lines():
    global coords
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 255, 255)
    for c in coords:
        glVertex2f(*c)
    glVertex2f(*coords[0])
    glEnd()

def smooth():
    global maxY
    bufs = [[] for i in range(maxY + 1)]
    
    for i in range(len(coords)):
        x = coords[i][0]
        y = coords[i][1]
        x2 = coords[i+1][0] if i < len(coords)-1 else coords[0][0]
        y2 = coords[i+1][1] if i < len(coords)-1 else coords[0][1]
        dx = x2 - x
        dy = y2 - y
        s1 = int(dx/abs(dx)) if dx != 0 else 0
        s2 = int(dy/abs(dy)) if dy != 0 else 0
        dx = abs(dx)
        dy = abs(dy)
        h = 0
        if dx != 0:
            h = dy/dx
        ch = False

        if dy > dx:
            dx, dy = dy, dx
            ch = True
            h = 1/h

        i_max = 255
        h *= i_max
        e = i_max / 2
        w = i_max - h
        j = 1
        while j <= dx:
            b = (coords[i][0] > x2) != (coords[i][1] > y2)
            if not ch:
                param = 255 - int(e) if b else int(e)
            else:
                param = int(e) if b else 255 - int(e)
            bufs[y].append([x, param])
            if e <= w:
                if ch:
                    y += s2
                else:
                    x += s1
                e += h
            else:
                x += s1
                y += s2
                e -= w
            j += 1
            
    make_buf(bufs)

def make_buf(bufs):
    global buf
    for i in range(len(bufs)):
        for j in bufs[i]:
            #buf[(win.width*i + j[0])*3] = 255 - j[1]
            buf[(win.width*i + j[0])*3 + 1] = 255 - j[1]
            buf[(win.width*i + j[0])*3 + 2] = 255 - j[1]
    glDrawPixels(win.width, win.height, GL_RGB, GL_UNSIGNED_BYTE, buf)

@win.event
def on_draw():
    pass

@win.event
def on_key_press(symbol, modifiers):
    global edges, color
    if symbol == key.SPACE:
        edges = counting()
        draw_lines()
    if symbol == key.Q:
        color = not color
        coloring(edges)
    if symbol == key.W:
        smooth()

@win.event
def on_mouse_press(x, y, button, modifiers):
    global coords, minX, maxX, minY, maxY
    if button == mouse.LEFT:
        coords.append([x, y])
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y

pgl.app.run()
