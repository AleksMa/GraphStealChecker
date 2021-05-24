import pyglet as pgl
from pyglet.gl  import *
from pyglet.window import key, mouse
import math as m

S = 600

coords_pol = [[]]
coords_cut = []
cutter = False

win = pgl.window.Window(S, S, 'lab5', resizable=True)
win.set_minimum_size(200, 200)

class Line:
    def __init__(self, x1, x2, y1, y2):
        self.A = y1 - y2
        self.B = x2 - x1
        self.C = x2*y1 - x1*y2

    def __str__(self):
        return 'line A:' + str(self.A) + ', B:' + str(self.B) + ', C:' + str(self.C)

class Edge:
    def __init__(self, x1, x2, y1, y2):
        self.minX = x1 if x1 < x2 else x2
        self.maxX = x2 if x1 < x2 else x1
        self.A = y1 - y2
        self.B = x2 - x1
        self.C = x2*y1 - x1*y2

    def __str__(self):
        return 'edge A:' + str(self.A) + ', B:' + str(self.B) + ', C:' + str(self.C)

def cross(line, edge):
    l1, l2 = line, edge
    delta = l1.A * l2.B - l1.B * l2.A
    if delta == 0:
        return False
    delta1 = l1.C * l2.B - l1.B * l2.C
    delta2 = l1.A * l2.C - l2.A * l1.C
    x = delta1 / delta
    y = delta2 / delta
    if edge.minX < x and x < edge.maxX:
        return [x, y]
    return False

def less(line, x, y):
    A, B, C = line.A, line.B, line.C
    if B == 0:
        if x < C / A:
            return True
    else:
        if y < (-A * x + C)/B:
            return True
    return False

def sutherlandHodgman():
    global coords_pol, coords_cut
    for i in range(len(coords_cut)):
    #print('coords: ' + str(coords_cut))
    #for i in range(2):
        #print('new')
        Cx1, Cy1 = coords_cut[i-1][0], coords_cut[i-1][1]
        Cx2, Cy2 = coords_cut[i][0], coords_cut[i][1]
        lineC = Line(Cx1, Cx2, Cy1, Cy2)
        #print(lineC)
        nextX = coords_cut[0][0] if i == len(coords_cut)-1 else coords_cut[i+1][0]
        nextY = coords_cut[0][1] if i == len(coords_cut)-1 else coords_cut[i+1][1]
        b1 = less(lineC, nextX, nextY)
        #print(b1)
        for j in range(len(coords_pol)):
            res = []
            for k in range(len(coords_pol[j])):
                Px1, Py1 = coords_pol[j][k-1][0], coords_pol[j][k-1][1]
                Px2, Py2 = coords_pol[j][k][0], coords_pol[j][k][1]
                edgeP = Edge(Px1, Px2, Py1, Py2)
                #print(edgeP)
                b2 = cross(lineC, edgeP)
                #print(b2)
                if b2 == False:
                    if b1 == less(lineC, Px1, Py1):
                        res.append([Px2, Py2])
                else:
                    if b1 == less(lineC, Px1, Py1):
                        res.append(b2)
                    else:
                        res.append(b2)
                        res.append([Px2, Py2])
                #print('res: ' + str(res))
            coords_pol[j] = res

    fixing()


def fixing():
    global coords_pol
    #print('coords: ', coords_pol)
    new = []
    change = False
    for i in range(len(coords_pol)):
        if change:
            break
        for j in range(len(coords_pol[i]) - 1):
            if change:
                break
            Px1, Py1 = coords_pol[i][j-1][0], coords_pol[i][j-1][1]
            Px2, Py2 = coords_pol[i][j][0], coords_pol[i][j][1]
            #print(Px1, Py1, Px2, Py2)
            e1 = Edge(Px1, Px2, Py1, Py2)
            #print(e1)
            for k in range(j+1, len(coords_pol[i])):
                Qx1, Qy1 = coords_pol[i][k-1][0], coords_pol[i][k-1][1]
                Qx2, Qy2 = coords_pol[i][k][0], coords_pol[i][k][1]
                #print('    ', Qx1, Qy1, Qx2, Qy2)
                e2 = Edge(Qx1, Qx2, Qy1, Qy2)
                #print('    ', e2, 'points:', Px1, Px2, Py1, Py2)
                if congruent(e1, e2, Px1, Px2, Py1, Py2):
                    #print("*")
                    Cx, Cy = Px1, Py1
                    l1 = [[Cx, Cy]]
                    i1 = j - 2
                    while Cx != Qx2 or Cy != Qy2:
                        Cx, Cy = coords_pol[i][i1][0], coords_pol[i][i1][1]
                        l1.append([Cx, Cy])
                        i1 -= 1
                    #print('new: ', l1)
                    Cx, Cy = Qx1, Qy1
                    l2 = [[Cx, Cy]]
                    i1 = k - 2
                    while Cx != Px2 or Cy != Py2:
                        Cx, Cy = coords_pol[i][i1][0], coords_pol[i][i1][1]
                        l2.append([Cx, Cy])
                        i1 -= 1
                    #print('new: ', l2)
                    new.append(l1)
                    new.append(l2)
                    #print('final: ', new)
                    change = True
                    break
    #print('new: ', new)
    if change:
        #print('*')
        coords_pol = division(coords_pol, new)
        fixing()

def division(pol, new):
    a = []
    for i in pol:
        skip = False
        for k in new:
            if skip:
                break
            for l in k:
                if i[0] == l:
                    skip = True
                    break
        if not skip:
            a.append(i[:])
            #print('a: ', a)
    for i in a:
        new.append(i)
    return new
                    

def congruent(e1, e2, Px1, Px2, Py1, Py2):
    if (e1.minX < e2.minX and e1.maxX > e2.maxX or e2.minX < e1.minX and e2.maxX > e1.maxX) and\
       round(e2.A * Px1 + e2.B * Py1, 5) == round(e2.C, 5) and\
       round(e2.A * Px2 + e2.B * Py2, 5) == round(e2.C, 5):
        return True
    return False
    
@win.event
def on_draw():
    win.clear()
    if cutter:
        glBegin(GL_LINE_LOOP)
        glColor3f(255, 0, 0)
        for c in coords_cut:
            glVertex2f(*c)
        glEnd()
    for c in coords_pol:
        glBegin(GL_LINE_LOOP)
        glColor3f(0, 255, 255)
        for c1 in c:
            glVertex2f(*c1)
        glEnd()
     

@win.event
def on_key_press(symbol, modifiers):
    global cutter
    if symbol == key.SPACE:
        cutter = True
    if symbol == key.Q:
        sutherlandHodgman()

@win.event
def on_mouse_press(x, y, button, modifiers):
    global coords, cutter
    if button == mouse.LEFT:
        if cutter:
            coords_cut.append([x, y])
        else:
            coords_pol[0].append([x, y])
    
pgl.app.run()
