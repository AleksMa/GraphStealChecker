from pyglet import *
from pyglet.gl import *

pixels = [0 for i in range(100 * 100)]
superSampledPixels = [0 for i in range(300 * 300)]
drawn = [0 for i in range(100)]
superDrawn = [0 for i in range(300)]


def draw_pixel(x, y):
    global pixels, drawn
    if drawn[y] >= 2:
        return
    if pixels[x+y*100] == 255:
        drawn[y] += 1
        pixels[x + y * 100 + 1] = 255
    else:
        drawn[y] += 1
        pixels[x + y * 100] = 255


def draw_line(x1, y1, x2, y2):
    dx = x2-x1
    dy = y2-y1

    dx = max(dx, -dx)
    dy = max(dy, -dy)

    incx = 1 if x2 >= x1 else -1
    incy = 1 if y2 >= y1 else -1

    x, y = x1, y1

    if dx >= dy:
        e = 2 * dy-dx
        de = 2 * dy
        draw_pixel(x, y)
        for i in range(dx):
            if e >= 0:
                y += incy
                draw_pixel(x, y)
                e += 2 * (dy - dx)
            else:
                e += de
            x += incx
    else:
        e = 2 * dx-dy
        de = 2 * dx
        for i in range(dy):
            if e >= 0:
                x += incx
                e += 2 * (dx - dy)
            else:
                e += de
            draw_pixel(x, y)
            y += incy


def draw_superpixel(x, y):
    global superSampledPixels, superDrawn
    if superDrawn[y] >= 2:
        return
    if superSampledPixels[x+y*300] == 255:
        superDrawn[y] += 1
        superSampledPixels[x + y*300 + 1] = 255
    else:
        superDrawn[y] += 1
        superSampledPixels[x + y*300] = 255


def draw_superline(x1, y1, x2, y2):
    dx = x2-x1
    dy = y2-y1

    dx = max(dx, -dx)
    dy = max(dy, -dy)

    incx = 1 if x2 >= x1 else -1
    incy = 1 if y2 >= y1 else -1

    x, y = x1, y1

    if dx >= dy:
        e = 2 * dy-dx
        de = 2 * dy
        draw_superpixel(x, y)
        for i in range(dx):
            if e >= 0:
                y += incy
                draw_superpixel(x, y)
                e += 2 * (dy - dx)
            else:
                e += de
            x += incx
    else:
        e = 2 * dx-dy
        de = 2 * dx
        for i in range(dy):
            if e >= 0:
                x += incx
                e += 2 * (dx - dy)
            else:
                e += de
            draw_superpixel(x, y)
            y += incy


def stage_1():
    global vertices
    glBegin(GL_LINE_LOOP)
    for i in vertices:
        glVertex2i(i[0]*5, i[1]*5)
    glEnd()


def stage_2():
    global vertices, pixels, drawn
    pixels = [0 for i in range(100*100)]
    for i in range(len(vertices)):
        draw_line(*vertices[i], *vertices[(i+1) % len(vertices)])
    for i in range(len(pixels)-1):
        if drawn[i // 100] == 1:
            continue
        if i % 100 == 0:
            pixels[i] = 0
        pixels[i+1] = pixels[i+1] ^ pixels[i]
    glDrawPixels(100, 100, GL_LUMINANCE, GL_UNSIGNED_BYTE, (GLubyte * len(pixels))(*pixels))


def stage_3():
    global vertices, pixels, drawn, superSampledPixels, superDrawn
    pixels = [0 for i in range(100*100)]
    superSampledPixels = [0 for i in range(300 * 300)]
    superDrawn = [0 for i in range(300)]
    for i in range(len(vertices)):
        draw_superline(vertices[i][0]*3, vertices[i][1]*3, vertices[(i+1) % len(vertices)][0]*3, vertices[(i+1) % len(vertices)][1]*3)
    for i in range(len(superSampledPixels)-1):
        if superDrawn[i // 300] == 1:
            continue
        if i % 300 == 0:
            superSampledPixels[i] = 0
        superSampledPixels[i+1] = superSampledPixels[i+1] ^ superSampledPixels[i]
    for i in range(len(pixels)):
        x = i % 100
        y = i // 100
        s = 0
        s += superSampledPixels[(3*x + 900*y)]
        s += superSampledPixels[(3*x + 900*y)+1]
        s += superSampledPixels[(3*x + 900*y)+2]
        s += superSampledPixels[(3*x + 900*y)]
        s += superSampledPixels[(3*x + 900*y)+1+300]
        s += superSampledPixels[(3*x + 900*y)+2+300]
        s += superSampledPixels[(3*x + 900*y)+600]
        s += superSampledPixels[(3*x + 900*y)+1+600]
        s += superSampledPixels[(3*x + 900*y)+2+600]
        pixels[i] = s // 9
    glDrawPixels(100, 100, GL_LUMINANCE, GL_UNSIGNED_BYTE, (GLubyte * len(pixels))(*pixels))


config = Config(double_buffer=True)
tela = pyglet.window.Window(height=500, width=500, config=config, resizable=True)


@tela.event
def on_draw():
    global stage, drawn
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    stage = min(stage, 3)
    stage = max(stage, 1)
    glPixelZoom(5, 5)
    drawn = [0 for i in range(500)]
    if stage == 1:
        stage_1()
    if stage == 2:
        stage_2()
    if stage == 3:
        stage_3()


@tela.event
def on_mouse_press(x, y, button, modifiers):
    global vertices, stage, miny, maxy
    if button == window.mouse.LEFT and stage == 1:
        vertices.append((round(x // 5), round(y // 5)))
    if button == window.mouse.RIGHT:
        vertices.clear()
        stage = 1


@tela.event
def on_key_press(s, m):
    global vertices, stage
    if s == pyglet.window.key.LEFT:
        stage -= 1
    if s == pyglet.window.key.RIGHT:
        stage += 1


stage = 1
vertices = []
app.run()
