from pyglet import *
from pyglet.gl import *
from pyglet.window import key
import random, time
from PIL import Image
from math import *
import numpy as np
import pickle
import os

#fps_display = pyglet.clock.ClockDisplay()

class Point():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def sub(self,p):
        return Point(self.x - p.x, self.y - p.y, self.z -  p.z)

    def cross(self,p):
        return Point(self.y * p.z - self.z * p.y, self.z * p.x - self.x * self.z, self.x * p.y - self.y * p.x)

    def normalize(self,p2,p3):
        v1 = p2.sub(self)
        v2 = p3.sub(self)

        vn = p3.cross(p2)
        leng = sqrt(vn.x * vn.x + vn.y * vn.y + vn.z * vn.z)
        vn.x /= leng
        vn.y /= leng
        vn.z /= leng

        return vn

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
        self.mov_flag = 0
        ##coord matrix
        self.vertL = []
        self.vertU = []
        self.__partition = 20
        self.coordUD = []
        self.tex_coordUD = []
        self.coord = []
        self.tex_coord = []
        self.normalV = []
        ##movement
        self.g = 0.1
        self.trigger = 0
        self.s = Oy
        self.timeST = 0
        self.t = float(sqrt(2*self.s/self.g))
        ##display_list
        self.displayList = None
        self.enableDL = False

    def changeSize(self,coe):
        self.__partition = self.__partition + coe

    def calc(self,num):

        size_tex = self.__partition * 2 * num

        self.coordUD = np.zeros((self.__partition*self.__partition*4,int(num/2)+1,2), dtype = np.ndarray)
        self.tex_coordUD = np.zeros((self.__partition*self.__partition*4,int(num/2)+1,2), dtype = np.ndarray)

        self.coord = np.zeros((self.__partition*self.__partition*4,num), dtype = np.ndarray)
        self.tex_coord = np.zeros((self.__partition*self.__partition*4,num), dtype = np.ndarray)

        self.normalV = np.zeros(num+2, dtype = np.ndarray)

        self.vertL = []
        self.vertU = []
        for i in range(num):
            self.vertL.append((self.length*sin(i/num*2*pi),
                               self.length*cos(i/num*2*pi),
                               0))

            self.vertU.append((self.length*sin(i/num*2*pi),
                               self.length*cos(i/num*2*pi),
                               self.c))

        for typ in range(2):
            count = 0
            st1 = 0
            st2 = 0
            normalFin = [0.0,0.0,0.0]
            while 1==1:

                if abs(st2-st1)==1:
                    break

                i = (st1+1)%num
                j = (st2-1+num)%num
                print(st1,i,st2,j)
                if typ==0:
                    x1,y1,z1 = self.vertL[st1]
                    x2,y2,z2 = self.vertL[i]
                    x3,y3,z3 = self.vertL[st2]
                    x4,y4,z4 = self.vertL[j]
                else:
                    x1,y1,z1 = self.vertU[st1]
                    x2,y2,z2 = self.vertU[i]
                    x3,y3,z3 = self.vertU[st2]
                    x4,y4,z4 = self.vertU[j]

                    normal1 = Point(x1,y1,z1).normalize(Point(x2,y2,z2),Point(x3,y3,z3))
                    normal2 = Point(x1,y1,z2).normalize(Point(x3,y3,z3),Point(x4,y4,z4))


                    normalFin = [(normal1.x + normal2.x + normalFin[0])/3,(normal1.y + normal2.y + normalFin[1])/3,(normal1.z + normal2.z + normalFin[2])/3]

                for times in range(self.__partition):
                    x1o,y1o,z1o = x1 + (1.0 * (x2-x1)/self.__partition) * times,     y1 + (1.0* (y2-y1)/self.__partition) * times,z1
                    x1n,y1n,z1n = x1 + (1.0 * (x2-x1)/self.__partition) * (times+1), y1 + (1.0* (y2-y1)/self.__partition) * (times+1),z1
                    x2o,y2o,z2o = x3 + (1.0 * (x4-x3)/self.__partition) * times,     y3 + (1.0* (y4-y3)/self.__partition) * times,z3
                    x2n,y2n,z2n = x3 + (1.0 * (x4-x3)/self.__partition) * (times+1), y3 + (1.0* (y4-y3)/self.__partition) * (times+1),z3
                    step1,n_step1 = times / self.__partition, (times+1) / self.__partition

                    for ti in range(self.__partition):
                        _x1o,_y1o,_z1o = x1o + (x2o-x1o)/self.__partition * ti,     y1o + (y2o-y1o)/self.__partition * ti,z1o
                        _x1n,_y1n,_z1n = x1o + (x2o-x1o)/self.__partition * (ti+1), y1o + (y2o-y1o)/self.__partition * (ti+1),z1o
                        _x2o,_y2o,_z2o = x1n + (x2n-x1n)/self.__partition * ti,     y1n + (y2n-y1n)/self.__partition * ti,z2o
                        _x2n,_y2n,_z2n = x1n + (x2n-x1n)/self.__partition * (ti+1), y1n + (y2n-y1n)/self.__partition * (ti+1),z2o

                        step2,n_step2 = count * self.__partition + typ * (self.__partition * num / 2) + ti / size_tex, count * self.__partition + typ * (self.__partition * num / 2) + (ti+1) / size_tex

                        #if texture_flag:
                        #self.tex_coordUD[times,times+1,typ] = [step1,n_step1]
                        #print(self.coordUD[times,times+1,count,0])

                        pos = 4 * times * self.__partition + 4 * ti

                        self.tex_coordUD[pos+0,count,typ] = [step1,n_step1]
                        self.coordUD[pos + 0,count,typ] = [_x1o,_y1o,_z1o]

                        self.tex_coordUD[pos+1,count,typ] = [n_step1,n_step2]
                        self.coordUD[pos + 1,count,typ] = [_x1n,_y1n,_z1n]

                        self.tex_coordUD[pos+2,count,typ] = [n_step2,step2]
                        self.coordUD[pos + 2,count,typ] = [_x2n,_y2n,_z2n]

                        self.tex_coordUD[pos+3,count,typ] = [step2,step1]
                        self.coordUD[pos + 3,count,typ] = [_x2o,_y2o,_z2o]

                count+=1
                st1 = i
                st2 = j

                if st1==st2:
                    break
            self.normalV[typ] = normalFin

        for i in range(num):
            j=(i+1)%num

            x1,y1,z1 = self.vertL[i]
            x2,y2,z2 = self.vertL[j]
            x3,y3,z3 = self.vertU[i]
            x4,y4,z4 = self.vertU[j]

            normal1 = Point.normalize(Point(x1,y1,z1),Point(x2,y2,z2),Point(x4,y4,z4))
            normal2 = Point.normalize(Point(x1,y1,z2),Point(x4,y4,z4),Point(x3,y3,z3))

            normalN = [(normal1.x + normal2.x)/2,(normal1.y + normal2.y)/2,(normal1.z + normal2.z)/2]
            self.normalV[i + 2] = normalN


            for times in range(self.__partition):
                x11,y11,z11 = x1, y1,(1.0 * self.c / self.__partition) * times
                x12,y12,z12 = x1, y1,(1.0 * self.c / self.__partition) * (times+1)
                x21,y21,z21 = x2, y2,(1.0 * self.c / self.__partition) * times
                x22,y22,z22 = x2, y2,(1.0 * self.c / self.__partition) * (times+1)

                step1,n_step1 = times / self.__partition, (times+1) / self.__partition


                for ti in range(self.__partition):
                    _x11,_y11,_z11 = x1 + (x2-x1)/self.__partition * ti, y1 + (y2-y1)/self.__partition * ti,z11
                    _x12,_y12,_z12 = x1 + (x2-x1)/self.__partition * ti, y1 + (y2-y1)/self.__partition * ti,z12
                    _x21,_y21,_z21 = x1 + (x2-x1)/self.__partition * (ti+1), y1 + (y2-y1)/self.__partition * (ti+1),z21
                    _x22,_y22,_z22 = x1 + (x2-x1)/self.__partition * (ti+1), y1 + (y2-y1)/self.__partition * (ti+1),z22

                    step2,n_step2 = 1/2 + self.__partition * i + ti / size_tex, 1/2 + self.__partition * i + (ti+1) / size_tex

                    pos = 4 * times * self.__partition + 4 * ti

                    self.tex_coord[pos + 0 , i] = [step1,n_step1]
                    self.coord[pos + 0 , i] = [_x11,_y11,_z11]

                    self.tex_coord[pos + 1 , i] = [n_step1,n_step2]
                    self.coord[pos + 1 , i] = [_x12,_y12,_z12]

                    self.tex_coord[pos + 2 , i] = [n_step2,step2]
                    self.coord[pos + 2 , i] = [_x22,_y22,_z22]

                    self.tex_coord[pos + 3 , i] = [step2,step1]
                    self.coord[pos + 3 , i] = [_x21,_y21,_z21]

    def genDisplayList(self,light_flag,texture_flag):

        def proc():
            #glEnable(GL_NORMALIZE)
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
                if light_flag:
                    glNormal3f(*(GLfloat * 3)(*self.normalV[0]))
                if texture_flag:
                    glColor3f(1,1,1)
                else:
                    glColor3f(cA/255,cB/255,cC/255)

                count = 0
                st1 = 0
                st2 = 0
                while 1==1:

                    if abs(st2-st1)==1:
                        break

                    i = (st1+1)%num
                    j = (st2-1+num)%num

                    for times in range(self.__partition):
                        for ti in range(self.__partition):
                            '''
                            if times==0 and ti ==1:
                                glColor3f(1,1,1)
                            else:
                                glColor3f(cA/255,cB/255,cC/255)
                            '''
                            pos = 4 * times * self.__partition + 4 * ti


                            template = [self.Ox,self.Oy,self.Oz]

                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 0,count,0]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 0,count,0])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 1,count,0]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 1,count,0])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 2,count,0]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 2,count,0])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 3,count,0]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 3,count,0])))


                    count+=1
                    st1 = i
                    st2 = j

                    if st1==st2:
                        break;

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
                if light_flag:
                    glNormal3f(*(GLfloat * 3)(*self.normalV[1]))
                if texture_flag:
                    glColor3f(1,1,1)
                else:
                    glColor3f(cA/255,cB/255,cC/255)

                count = 0
                st1 = 0
                st2 = 0
                while 1==1:

                    if abs(st2-st1)==1:
                        break

                    i = (st1+1)%num
                    j = (st2-1+num)%num

                    for times in range(self.__partition):
                        for ti in range(self.__partition):
                            '''
                            if times==0 and ti ==1:
                                glColor3f(1,1,1)
                            else:
                                glColor3f(cA/255,cB/255,cC/255)
                            '''
                            pos = 4 * times * self.__partition + 4 * ti

                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 0,count,1]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 0,count,1])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 1,count,1]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 1,count,1])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 2,count,1]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 2,count,1])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coordUD[pos + 3,count,1]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coordUD[pos + 3,count,1])))

                    count+=1
                    st1 = i
                    st2 = j

                    if st1==st2:
                        break;

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
                    if light_flag:
                        glNormal3f(*(GLfloat * 3)(*self.normalV[i+2]))

                    if texture_flag:
                        glColor3f(1,1,1)
                    else:
                        glColor3f(cA/255,cB/255,cC/255)


                    for times in range(self.__partition):
                        for ti in range(self.__partition):

                            pos = 4 * times * self.__partition + 4 * ti

                            template = [self.Ox,self.Oy,self.Oz]

                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coord[pos + 0,i]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coord[pos + 0,i])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coord[pos + 1,i]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coord[pos + 1,i])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coord[pos + 2,i]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coord[pos + 2,i])))
                            if texture_flag:
                                glTexCoord2f(*(GLfloat * 2)(*self.tex_coord[pos + 3,i]))
                            glVertex3fv((GLfloat * 3)(*map(lambda x,y : x + y, template, self.coord[pos + 3,i])))
                    glEnd()

        if self.enableDL:
            _id = glGenLists(1)
            self.displayList = _id
            if _id != 0:
                glNewList(_id,GL_COMPILE)
                proc()
                glEndList()
        else:
            proc()
    def draw(self,light_flag,texture_flag):
        glTranslatef(self.Ox,self.Oy,self.Oz)
        glRotatef(self.angleX,1,0,0)
        glRotatef(self.angleY,0,1,0)
        glRotatef(self.angleZ,0,0,1)
        glTranslatef(-self.Ox,-self.Oy,-self.Oz)
        self.genDisplayList(light_flag,texture_flag)

        if self.enableDL:
            glCallList(self.displayList)


    def update(self):
        if self.mov_flag==0:
            return
        s = float(1/2*self.g*(time.time()-self.timeST)*(time.time()-self.timeST))
        #print(s,self.timeST)
        if float(self.s)-s>=0.0 and float(self.s)-s<=0.1:
            self.trigger = 1
        elif s-float(self.s)>=0.0 and 2*float(self.s)-s<=0.1:
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

        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_ALPHA_ARB, GL_REPLACE )
        glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_RGB, GL_MODULATE)
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE0_RGB, GL_PREVIOUS);
        glTexEnvi(GL_TEXTURE_ENV, GL_SOURCE1_RGB, GL_TEXTURE);
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND0_RGB, GL_SRC_COLOR);
        glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND1_RGB, GL_SRC_COLOR);

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
        self.ambient_light0 = [0.2,0.2,0.2,1]
        self.diffuse_light0 = [0.8,0.8,0.8,1]
        self.specular_light0 = [1,1,1,1]
        self.position_light0 = [.4,.95,.9,1]

        self.ambient_light1 = [0.2,0.2,0.2,1]
        self.diffuse_light1 = [0.8,0.8,0.8,1]
        self.specular_light1 = [1,1,1,1]
        self.position_light1 = [.4,1.05,.8,1]
        self.spot_direction_light1 = [0,1,-1]

        #diffuse_material = [64/255,150/255,165/255,1]
        #ambient_material = [64/255,150/255,165/255,1]
        self.specular_material = [1,1,1,1]
        self.shininess_material = 20

    def init(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        glLightfv(GL_LIGHT0,GL_DIFFUSE,(GLfloat * 4)(*self.diffuse_light0))
        glLightfv(GL_LIGHT0,GL_AMBIENT,(GLfloat * 4)(*self.ambient_light0))
        glLightfv(GL_LIGHT0,GL_SPECULAR,(GLfloat * 4)(*self.specular_light0))
        glLightfv(GL_LIGHT0,GL_POSITION,(GLfloat * 4)(*self.position_light0))

        glLightfv(GL_LIGHT1,GL_DIFFUSE,(GLfloat * 4)(*self.diffuse_light1))
        glLightfv(GL_LIGHT1,GL_AMBIENT,(GLfloat * 4)(*self.ambient_light1))
        glLightfv(GL_LIGHT1,GL_SPECULAR,(GLfloat * 4)(*self.specular_light1))
        glLightfv(GL_LIGHT1,GL_POSITION,(GLfloat * 4)(*self.position_light1))
        glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, (GLfloat)(25.0))
        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, (GLfloat * 3)(*self.spot_direction_light1))
        glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, (GLfloat)(2))

        glShadeModel (GL_SMOOTH)

        glEnable(GL_COLOR_MATERIAL)
        #glMaterialfv(GL_FRONT,GL_DIFFUSE,(GLfloat * 4)(*diffuse_material))
        #glMaterialfv(GL_FRONT,GL_AMBIENT,(GLfloat * 4)(*ambient_material))
        glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT,GL_SPECULAR,(GLfloat * 4)(*self.specular_material))
        glMaterialfv(GL_FRONT,GL_SHININESS,(GLfloat)(self.shininess_material))

    def disable(self):
        glDisable(GL_LIGHTING)

class Serial:
    def __init__(self,name="save_attr.pickle"):
        self.name = name
        if not os.path.exists("save_attr.pickle"):
            open(self.name,mode="w").close()


    def load(self):
        with open(self.name,mode="rb") as file:
            #mesh
            prism.c = pickle.load(file)
            prism.angleX = pickle.load(file)
            prism.angleY = pickle.load(file)
            prism.angleZ = pickle.load(file)
            prism.length = pickle.load(file)
            prism.Ox = pickle.load(file)
            prism.Oy = pickle.load(file)
            prism.Oz = pickle.load(file)
            prism.__partition = pickle.load(file)
            prism.g = pickle.load(file)
            prism.s = pickle.load(file)
            prism.t = pickle.load(file)
            #texture
            texture.image = pickle.load(file)
            #lights
            light.ambient_light0 = pickle.load(file)
            light.diffuse_light0 = pickle.load(file)
            light.specular_light0 = pickle.load(file)
            light.position_light0 = pickle.load(file)
            light.ambient_light1 = pickle.load(file)
            light.diffuse_light1 = pickle.load(file)
            light.specular_light1 = pickle.load(file)
            light.position_light1 = pickle.load(file)
            light.spot_direction_light1 = pickle.load(file)
            light.specular_material = pickle.load(file)
            light.shininess_material = pickle.load(file)

    def save(self):
        with open(self.name,mode="wb") as file:
            #mesh
            pickle.dump(prism.c,file)
            pickle.dump(prism.angleX,file)
            pickle.dump(prism.angleY,file)
            pickle.dump(prism.angleZ,file)
            pickle.dump(prism.length,file)
            pickle.dump(prism.Ox,file)
            pickle.dump(prism.Oy,file)
            pickle.dump(prism.Oz,file)
            pickle.dump(prism.__partition,file)
            pickle.dump(prism.g,file)
            pickle.dump(prism.s,file)
            pickle.dump(prism.t,file)
            #texture
            pickle.dump(texture.image,file)
            #lights
            pickle.dump(light.ambient_light0,file)
            pickle.dump(light.diffuse_light0,file)
            pickle.dump(light.specular_light0,file)
            pickle.dump(light.position_light0,file)
            pickle.dump(light.ambient_light1,file)
            pickle.dump(light.diffuse_light1,file)
            pickle.dump(light.specular_light1,file)
            pickle.dump(light.position_light1,file)
            pickle.dump(light.spot_direction_light1,file)
            pickle.dump(light.specular_material,file)
            pickle.dump(light.shininess_material,file)


window = pyglet.window.Window(width=1600, height=900)

prism = Prism(0.5,"img/pic.jpg")
cube = Cube(0.3,0,0.3)
status = 0
num = 3
light = Light()
texture = Texture()
serial = Serial()
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
    glVertex3d(.1, 0.0, 0.0);

    glColor3d(0.0, 1.0, 0.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, .1, 0.0);

    glColor3d(0.0, 0.0, 1.0);
    glVertex3d(0.0, 0.0, 0.0);
    glVertex3d(0.0, 0.0, .1);

    glEnd();

    if light.Flag:
        light.init()
    else:
        light.disable()

    texture.open_image(os.path.join(os.getcwd(),"img","pic.png"))
    texture.load_texture()

    #fps.draw()

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
    elif symbol == key.F1:
        prism.changeSize(5)
        prism.calc(num)
    elif symbol == key.F2:
        prism.changeSize(-5)
        prism.calc(num)
    elif symbol == key.Z:
        prism.enableDL ^= 1
    elif symbol == key.L:
        serial.load()
    elif symbol == key.O:
        serial.save()

def update(dt):
    prism.update()

pyglet.clock.schedule_interval(update,1/100)
pyglet.app.run()
