from pyglet import *
from pyglet.gl import *
import math, random

class Prism:
    def __init__(self,c,angleX=0,angleY=0,angleZ=0):
        self.c = c                  '''height of prism'''
        self.angleX = angleX
        self.angleY = angleY
        self.angleZ = angleZ

    def draw(self): '''draw prism methods'''

        if self.angleX+self.angleY+self.angleZ!=0:
            glRotatef(-angle,0,0,1)
            glRotatef(40,1,0,0)
        glRotatef(self.angleX,1,0,0)
        glRotatef(self.angleY,0,1,0)
        glRotatef(self.angleZ,0,0,1)

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
            glVertex3f(10*math.sin(i/num*2*math.pi),
                       10*math.cos(i/num*2*math.pi),0)

        glEnd()

        '''upper num-gonal'''
        cA = (cA + 4312)%255
        cB = (cB - 124 + 255)%255
        cC = (cC - 123 + 255)%255
        glBegin(GL_POLYGON)
        glColor3f(cA/255,cB/255,cC/255)
        for i in range(num):
            glVertex3f(10*math.sin(i/num*2*math.pi),
                       10*math.cos(i/num*2*math.pi),self.c)
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
            glVertex3f(10*math.sin(i/num*2*math.pi),
                       10*math.cos(i/num*2*math.pi),0)
            glVertex3f(10*math.sin(j/num*2*math.pi),
                       10*math.cos(j/num*2*math.pi),0)
            glVertex3f(10*math.sin(j/num*2*math.pi),
                       10*math.cos(j/num*2*math.pi),self.c)
            glVertex3f(10*math.sin(i/num*2*math.pi),
                       10*math.cos(i/num*2*math.pi),self.c)
            glEnd()

        ######DEBUG#############
        glBegin(GL_LINES)
        glColor3f (1, 1, 1) #red
        glVertex3f(-10,-10,0)
        glVertex3f(-10,10,0)
        glColor3f (1, 1, 1) #red
        glVertex3f(-10,10,0)
        glVertex3f(10,10,0)
        glColor3f (1, 1, 1) #red
        glVertex3f(10,10,0)
        glVertex3f(10,-10,0)
        glColor3f (1, 1, 1) #red
        glVertex3f(10,-10,0)
        glVertex3f(-10,-10,0)
        glColor3f (1, 1, 1) #red
        glVertex3f(-10,-10,self.c)
        glVertex3f(-10,10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(-10,10,self.c)
        glVertex3f(10,10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(10,10,self.c)
        glVertex3f(10,-10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(10,-10,self.c)
        glVertex3f(-10,-10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(-10,-10,0)
        glVertex3f(-10,-10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(-10,10,0)
        glVertex3f(-10,10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(10,10,0)
        glVertex3f(10,10,self.c)
        glColor3f (1, 1, 1) #red
        glVertex3f(10,-10,0)
        glVertex3f(10,-10,self.c)
        glEnd()
        #########################

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
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

prism = Prism(20)       ''' create a prism with height = 20 '''
cube = Cube(20,0,10)    ''' create a cube with from coordinate (20,0,0) and size = 10'''
fovy = 50               ''' fovy - changeable by interactive, use when changing position of perspective'''
angle = -10             ''' angle - changeable by interactive, use when changing position of camera around object'''
status = 0
num = 6                 '''num - changeable by interactive, use when changing to n-gonal prism  '''

@window.event
def on_draw():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy,float(window.width)/window.height,0.1,1000) '''navigate camera by change fovy of perspective <=> change size of object'''
    glTranslatef(0,-5,-100)
    glRotatef(-40,1,0,0)
    glRotatef(angle,0,0,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0,0,0,0);
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST) # Enable depth testing for z-culling

    '''
    ##########DEBUG########
    glPushMatrix()
    glRotatef(0,1,0,0)
    glRotatef(0,0,1,0)
    glRotatef(0,0,0,1)
    glBegin(GL_LINES)
    glColor3f (1.0, 0.0, 0.0) #red
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(100.0, 0.0, 0.0)
    glColor3f (0.0, 1.0, 0.0) #green
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)
    glColor3f (0.0, 0.0, 1.0) #blue
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 100.0)
    glEnd()
    glPopMatrix()
    ######################
    '''

    glPushMatrix()
    prism.draw()
    glPopMatrix()

    glPushMatrix()
    cube.draw()
    glPopMatrix()

def update(dt):
    global fovy,status,projection,angle,num

    if keys[pyglet.window.key.ENTER]:
        status = 1-status
        if status==1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    elif keys[pyglet.window.key.UP]:
        fovy -= 2
    elif keys[pyglet.window.key.DOWN]:
        fovy += 2
    elif keys[pyglet.window.key.LEFT]:
        angle += 5
    elif keys[pyglet.window.key.RIGHT]:
        angle -= 5
    elif keys[pyglet.window.key.F1]: '''generate isometric of object'''
        prism.angleX = -math.atan(20/(10*math.sqrt(2))) * 180/math.pi
        prism.angleZ = -45
    elif keys[pyglet.window.key.Q]:
        num+=1


pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()
