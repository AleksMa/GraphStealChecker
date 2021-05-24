from pyglet import *
from pyglet.gl import *
from pyglet.window import key
import random, time
from PIL import Image
from math import *


class Prism:
    def __init__(self,c,texturefile,angleX=0,angleY=0,angleZ=0,Ox=0.4,Oy=1.2,Oz=0.6): #.5 1 .6
        self.c = c
        self.angleX = angleX
        self.angleY = angleY
        self.angleZ = angleZ
        self.length = 0.15
        self.Ox = Ox
        self.Oy = Oy
        self.Oz = Oz
        self.vertL = []
        self.vertU = []
        self.__partition = 20
        self.mov_flag = 0
        ##movement
        self.g = 0.05
        self.trigger = 0
        self.s = Oy
        self.timeST = 0
        self.t = float(sqrt(2*self.s/self.g))

    def calc(self,num):
        self.vertL = []
        self.vertU = []
        for i in range(num):
            self.vertL.append((self.length*sin(i/num*2*pi),
                               self.length*cos(i/num*2*pi),
                               0))

            self.vertU.append((self.length*sin(i/num*2*pi),
                               self.length*cos(i/num*2*pi),
                               self.c))


    def draw(self,light_flag,texture_flag):
        glTranslatef(self.Ox,self.Oy,self.Oz)
        glRotatef(self.angleX,1,0,0)
        glRotatef(self.angleY,0,1,0)
        glRotatef(self.angleZ,0,0,1)
        glTranslatef(-self.Ox,-self.Oy,-self.Oz)
        cA = 123
        cB = 213
        cC = 12
        cA = (cA + 100)%255
        cB = (cB - 75 + 255)%255
        cC = (cC + 324)%255
        '''1'''
        if light_flag==False and texture_flag==False:
            glBegin(GL_POLYGON)
            glColor3f(cA/255,cB/255,cC/255)
            for i in range(num):
                x,y,z = self.vertL[i]
                glVertex3f(x+self.Ox,y+self.Oy,z+self.Oz)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glNormal3f(0.0,0.0,1.0)
            if texture_flag:
                glColor3f(1,1,1)
            else:
                glColor3f(cA/255,cB/255,cC/255)

            for i in range(num):
                j=(i+1)%num

                z0 = 0
                x1_e,y1_e,z1_e = self.vertL[i]
                x2_e,y2_e,z2_e = self.vertL[j]

                for times in range(self.__partition):
                    x11,y11,z11 = (1.0 * x1_e/self.__partition) * times, (1.0* y1_e/self.__partition) * times,z1_e
                    x12,y12,z12 = (1.0 * x1_e/self.__partition) * (times+1), (1.0* y1_e/self.__partition) * (times+1),z1_e
                    x21,y21,z21 = (1.0 * x2_e/self.__partition) * times, (1.0* y2_e/self.__partition) * times,z2_e
                    x22,y22,z22 = (1.0 * x2_e/self.__partition) * (times+1), (1.0* y2_e/self.__partition) * (times+1),z2_e
                    step1,n_step1 = times / self.__partition, (times+1) / self.__partition
                    '''
                    glVertex3f(x11+self.Ox,y11+self.Oy,z11+self.Oz)
                    glVertex3f(x12+self.Ox,y12+self.Oy,z12+self.Oz)
                    glVertex3f(x22+self.Ox,y22+self.Oy,z22+self.Oz)
                    glVertex3f(x21+self.Ox,y21+self.Oy,z21+self.Oz)
                    '''
                    for ti in range(self.__partition):
                        _x11,_y11,_z11 = x11 + (x21-x11)/self.__partition * ti, y11 + (y21-y11)/self.__partition * ti,z11
                        _x12,_y12,_z12 = x12 + (x22-x12)/self.__partition * ti, y12 + (y22-y12)/self.__partition * ti,z12
                        _x21,_y21,_z21 = x11 + (x21-x11)/self.__partition * (ti+1), y11 + (y21-y11)/self.__partition * (ti+1),z21
                        _x22,_y22,_z22 = x12 + (x22-x12)/self.__partition * (ti+1), y12 + (y22-y12)/self.__partition * (ti+1),z22

                        step2,n_step2 = ti / self.__partition, (ti+1) / self.__partition

                        if texture_flag:
                            glTexCoord2f(step1,n_step1)
                        glVertex3f(_x11+self.Ox,_y11+self.Oy,_z11+self.Oz)
                        if texture_flag:
                            glTexCoord2f(n_step1,n_step2)
                        glVertex3f(_x12+self.Ox,_y12+self.Oy,_z12+self.Oz)
                        if texture_flag:
                            glTexCoord2f(n_step2,step2)
                        glVertex3f(_x22+self.Ox,_y22+self.Oy,_z22+self.Oz)
                        if texture_flag:
                            glTexCoord2f(step2,step1)
                        glVertex3f(_x21+self.Ox,_y21+self.Oy,_z21+self.Oz)

            glEnd()
        '''2'''
        cA = (cA + 4312)%255
        cB = (cB - 124 + 255)%255
        cC = (cC - 123 + 255)%255

        if light_flag==False and texture_flag==False:
            glBegin(GL_POLYGON)
            glColor3f(cA/255,cB/255,cC/255)
            for i in range(num):
                x,y,z = self.vertU[i]
                glVertex3f(x+self.Ox,y+self.Oy,z+self.Oz)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glNormal3f(0.0,0.0,1.0)
            if texture_flag:
                glColor3f(1,1,1)
            else:
                glColor3f(cA/255,cB/255,cC/255)
            for i in range(num):
                j=(i+1)%num

                z0 = 0
                x1_e,y1_e,z1_e = self.vertU[i]
                x2_e,y2_e,z2_e = self.vertU[j]

                for times in range(self.__partition):
                    x11,y11,z11 = (1.0 * x1_e/self.__partition) * times, (1.0* y1_e/self.__partition) * times,z1_e
                    x12,y12,z12 = (1.0 * x1_e/self.__partition) * (times+1), (1.0* y1_e/self.__partition) * (times+1),z1_e
                    x21,y21,z21 = (1.0 * x2_e/self.__partition) * times, (1.0* y2_e/self.__partition) * times,z2_e
                    x22,y22,z22 = (1.0 * x2_e/self.__partition) * (times+1), (1.0* y2_e/self.__partition) * (times+1),z2_e
                    glVertex3f(x11+self.Ox,y11+self.Oy,z11+self.Oz)
                    glVertex3f(x12+self.Ox,y12+self.Oy,z12+self.Oz)
                    glVertex3f(x22+self.Ox,y22+self.Oy,z22+self.Oz)
                    glVertex3f(x21+self.Ox,y21+self.Oy,z21+self.Oz)
            glEnd()

        '''3'''
        for i in range(num):
            cA = (cA + 1243)%255
            cB = (cB + 112323)%255
            cC = (cC - 21201 + 255)%255
            j=(i+1)%num
            if light_flag==False and texture_flag==False:
                glBegin(GL_QUADS)
                glColor3f(cA/255,cB/255,cC/255)
                x,y,z = self.vertL[i]
                glVertex3f(x+self.Ox,y+self.Oy,z+self.Oz)
                x,y,z = self.vertL[j]
                glVertex3f(x+self.Ox,y+self.Oy,z+self.Oz)
                x,y,z = self.vertU[j]
                glVertex3f(x+self.Ox,y+self.Oy,z+self.Oz)
                x,y,z = self.vertU[i]
                glVertex3f(x+self.Ox,y+self.Oy,z+self.Oz)
                glEnd()
            else:
                glBegin(GL_QUADS)
                glNormal3f(0.0,0.0,1.0)
                if texture_flag:
                    glColor3f(1,1,1)
                else:
                    glColor3f(cA/255,cB/255,cC/255)

                x1,y1,z1 = self.vertL[i]
                x2,y2,z2 = self.vertL[j]

                for times in range(self.__partition):
                    x11,y11,z11 = x1, y1,(1.0 * self.c / self.__partition) * times
                    x12,y12,z12 = x1, y1,(1.0 * self.c / self.__partition) * (times+1)
                    x21,y21,z21 = x2, y2,(1.0 * self.c / self.__partition) * times
                    x22,y22,z22 = x2, y2,(1.0 * self.c / self.__partition) * (times+1)

                    step1,n_step1 = times / self.__partition, (times+1) / self.__partition

                    '''
                    glVertex3f(x11+self.Ox,y11+self.Oy,z11+self.Oz)
                    glVertex3f(x12+self.Ox,y12+self.Oy,z12+self.Oz)
                    glVertex3f(x22+self.Ox,y22+self.Oy,z22+self.Oz)
                    glVertex3f(x21+self.Ox,y21+self.Oy,z21+self.Oz)
                    '''
                    for ti in range(self.__partition):
                        _x11,_y11,_z11 = x1 + (x2-x1)/self.__partition * ti, y1 + (y2-y1)/self.__partition * ti,z11
                        _x12,_y12,_z12 = x1 + (x2-x1)/self.__partition * ti, y1 + (y2-y1)/self.__partition * ti,z12
                        _x21,_y21,_z21 = x1 + (x2-x1)/self.__partition * (ti+1), y1 + (y2-y1)/self.__partition * (ti+1),z21
                        _x22,_y22,_z22 = x1 + (x2-x1)/self.__partition * (ti+1), y1 + (y2-y1)/self.__partition * (ti+1),z22

                        step2,n_step2 = ti / self.__partition, (ti+1) / self.__partition

                        if texture_flag:
                            glTexCoord2f(step1,n_step1)
                        glVertex3f(_x11+self.Ox,_y11+self.Oy,_z11+self.Oz)
                        if texture_flag:
                            glTexCoord2f(n_step1,n_step2)
                        glVertex3f(_x12+self.Ox,_y12+self.Oy,_z12+self.Oz)
                        if texture_flag:
                            glTexCoord2f(n_step2,step2)
                        glVertex3f(_x22+self.Ox,_y22+self.Oy,_z22+self.Oz)
                        if texture_flag:
                            glTexCoord2f(step2,step1)
                        glVertex3f(_x21+self.Ox,_y21+self.Oy,_z21+self.Oz)
                glEnd()

    def update(self):
        if self.mov_flag==0:
            return
        s = float(1/2*self.g*(time.time()-self.timeST)*(time.time()-self.timeST))
        #print(s,self.timeST)
        if float(self.s)-s>=0.0 and float(self.s)-s<=0.05:
            self.trigger = 1
        elif s-float(self.s)>=0.0 and 2*float(self.s)-s<=0.05:
            self.timeST = time.time()
            self.trigger = 0
            s = 0
        if self.trigger==0:
            self.Oy = self.s - s
        elif self.trigger==1:
            self.Oy = s - self.s

class Texture:

    def __init__(self):
        self.textures = []
        self.image = None
        self.index_active_texture = -1
        self.flag = False


    def load_texture(self):
        if self.flag:
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)
            return None

        if self.textures == []:
            return None

        glEnable(self.textures[self.index_active_texture].target)
        glBindTexture(self.textures[self.index_active_texture].target,self.textures[self.index_active_texture].id)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)

        # Repeat of texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)


        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,self.image.width,self.image.height,0,
                     GL_RGBA,GL_UNSIGNED_BYTE,self.image.get_image_data().get_data("RGBA",self.image.width*len("RGBA")))


    def open_image(self,name):
        self.image = pyglet.image.load(name)
        self.textures.append(self.image.get_texture())
        self.index_active_texture = len(self.textures)-1


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

class Light:
    def __init__(self):
        self.Flag = False

    def init(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        ambient_light0 = [0.2,0.2,0.2,1]
        diffuse_light0 = [0.8,0.8,0.8,1]
        specular_light0 = [1,1,1,1]
        position_light0 = [.4,.95,.9,1]
        #position_light0 = [.5,1,.65,1]
        #position_light0 = [.6,1.1,1.05,1]

        glLightfv(GL_LIGHT0,GL_DIFFUSE,(GLfloat * 4)(*diffuse_light0))
        glLightfv(GL_LIGHT0,GL_AMBIENT,(GLfloat * 4)(*ambient_light0))
        glLightfv(GL_LIGHT0,GL_SPECULAR,(GLfloat * 4)(*specular_light0))
        glLightfv(GL_LIGHT0,GL_POSITION,(GLfloat * 4)(*position_light0))

        ambient_light1 = [0.2,0.2,0.2,1]
        diffuse_light1 = [0.8,0.8,0.8,1]
        specular_light1 = [1,1,1,1]
        position_light1 = [.4,1.05,.8,1]

        spot_direction_light1 = [0,1,-1]
        glLightfv(GL_LIGHT1,GL_DIFFUSE,(GLfloat * 4)(*diffuse_light1))
        glLightfv(GL_LIGHT1,GL_AMBIENT,(GLfloat * 4)(*ambient_light1))
        glLightfv(GL_LIGHT1,GL_SPECULAR,(GLfloat * 4)(*specular_light1))
        glLightfv(GL_LIGHT1,GL_POSITION,(GLfloat * 4)(*position_light1))
        glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, (GLfloat)(25.0))
        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, (GLfloat * 3)(*spot_direction_light1))
        glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, (GLfloat)(2))

        glShadeModel (GL_SMOOTH)

        glEnable(GL_COLOR_MATERIAL)
        #diffuse_material = [64/255,150/255,165/255,1]
        #ambient_material = [64/255,150/255,165/255,1]
        specular_material = [1,1,1,1]
        shininess_material = 80
        #glMaterialfv(GL_FRONT,GL_DIFFUSE,(GLfloat * 4)(*diffuse_material))
        #glMaterialfv(GL_FRONT,GL_AMBIENT,(GLfloat * 4)(*ambient_material))
        glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT,GL_SPECULAR,(GLfloat * 4)(*specular_material))
        glMaterialfv(GL_FRONT,GL_SHININESS,(GLfloat)(shininess_material))

    def disable(self):
        glDisable(GL_LIGHTING)


window = pyglet.window.Window(width=1600, height=900)

prism = Prism(0.5,"img/pic.png")
cube = Cube(0.3,0,0.3)
status = 0
num = 3
light = Light()
texture = Texture()
prism.calc(num)

@window.event
def on_draw():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    '''this length so that camera is 1 unit away from origin'''
    dist = sqrt(1 / 3.0) #'''1/sqrt(3) = arctan(30)'''

    gluLookAt(dist, dist, dist, #'''pos of camera'''
          0.0,  0.0,  0.0, #'''pos which camera look at'''
          0.0,  1.0,  0.0) #'''direction'''




    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(0,0,0,0);
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST) # Enable depth testing for z-culling

    glBegin(GL_LINES);

    glColor3d(1.0, 0.0, 0.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(1.0, 0.0, 0.0);

    glColor3d(0.0, 1.0, 0.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, 1.0, 0.0);

    glColor3d(0.0, 0.0, 1.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, 0.0, 1.0);

    glEnd();

    if light.Flag:
        light.init()
    else:
        light.disable()

    texture.open_image(os.path.join(os.getcwd(),"img","pic.png"))
    texture.load_texture()

    glPushMatrix()
    prism.draw(light.Flag,texture.flag)
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
    elif symbol == key.L:
        light.Flag ^= 1
    elif symbol == key.M:
        prism.mov_flag ^= 1
        prism.timeST = time.time()
    elif symbol == key.T:
        texture.flag ^= 1

def update(dt):
    prism.update()

pyglet.clock.schedule_interval(update,1/100)
pyglet.app.run()
