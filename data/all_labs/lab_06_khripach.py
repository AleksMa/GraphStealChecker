import pyglet as pgl
import ctypes
from pyglet.gl import *
from pyglet.window import key, mouse
import math as m

S = 600
n = 4
p = 10
c = 2
c1 = 0.5
t = 0
flag = False
animation = False

light1 = light2 = light3 = light0 = light4 = False

tex = False
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

class Point:
    def __init__(self, coord, nCoord, tCoord, aCoord):
        self.coord = coord
        self.nCoord = nCoord
        self.tCoord = tCoord
        self.aCoord = aCoord
'''
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
    coords = countFrustum(p, c)
    print(coords)

    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    i = 0
    for j in range(p+1):
        for k in range(n):
            #glTexCoords()
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

    norms = countNorm(coords)
    print(norms)
    for nx in norms:
        glNormal3f(*nx)

    for cx in coords:
        glTexCoord2f(cx[0], cx[2])
    glEnd()
'''
def drawFrustum2():
    global n, p, c, t, flag
    coords1 = countFrustum(p, c)
    points = makePoints(coords1)

    glBegin(GL_TRIANGLES)
    if animation:
        if t < 1 and not flag:
            t += 0.01
        else:
            flag = True
        if t > 0 and flag:
            t -= 0.01
        else:
            flag = False
        for po in points:
            for co in po:
                glNormal3f(*co.nCoord)
                glTexCoord2f(*co.tCoord)
                glVertex3f((1-t)**3 * co.coord[0] + 3*t*(1-t)**2 * (co.coord[0]/2) + 3*t*t*(1-t) * (co.aCoord[0]/2) + t**3 * co.aCoord[0],
                           (1-t)**3 * co.coord[1] + 3*t*(1-t)**2 * (co.coord[1]/2) + 3*t*t*(1-t) * (co.aCoord[1]/2) + t**3 * co.aCoord[1],
                           (1-t)**3 * co.coord[2] + 3*t*(1-t)**2 * (co.coord[2]/2) + 3*t*t*(1-t) * (co.aCoord[2]/2) + t**3 * co.aCoord[2])
    else:
        for po in points:
            for co in po:
                glNormal3f(*co.nCoord)
                glTexCoord2f(*co.tCoord)
                glVertex3f(*co.coord)
    glEnd()

'''
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
'''
def countFrustum(p, c):
    global n
    coords1 = []
    for i in range(p+1):
        for k in range(n):
            coords1.append([m.cos(2*m.pi*k/n)*(2*p-i)/(2*p)*c, -c+2*c*i/p,
                           m.sin(2*m.pi*k/n)*(2*p-i)/(2*p)*c])     
    return coords1

def vector(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]

def vecMult(v1, v2):
    i = v1[1]*v2[2] - v1[2]*v2[1]
    j = v1[0]*v2[2] - v1[2]*v2[0]
    k = v1[0]*v2[1] - v1[1]*v2[0]

    l = m.sqrt(i*i + j*j + k*k)
    i /= l
    j /= l
    k /= l
    return [i, j, k]

def makePoints(coords):
    global n, p
    points = []
    #print(coords)
    v2 = vector(coords[0], coords[n - 1])
    v1 = vector(coords[0], coords[1])
    #vm = vecMult(v1, v2)
    vm = [0, -1, 0]
    vm2 = [-vm[0], -vm[1], -vm[2]]
    for i in range(n):
        ps = []
        ps.append(Point(coords[i], vm, [coords[i][0]/4,coords[i][2]/4], [coords[i+n*p][0], coords[i][1], coords[i+n*p][2]]))
        if i < n-1:
            ps.append(Point(coords[i+1], vm, [coords[i+1][0]/4,coords[i+1][2]/4], [coords[i+1+n*p][0], coords[i+1][1], coords[i+1+n*p][2]]))
        else:
            ps.append(Point(coords[0], vm, [coords[0][0]/4,coords[0][2]/4], [coords[n*p][0], coords[0][1], coords[n*p][2]]))
        ps.append(Point([0, coords[i][1], 0] , vm, [0,0], [0, coords[i][1], 0]))
        points.append(ps)
    for i in range(len(coords) - n, len(coords)):
        ps = []
        ps.append(Point(coords[i], vm2, [coords[i][0],coords[i][2]], [coords[i-n*p][0], coords[i][1], coords[i-n*p][2]]))
        ps.append(Point([0, coords[i][1], 0] , vm2, [0,0], [0, coords[i][1], 0]))
        if i < len(coords) - 1:    
            ps.append(Point(coords[i+1], vm2, [coords[i+1][0],coords[i+1][2]], [coords[i+1-n*p][0], coords[i+1][1], coords[i+1-n*p][2]]))
        else:
            ps.append(Point(coords[i+1 - n], vm2, [coords[i+1-n][0],coords[i+1-n][2]], [coords[i+1-n-n*p][0], coords[i+1-n][1], coords[i+1-n-n*p][2]]))
        points.append(ps)
    for j in range(p):
        step = (p - 2*j)*n if j <= (p+1)//2 else -(p-(p-j)*2)*n
        for i in range(n*j, n*j + n):
            v1 = vector(coords[i], coords[i + n])
            if i < n*j + n - 1:
                v2 = vector(coords[i], coords[i+1])
            else:
                v2 = vector(coords[i], coords[n*j])
            vm = vecMult(v1, v2)
            
            ps = []    
            ps.append(Point(coords[i], vm, [0,0], [coords[i+step][0], coords[i][1], coords[i+step][2]]))
            ps.append(Point(coords[i + n] , vm, [1,0], [coords[i+step-n][0], coords[i+n][1], coords[i+step-n][2]]))
            if i < n*j + n - 1:
                ps.append(Point(coords[i+1], vm, [0,1], [coords[i+1+step][0], coords[i+1][1], coords[i+1+step][2]]))
            else:
                ps.append(Point(coords[n*j], vm, [0,1], [coords[n*j + step][0], coords[n*j][1], coords[n*j + step][2]]))
            points.append(ps)
            ps = []
            if i < n*j + n - 1:
                ps.append(Point(coords[i+1 + n], vm, [0,1], [coords[i+1+step-n][0], coords[i+1+n][1], coords[i+1+step-n][2]])) 
                ps.append(Point(coords[i+1], vm, [0,0], [coords[i+1+step][0], coords[i+1][1], coords[i+1+step][2]]))
            else:
                ps.append(Point(coords[n*j + n], vm, [0,1], [coords[n*j+step-n][0], coords[n*j + n][1], coords[n*j+step-n][2]])) 
                ps.append(Point(coords[n*j], vm, [0,0], [coords[n*j + step][0], coords[n*j][1], coords[n*j + step][2]]))
            ps.append(Point(coords[i + n] , vm, [1,0], [coords[i+step-n][0], coords[i+n][1], coords[i+step-n][2]]))
                 
            points.append(ps)
        
    return points

def vec(*args):
    return (GLfloat * len(args))(*args)

def lightOn():
    global light0, light1, light2, light3
    glPushMatrix()

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, vec(1, 2, 1, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1, 1, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0, 0, 1))
    if not light0:
        glDisable(GL_LIGHT0)
        
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, vec(-1, 2, 1, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(1, 0, 0))
    glLightfv(GL_LIGHT1, GL_AMBIENT, vec(1, 0, 0))
    if not light1:
        glDisable(GL_LIGHT1)
             
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_POSITION, vec(-1, -2, 1, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT2, GL_DIFFUSE, vec(0, 1, 1))
    glLightfv(GL_LIGHT2, GL_AMBIENT, vec(0, 1, 1))
    if not light2:
        glDisable(GL_LIGHT2)
        
    glEnable(GL_LIGHT3)
    glLightfv(GL_LIGHT3, GL_POSITION, vec(1, -2, 1, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT3, GL_DIFFUSE, vec(1, 0, 1))
    glLightfv(GL_LIGHT3, GL_AMBIENT, vec(0, 1, 0))
    if not light3:
        glDisable(GL_LIGHT3)

    glEnable(GL_LIGHT4)
    glLightfv(GL_LIGHT4, GL_POSITION, vec(1, 1, 1, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT4, GL_DIFFUSE, vec(1, 1, 1))
    glLightfv(GL_LIGHT4, GL_AMBIENT, vec(1, 1, 1))
    if not light4:
        glDisable(GL_LIGHT4)
          
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec(0.2, 0.2, 0.2, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, vec(0.8, 0.8, 0.8, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128)
    
    glPopMatrix()

textures = GLuint()
def texture():
    #img = pyglet.image.load('texture.bmp')
    img = pyglet.image.load('plaster.bmp')
    glGenTextures(1, ctypes.pointer(textures))
    glBindTexture(GL_TEXTURE_2D, textures)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    data = img._current_data
    glTexImage2D(GL_TEXTURE_2D, 0, 3, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glBindTexture(GL_TEXTURE_2D, 0)

def countTexture():
    global n
    arr = []

def inv(b):
    if b == 0:
        return 1
    else:
        return 0

def saving():
    file = open('save.txt', 'w')
    file.write(str(coords[0]) + ' ' + str(coords[1]) + ' ' + str(coords[2]) + ' ')
    file.write(str(rotation[0]) + ' ' + str(rotation[1]) + ' ' + str(rotation[2]) + ' ')
    file.write(str(tex) + ' ')
    file.write(str(n) + ' ')
    file.write(str(c) + ' ')
    file.write(str(light0) + ' ' + str(light1) + ' ' + str(light2) + ' ' +
               str(light3) + ' ' + str(light4) + ' ')
    file.write(str(animation))

def loading():
    global coords, rotation, tex, n, c, light0, light1, light2, light3, light4, animation
    file = open('save.txt', 'r')
    data = file.read()
    datas = data.split()
    coords = [float(datas[0]), float(datas[1]), float(datas[2])]
    rotation = [float(datas[3]), float(datas[4]), float(datas[5])]
    tex = True if datas[6] == 'True' else False
    n, c = int(datas[7]), float(datas[8])
    light0 = True if datas[9] == 'True' else False
    light1 = True if datas[10] == 'True' else False
    light2 = True if datas[11] == 'True' else False
    light3 = True if datas[12] == 'True' else False
    light4 = True if datas[13] == 'True' else False
    animation = True if datas[14] == 'True' else False
    file.close()
    

@win.event
def on_draw():
    win.clear()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_NORMALIZE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    #texture()
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
    '''
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-1, -1, -0.5)
    glScalef(0.2, 0.2, 0.2)
    useful_function()
    '''
    lightOn()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(coords[0] - 2, coords[1] - 2, coords[2] - 0.3)
    glScalef(0.2, 0.2, 0.2)
    glRotatef(rotation[0], 1, 0, 0)
    glRotatef(rotation[1], 0, 1, 0)
    glRotatef(rotation[2], 0, 0, 1)
    if tex:
        glBindTexture(GL_TEXTURE_2D, textures)
    else:
        glBindTexture(GL_TEXTURE_2D, 0)
    drawFrustum2()
    glPopMatrix()
    
@win.event
def on_resize(width, height):
    global anti_resize
    glViewport(0, 0, width, height)
    anti_resize = width/height

@win.event
def on_key_press(symbol, modifiers):
    global skeleton, n, p, c, light0, light1, light2, light3, light4, tex
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
        tex = not tex
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
    elif symbol == key.Z:
        light4 = not light4
    elif symbol == key.X:
        light0 = not light0
    elif symbol == key.C:
        light1 = not light1
    elif symbol == key.V:
        light2 = not light2
    elif symbol == key.B:
        light3 = not light3
    elif symbol == key.N:
        saving()
    elif symbol == key.M:
        loading()
        
@win.event
def on_mouse_press(x, y, button, modifiers):
    global animation
    if button == mouse.RIGHT:
        animation = not animation

def update(dt):
    pass
pgl.clock.schedule_interval(update, 1/100)

texture()
pgl.app.run()
