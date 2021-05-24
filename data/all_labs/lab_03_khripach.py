import pyglet as pgl
from pyglet.gl import *
from pyglet.window import key, mouse
import math as m

S = 600
n = 4
p = 3
c = 2
c1 = 0.5
skeleton = False
f_colors = [[1,0,0], [0,0,1], [0,1,0]]
colors = [[1,0,0], [0,1,0], [0,0,1], [1,1,1], [1,1,0], [1,0.64,0], [0,1,1]]
sides = [[c1,c1,c1], [-c1,c1,c1], [-c1,-c1,c1], [c1,-c1,c1],
         [c1,-c1,-c1], [-c1,-c1,-c1], [-c1,c1,-c1], [c1,c1,-c1]]
coords = [2,2,0]
rotation = [0]*3
anti_resize = 1

win = pgl.window.Window(S, S, resizable=True)
win.set_minimum_size(200, 200)

def drawCube(c, s1, s2, s3, s4):
    glBegin(GL_POLYGON)
    glColor3f(*c)
    glVertex3f(*s1)
    glVertex3f(*s2)
    glVertex3f(*s3)
    glVertex3f(*s4)
    glEnd()

def useful_function():
    drawCube(colors[0], sides[0], sides[1], sides[2], sides[3])  
    drawCube(colors[1], sides[1], sides[2], sides[5], sides[6])
    drawCube(colors[2], sides[0], sides[3], sides[4], sides[7]) 
    drawCube(colors[3], sides[0], sides[1], sides[6], sides[7])
    drawCube(colors[4], sides[2], sides[3], sides[4], sides[5])
    drawCube(colors[5], sides[4], sides[5], sides[6], sides[7])

def drawFrustum():
    global n, p, c 
    coords = countFrustum(n, p, c)

    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)
    i = 0
    for j in range(p+1):
        for k in range(n):
            glVertex3f(*coords[i])
            if k == n-1:
                glVertex3f(*coords[i-n+1])
            else:
                glVertex3f(*coords[i+1])
            glVertex3f(0, -c+2*c*j/p, 0)
            i += 1
    i = 0
    for j in range(p):
        b = 0
        if n % 2 == 0:
            glColor3f(*f_colors[b])
        else:
            glColor3f(*f_colors[2])
        b = inv(b)
        for k in range(n):
            glVertex3f(*coords[i])
            if k == n-1:
                glVertex3f(*coords[i-n+1])
            else:
                glVertex3f(*coords[i+1])
            glVertex3f(*coords[i+n])
            glVertex3f(*coords[i+n])
            if k == n-1:
                glVertex3f(*coords[i+1])
                glVertex3f(*coords[i-n+1])
            else:
                glVertex3f(*coords[i+n+1])
                glVertex3f(*coords[i+1])
            i += 1
            glColor3f(*coords[b])
            b = inv(b)
    glEnd()

def drawSkeleton():
    global n, p, c
    coords = countFrustum(n, p, c)

    i = 0
    for j in range(p+1):
        glBegin(GL_LINE_LOOP)
        glColor3f(0, 1, 1)
        for k in range(n):
            glVertex3f(*coords[i])
            if k == n-1:
                glVertex3f(*coords[i-n+1])
            else:
                glVertex3f(*coords[i+1])
            glVertex3f(0, -c+2*c*j/p, 0)
            i += 1
        glEnd()
    i = 0
    for j in range(p):
        glBegin(GL_LINE_LOOP)
        glColor3f(0, 1, 1)
        for k in range(n):
            glVertex3f(*coords[i])
            if k == n-1:
                glVertex3f(*coords[i-n+1])
            else:
                glVertex3f(*coords[i+1])
            glVertex3f(*coords[i+n])
            glVertex3f(*coords[i+n])
            if k == n-1:
                glVertex3f(*coords[i+1])
                glVertex3f(*coords[i-n+1])
            else:
                glVertex3f(*coords[i+n+1])
                glVertex3f(*coords[i+1])
            i += 1
        glEnd()

def countFrustum(n, p, c):
    coords = []
    for i in range(p+1):
        for k in range(n):
            coords.append([m.cos(2*m.pi*k/n)*(2*p-i)/(2*p)*c, -c+2*c*i/p,
                           m.sin(2*m.pi*k/n)*(2*p-i)/(2*p)*c])     
    return coords

def inv(b):
    if b == 0:
        return 1
    else:
        return 0

@win.event
def on_draw():
    win.clear()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if win.height > win.width:
        glViewport(0, 0, win.height, win.height)
    else:
        glViewport(0, 0, win.width, win.width)

    glMatrixMode(GL_PROJECTION)

    coef = 0.5
    front_dimetry = (GLfloat*16)(1,0,0,0,
                     0,1,0,0,
                     -coef*m.cos(m.pi/4),-coef*m.sin(m.pi/4),1,0,
                     0,0,0,1)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -100, 100)
    glMultMatrixf(front_dimetry)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-1, -1, -0.5)
    glScalef(0.2, 0.2, 0.2)
    useful_function()
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(coords[0] - 2, coords[1] - 2, coords[2] - 0.3)
    glScalef(0.2, 0.2, 0.2)
    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)
    glRotatef(rotation[2], 0, 0, 1)
    if skeleton:
        drawSkeleton()
    else:
        drawFrustum()

    
@win.event
def on_resize(width, height):
    global anti_resize
    glViewport(0, 0, width, height)
    anti_resize = width/height

@win.event
def on_key_press(symbol, modifiers):
    global skeleton, n, p, c
    c1 = 0.1
    c2 = 11
    if symbol == key.UP:
        coords[1] += c1
    elif symbol == key.DOWN:
        coords[1] += -c1
    elif symbol == key.LEFT:
        coords[0] += -c1
    elif symbol == key.RIGHT:
        coords[0] += c1
    elif symbol == key.Q:
        coords[2] += c1
    elif symbol == key.A:
        coords[2] += -c1
    elif symbol == key.W:
        rotation[0] += -c2
    elif symbol == key.S:
        rotation[0] += c2
    elif symbol == key.E:
        rotation[1] += -c2
    elif symbol == key.R:
        rotation[1] += c2
    elif symbol == key.D:
        rotation[2] += -c2
    elif symbol == key.F:
        rotation[2] += c2
    elif symbol == key.SPACE:
        skeleton = not skeleton
    elif symbol == key.U:
        n += 1
    elif symbol == key.J and n > 3:
        n -= 1
    elif symbol == key.I:
        p += 1
    elif symbol == key.K and p > 1:
        p -= 1
    elif symbol == key.O:
        c += 0.5
    elif symbol == key.L and c > 0.5:
        c -= 0.5

@win.event
def on_mouse_press(x, y, button, modifiers):
    pass

pgl.app.run()
