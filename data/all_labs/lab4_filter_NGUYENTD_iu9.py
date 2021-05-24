from pyglet import *
from pyglet.gl import *
from pyglet.window import key,mouse
import math,random
import numpy as np

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getPoint(self):
        return (self.x,self.y)

class Frame:
    def __init__(self,width,height):
        self.points = []
        self.width = width
        self.height = height
        self.pixels = np.empty(self.width*self.height*3,dtype=GLfloat)
        self.pixels.fill(1.0)
        self.fill = False
        self.AA = False
        self.drawOne = True

    def add_point(self,x,y):
        self.points.append(Point(x,y))
        print(self.points[len(self.points)-1].getPoint())
        #print(len(self.points))

    def draw_points(self):
        glColor3f(0,0,0)
        if len(self.points)>1:
            if self.fill or self.AA:
                if self.AA:
                    self.antiAliasing()
                    self.AA = False
                else:
                    self.fillPolygon()
                    self.fill = False

                glDrawPixels(self.width,self.height,GL_RGB,GL_FLOAT,(GLfloat * len(self.pixels))(*self.pixels))

        if self.drawOne:
            if self.fill:
                self.drawOne = False
            for i in range(len(self.points)):
                if i == len(self.points)-1:
                    glBegin(GL_LINES)
                    glVertex2f(*self.points[i].getPoint())
                    glVertex2f(*self.points[0].getPoint())
                    glEnd()
                    break
                glBegin(GL_LINES)
                glVertex2f(*self.points[i].getPoint())
                glVertex2f(*self.points[i+1].getPoint())
                glEnd()


    def invert(self,x,y):
        pos = y*self.width+x
        for i in range(3):
            self.pixels[pos*3+i] = 1 - self.pixels[pos*3+i]

    def antiAliasing(self):
        print('Starting anti-aliasing, wait a bit')
        width_o = self.width
        height_o = self.height
        kernel = [[1,2,1],[2,4,2],[1,2,1]]
        pixels_o = np.empty(width_o*height_o*3,dtype=GLfloat)
        pixels_o.fill(0.0)

        for x in range(width_o):
            for y in range(height_o):
                pos_o = y*width_o+x

                for i in range(3):
                    for j in range(3):
                        i = i - 1
                        j = j - 1
                        if y+j < 0 or y+j >= height_o or x+i < 0 or x+i >= width_o:
                            continue
                        pos = (y+j) * self.width + (x+i)
                        pixels_o[3*pos_o+0] += self.pixels[3*pos + 0] * kernel[i][j] / 16.0
                        pixels_o[3*pos_o+1] += self.pixels[3*pos + 1] * kernel[i][j] / 16.0
                        pixels_o[3*pos_o+2] += self.pixels[3*pos + 2] * kernel[i][j] / 16.0

        self.pixels = np.empty(width_o*height_o*3,dtype=GLfloat)
        self.pixels = np.copy(pixels_o)
        print(self.pixels)
        self.width = width_o
        self.height = height_o
        print('DONE anti-aliasing')


    def fillPolygon(self):
        #print('Filling polygon in this frame atm',factor)


        def fillByEdge(x0,y0,x1,y1,xPartition):
            if y0>y1:
                x0,y0,x1,y1 = x1,y1,x0,y0

            xmin,xmax = min(x0,x1),max(x0,x1)

            for y in range(y0,y1):
                x = math.ceil((y-y0)/(y1-y0) * (x1-x0) + x0)
                if x<xPartition:
                    for x3 in range(x,xPartition):
                        self.invert(x3,y)
                else:
                    for x3 in range(xPartition,x):
                        self.invert(x3,y)


        xMin,xMax = 1000,0
        for i in range(len(self.points)):
            x0,y0 = self.points[i].getPoint()
            x0,y0 = x0,y0
            xMin,xMax = min(xMin,x0), max(xMax,x0)
        xPartition = random.randint(xMin,xMax)

        for i in range(len(self.points)):
            if i == len(self.points)-1:
                x0,y0 = self.points[i].getPoint()
                x1,y1 = self.points[0].getPoint()
            else:
                x0,y0 = self.points[i].getPoint()
                x1,y1 = self.points[i+1].getPoint()

            x0,y0 = x0,y0
            x1,y1 = x1,y1
            fillByEdge(x0,y0,x1,y1,xPartition)



window = pyglet.window.Window(800,600, resizable=True)
pyglet.gl.glClearColor(1,1,1,0)
frame = Frame(800,600)

@window.event
def on_draw():
    window.clear()
    frame.draw_points()

@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.ENTER:
        frame.fill = True
    elif symbol == key.SPACE:
        frame.AA = True


@window.event
def on_mouse_press(x,y,button,modifiers):
    if button & mouse.LEFT:
        frame.add_point(x,y)

@window.event
def on_resize(width,height):
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,width,0,height)
    glMatrixMode(GL_MODELVIEW)

pyglet.app.run()
