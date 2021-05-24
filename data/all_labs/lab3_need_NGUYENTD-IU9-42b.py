from pyglet import *
from pyglet.gl import *
from pyglet.window import key
import math, random

class Prism:
    def __init__(self,c,angleX=0,angleY=0,angleZ=0,Ox=1,Oy=1,Oz=1):
        self.c = c
        self.angleX = angleX
        self.angleY = angleY
        self.angleZ = angleZ
        self.length = 0.1
        self.Ox = Ox
        self.Oy = Oy
        self.Oz = Oz
        self.vertL = []
        self.vertU = []

		### define function calculate() to get the polygonal mesh for the prism
		### as i already mentioned, this function should be called whenever the "geometry" (i.e. polygonal mesh) changes
		### all the vertices of the mesh should be stored in a data structure of your own design

    def calc(self,num):
        self.vertL = []
        self.vertU = []
        for i in range(num):
            self.vertL.append((self.length*math.sin(i/num*2*math.pi) + self.Ox,
                               self.length*math.cos(i/num*2*math.pi) + self.Oy,
                               0 + self.Oz))

            self.vertU.append((self.length*math.sin(i/num*2*math.pi) + self.Ox,
                               self.length*math.cos(i/num*2*math.pi) + self.Oy,
                               self.c + self.Oz))


    def draw(self):
        glTranslatef(self.Ox,self.Oy,self.Oz)
        glRotatef(self.angleX,1,0,0)
        glRotatef(self.angleY,0,1,0)
        glRotatef(self.angleZ,0,0,1)
        glTranslatef(-self.Ox,-self.Oy,-self.Oz)
        '''cA cB cC is RGB color code, I generated randomly'''
        cA = 150
        cB = 100
        cC = 190

        '''lower num-gonal'''
        glBegin(GL_POLYGON)

        cA = (cA + 100)%255
        cB = (cB - 75 + 255)%255
        cC = (cC + 324)%255
        glColor3f(cA/255,cB/255,cC/255)
        for i in range(num):
		### here and further in draw() you should only get vertices from your data structure, with no calculations
		### in calculate() function, vertex[num] should be the copy of vertex[0] to complete the mesh properly, without any "gaps"
            glVertex3f(*self.vertL[i])

        glEnd()

        '''upper num-gonal'''
        cA = (cA + 4312)%255
        cB = (cB - 124 + 255)%255
        cC = (cC - 123 + 255)%255
        glBegin(GL_POLYGON)
        glColor3f(cA/255,cB/255,cC/255)
        for i in range(num):
            glVertex3f(*self.vertU[i])
        glEnd()

        '''num faces rectangles'''
        for i in range(num):
            cA = (cA + 132)%255
            cB = (cB + 123)%255
            cC = (cC - 201 + 255)%255
            glBegin(GL_QUADS)
            glColor3f(cA/255,cB/255,cC/255)
            if (i==num-1):
                j=0
            else:
                j=i+1
            glVertex3f(*self.vertL[i])
            glVertex3f(*self.vertL[j])
            glVertex3f(*self.vertU[j])
            glVertex3f(*self.vertU[i])
            glEnd()

class Cube:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def draw(self):
        glRotatef(0,1,0,0)
        glRotatef(0,0,1,0)
        glRotatef(0,0,0,1)

        verD = [(self.a,self.b,0),(self.a+self.c,self.b,0),
                (self.a+self.c,self.b+self.c,0),(self.a,self.b+self.c,0)]
        verU = [(self.a,self.b,self.c),(self.a+self.c,self.b,self.c),
                (self.a+self.c,self.b+self.c,self.c),(self.a,self.b+self.c,self.c)]

        cA = 200
        cB = 200
        cC = 200

        cA = (cA + 4123)%255
        cB = (cB - 234 + 255)%255
        cC = (cC + 124)%255

        glBegin(GL_QUADS)
        glColor3f(cA/255,cB/255,cC/255)
        for i in range(4):
            glVertex3f(*verD[i])
        glEnd()

        glBegin(GL_QUADS)
        glColor3f(cA,cB,cC)
        for i in range(4):
            glVertex3f(*verU[i])
        glEnd()

        for i in range(4):
            cA = (cA - 241 + 255)%255
            cB = (cB - 124 + 255)%255
            cC = (cC + 6435)%255
            glBegin(GL_QUADS)
            glColor3f(cA/255,cB/255,cC/255)
            if (i==3):
                j=0
            else:
                j=i+1
            glVertex3f(*verD[i])
            glVertex3f(*verD[j])
            glVertex3f(*verU[j])
            glVertex3f(*verU[i])
            glEnd()

window = pyglet.window.Window(width=1600, height=900)

prism = Prism(0.3)
cube = Cube(0.3,0,0.15)
status = 0
num = 6
prism.calc(num)

@window.event
def on_draw():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    ### I understood what I used for rendering isometric projection here
    '''this length so that camera is 1 unit away from origin'''
    dist = math.sqrt(1 / 3.0) #'''1/sqrt(3) = arctan(30)'''

    gluLookAt(dist, dist, dist, #'''pos of camera'''
          0.0,  0.0,  0.0, #'''pos which camera look at'''
          0.0,  1.0,  0.0) #'''direction'''

	### the right projection as long as you clearly understand what matrix is finally rendered internally

    '''
    glMatrixMode(GL_MODELVIEW)

    glBegin(GL_LINES);

    glColor3d(1.0, 0.0, 0.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.1, 0.0, 0.0);

    glColor3d(0.0, 1.0, 0.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, 0.1, 0.0);

    glColor3d(0.0, 0.0, 1.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, 0.0, 0.1);

    glEnd();

    glFlush();

    '''
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0,0,0,0);
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST) # Enable depth testing for z-culling

    glPushMatrix()
    prism.draw()
    glPopMatrix()

    glPushMatrix()
    cube.draw()
    glPopMatrix()

    glFlush()


@window.event
def on_key_press(symbol,modifiers):
    global fovy,status,projection,angle,num

    if symbol == key.ENTER:
        status = 1-status
        if status==1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    elif symbol == key.SPACE:
        num+=1
        prism.calc(num) #<---
		### call calculate to generate new mesh
    elif symbol == key.UP:
        prism.Oy+=0.1
    elif symbol == key.DOWN:
        prism.Oy-=0.1
    elif symbol == key.LEFT:
        prism.Ox-=0.1
    elif symbol == key.RIGHT:
        prism.Ox+=0.1
    elif symbol == key.F12:
        prism.Oz+=0.1
    elif symbol == key.F11:
        prism.Oz-=0.1
    elif symbol == key.Q:
        prism.angleY-=20
    elif symbol == key.A:
        prism.angleY+=20
    elif symbol == key.W:
        prism.angleZ-=20
    elif symbol == key.S:
        prism.angleZ+=20
    elif symbol == key.E:
        prism.angleX-=20
    elif symbol == key.D:
        prism.angleX+=20


pyglet.app.run()
