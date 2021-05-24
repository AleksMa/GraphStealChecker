
from pyglet import *
from pyglet.gl import *
from pyglet.window import key, mouse
import math
import numpy

height, width = 600, 600
window = pyglet.window.Window(height, width, resizable=True) #размер окна
pyglet.gl.glClearColor(0, 0, 0, 0) #цвет фона
pixels = numpy.empty(3 * height * width, dtype=float)
pixels.fill(0.0)
points = []
stack = []
clockwiseDirection = True
shapeIsDrawn = False
pointsUpdated = False

def appendPoint(x, y):
    global points, clockwiseDirection, pointsUpdated
    pointsUpdated = True
    len_prev = len(points)
    points.append((x,y))
    if len_prev > 1:
        p1, p2, p3 = points[len_prev - 2], points[len_prev - 1], points[len_prev]
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        x3, y3 = p3[0], p3[1]
        clockwiseDirection = ((x3 - x1) * (y2 - y1)) -((y3 - y1) * (x2 - x1)) > 0

def clearPixels():
    global pixels, height, width, shapeIsDrawn, outlineFiltered
    pixels.fill(0.0)
    shapeIsDrawn = False

def setBrightness(x, y, value):
    global pixels, height, width
    for i in range(3):
        pixels[3 * (y * width + x) + i] = value

def setGreenGlow(x, y, value):
    global pixels, height, width
    for i in range(3):
        pixels[3 * (y * width + x) + i] = 0.0
    pixels[3 * (y * width + x) + 1] = value

def wu(x0, y0, x1, y1, aa):
    dx, dy = x1 - x0, y1 - y0
    steep = abs(dy) > abs(dx)

    setBrightness(x0, y0, 1.0)
    setBrightness(x1, y1, 1.0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        dx, dy = dy, dx

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        dx, dy = -dx, -dy

    sign_y = 1 if dy > 0 else -1
    dy = abs(dy)

    e = dx // 2
    y = y0

    for x in range(x0, x1 + 1):
        intensity = float(e) / float(dx)
        int
        setBrightness(y if steep else x, x if steep else y, intensity if aa else 1.0)
        if aa:
            setBrightness(y + sign_y if steep else x, x if steep else y + sign_y, (1.0 - intensity))
        e -= dy
        if e < 0:
            y += sign_y
            e += dx

def brezenhem(x0, y0, x1, y1, aa):
    '''Clockwise'''
    dx, dy = x1 - x0, y1 - y0
    setBrightness(x0, y0, 1.0)
    setBrightness(x1, y1, 1.0)

    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1
    dx, dy = abs(dx), abs(dy)
    shapeIsLeftward = (sign_x == 1) ^ (sign_y == 1) ^ (dy > dx)
    colorDepth = 10
    if dx > dy:
        m = colorDepth * dy
        e = dx // 2
        w = colorDepth * dx - m
        y = y0

        for x in range(x0, x1, sign_x):
            if e < w:
                e += m
            else:
                y += sign_y
                e -= w
            intensity = float(e) / float(dx * colorDepth)
            intensity = 1.0 - intensity if shapeIsLeftward else intensity
            setBrightness(x, y, intensity if aa else 1.0)
    else:
        m = colorDepth * dx
        e = dy // 2
        w = colorDepth * dy - m
        x = x0
        for y in range(y0, y1, sign_y):
            if e < w:
                e += m
            else:
                x += sign_x
                e -= w
            intensity = float(e) / float(dy * colorDepth)
            intensity = 1.0 - intensity if shapeIsLeftward else intensity
            setBrightness(x, y, intensity if aa else 1.0)

def connectPoints(aa):
    global points, clockwiseDirection, pointsUpdated, shapeIsDrawn
    if pointsUpdated:
            clearPixels()
            pointsUpdated = False
    if not shapeIsDrawn:
        clearPixels()
    len_p = len(points)

    if clockwiseDirection:
        start, end, step = 0, len_p - 1, 1
        if len_p > 2:
            p1, p2 = points[len_p - 1], points[0]
            drawLine(p1[0], p1[1], p2[0], p2[1], aa)
    else:
        start, end, step = len_p - 1, 0, -1
        if len_p > 2:
            p1, p2 = points[len_p - 1], points[0]
            drawLine(p1[0], p1[1], p2[0], p2[1], aa)
    for i in range(start, end, step):
        p1, p2 = points[i], points[i + step]
        drawLine(p1[0], p1[1], p2[0], p2[1], aa)

def drawLine(x0, y0, x1, y1, aa):
    global shapeIsDrawn
    if shapeIsDrawn:
        brezenhem(x0, y0, x1, y1, aa)
    else:
        if aa:
            wu(x0, y0, x1, y1, aa)
        else:
            brezenhem(x0, y0, x1, y1, False)

def drawPixels():
    global pixels, height, width
    glDrawPixels(height, width, GL_RGB, GL_FLOAT, (GLfloat * len(pixels))(*pixels))

def fill(x, y):
    global height, width, pixels, shapeIsDrawn, stack
    clearPixels()
    connectPoints(False)
    stack.append((x,y))
    while len(stack) != 0:
        p = stack.pop()
        x, y = p[0], p[1]
        while x >= 0 and pixels[3 * (y * width + x)]  == 0.0:
            x -= 1
        x += 1
        spanAbove, spanBelow = False, False
        while x < width and pixels[3 * (y * width + x)] == 0.0:
            for i in range(3):
                pixels[3 * (y * width + x) + i] = 1.0
            if not spanAbove and y > 0 and pixels[3 * ((y - 1) * width + x)]  == 0.0:
                stack.append((x, y - 1))
                spanAbove = True
            elif spanAbove and y > 0 and pixels[3 * ((y - 1) * width + x)] != 0.0:
                spanAbove = False
            if not spanBelow and y < height - 1 and pixels[3 * ((y + 1) * width + x)]  == 0.0:
                stack.append((x, y + 1))
                spanBelow = True
            elif spanBelow and y < height - 1 and pixels[3 * ((y + 1) * width + x)] != 0.0:
                spanBelow = False
            x += 1
    shapeIsDrawn = True

@window.event
def on_draw():
    window.clear()
    drawPixels()

@window.event
def on_key_press(symbol, modkey):
    global points, pointsUpdated
    if symbol == key.A:
        connectPoints(True)
    if symbol == key.S:
        connectPoints(False)
    if symbol == key.R:
        clearPixels()
        points = []
        pointsUpdated = False

@window.event
def on_mouse_press(x, y, button, modifiers):
    global casting, stack
    if button & mouse.LEFT:
        appendPoint(x, y)
        setBrightness(x, y, 1.0)
    if button & mouse.RIGHT:
        fill(x, y)

@window.event
def on_resize(width_new, height_new):
    global width, height, pixels
    width = width_new
    height = height_new
    pixels = numpy.empty(3 * height * width, dtype=float)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)

pyglet.app.run()
