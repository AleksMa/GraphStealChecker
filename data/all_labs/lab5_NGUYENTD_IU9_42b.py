from pyglet import *
from pyglet.gl import *
from pyglet.window import key,mouse
import math

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getPoint(self):
        return (self.x,self.y)

class Line:
    def __init__(self):
        self.attr = []

    def getSize(self):
        return len(self.attr)

    def addPoint(self,pt):
        self.attr.append(pt)

    def getLine(self):
        return self.attr

class WhiteBoard:
    def __init__(self):
        self.lines = []
        self.nowLine = Line()
        self.outLines = []
        self.clipping = False
        self.xMax = 0
        self.yMax = 0
        self.xMin = 1600
        self.yMin = 900

    def add_lines(self,x,y):
        if self.nowLine.getSize() < 2:
            self.nowLine.addPoint(Point(x,y))
            if self.nowLine.getSize() == 2:
                self.lines.append(self.nowLine)
        else:
            self.nowLine = Line()
            self.nowLine.addPoint(Point(x,y))

    def drawRectangle(self):
        x0,y0 = 307,728
        x1,y1 = 1127,261
        self.xMin,self.xMax = min(x0,x1), max(x0,x1)
        self.yMin,self.yMax = min(y0,y1), max(y0,y1)
        glColor3f(0,0,0)
        glBegin(GL_LINES)
        glVertex2f(self.xMin,self.yMin)
        glVertex2f(self.xMin,self.yMax)
        glVertex2f(self.xMin,self.yMax)
        glVertex2f(self.xMax,self.yMax)
        glVertex2f(self.xMax,self.yMax)
        glVertex2f(self.xMax,self.yMin)
        glVertex2f(self.xMax,self.yMin)
        glVertex2f(self.xMin,self.yMin)
        glEnd()

    def lineClipping(self):

        def getCode(xMin,yMin,xMax,yMax,x,y):
            code = 0
            if x<xMin:
                code |= 1
            elif x>xMax:
                code |= 2
            elif y<yMin:
                code |= 4
            elif y>yMax:
                code |= 8
            return code

        def drawLine(x0,y0,x1,y1):
            glColor3f(0,0,0)
            glBegin(GL_LINES)
            glVertex2f(x0,y0)
            glVertex2f(x1,y1)
            glEnd()

        def Cohen_Sutherland(xMin,yMin,xMax,yMax,x0,y0,x1,y1):
            while 1==1:
                x,y = 0.0,0.0
                out = 0
                code0 = getCode(xMin,yMin,xMax,yMax,x0,y0)
                code1 = getCode(xMin,yMin,xMax,yMax,x1,y1)
                if code0 < code1:
                    out=code1
                else:
                    out=code0

                if code0&code1!=0:
                    drawLine(x0,y0,x1,y1)
                    break
                elif code0|code1==0:
                    break
                else:
                    if out&8!=0:
                        x = (yMax-y0)/(y1-y0) * (x1-x0) + x0
                        y = yMax
                    elif out&4!=0:
                        x = (yMin-y0)/(y1-y0) * (x1-x0) + x0
                        y = yMin
                    elif out&1!=0:
                        x = xMin
                        y = (xMin-x0)/(x1-x0) * (y1-y0) + y0
                    else:
                        x = xMax
                        y = (xMax-x0)/(x1-x0) * (y1-y0) + y0

                    if out==code0:
                        #drawLine(x0,y0,x,y)
                        line = Line()
                        line.addPoint(Point(x0,y0))
                        line.addPoint(Point(x,y))
                        self.outLines.append(line)
                        x0,y0=x,y
                    else:
                        #drawLine(x1,y1,x,y)
                        line = Line()
                        line.addPoint(Point(x1,y1))
                        line.addPoint(Point(x,y))
                        self.outLines.append(line)
                        x1,y1=x,y

        for p in self.lines:
            p1,p2 = p.getLine()[0],p.getLine()[1]
            x0,y0=p1.getPoint()
            x1,y1=p2.getPoint()
            Cohen_Sutherland(self.xMin,self.yMin,self.xMax,self.yMax,x0,y0,x1,y1)

    def drawLines(self):
        glBegin(GL_LINES)
        glColor3f(0,0,0)
        for p in self.lines:
            p1,p2 = p.getLine()[0],p.getLine()[1]
            glVertex2f(*p1.getPoint())
            glVertex2f(*p2.getPoint())
        glEnd()

    def drawOutput(self):
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        for p in self.outLines:
            p1,p2 = p.getLine()[0],p.getLine()[1]
            glVertex2f(*p1.getPoint())
            glVertex2f(*p2.getPoint())
        glEnd()


window = pyglet.window.Window(1600,900,resizable=True)
pyglet.gl.glClearColor(1,1,1,0)
white_board = WhiteBoard()

@window.event
def on_draw():
    window.clear()
    white_board.drawRectangle()
    if white_board.clipping:
        white_board.lineClipping()
        white_board.drawOutput()
    else:
        white_board.drawLines()


@window.event
def on_mouse_press(x,y,button,modifiers):
    if button & mouse.LEFT:
        white_board.add_lines(x,y)

@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.ENTER:
        white_board.clipping = True

@window.event
def on_resize(width,height):
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,width,0,height)
    glMatrixMode(GL_MODELVIEW)

pyglet.app.run()
