from OpenGL.GL import glRasterPos
from pyglet.window import key, mouse
from pyglet.gl import *
import pyglet


zoom = 12
Width = int(1200/zoom)
Height = int(1200/zoom)
window = pyglet.window.Window(1200, 1200, resizable=True)
window.set_minimum_size(100, 100)
glClearColor(1, 1, 1, 1)

fill = False
smooth = False
buffer = ""
points = []
help_buffer = []
base = []
vertex = []


def upgrade_line(x1, y1, x2, y2):
    global vertex
    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    ax = ay = 0
    if sign_x != 0:
        ax = 1
    if sign_y != 0:
        ay = 1

    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el / 2, 0

    vertex.append([x, y])
    set_pixel(x, y, 255)

    while t < el:
        error -= es
        if error < 0:
            error += el
            if ax == ay == 1:
                if sign_x == sign_y == 1:
                    vertex.append([x, y + 1])
                    if dx <= dy:
                        set_pixel(x, y + 1, int(255 * (error + es - el) * 1.0 / el))
                    else:
                        set_pixel(x, y + 1, 255 - int(255 * error * 1.0 / el))

                if sign_x == sign_y == -1:
                    vertex.append([x, y - 1])
                    if dx <= dy:
                        set_pixel(x, y - 1, int(255 * (error + es - el) * 1.0 / el))
                    else:
                        set_pixel(x, y - 1, 255 - int(255 * error * 1.0 / el))

                if sign_x == 1 and sign_y == -1:
                    vertex.append([x + 1, y])
                    if dx <= dy:
                        set_pixel(x + 1, y, 255 - int(255 * error * 1.0 / el))
                    else:
                        set_pixel(x + 1, y, int(255 * (error + es - el) * 1.0 / el))

                if sign_x == -1 and sign_y == 1:
                    vertex.append([x - 1, y])
                    if dx <= dy:
                        set_pixel(x - 1, y, 255 - int(255 * error * 1.0 / el))
                    else:
                        set_pixel(x - 1, y, int(255 * (error + es - el) * 1.0 / el))

            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        vertex.append([x, y])
        if ax == ay == 1:
            if sign_x == sign_y == 1 and dx <= dy:
                set_pixel(x, y, int(255 * error * 1.0 / el))
            elif sign_x == sign_y == 1 and dx > dy:
                set_pixel(x, y, 255 - int(255 * error * 1.0 / el))

            elif sign_x == 1 and sign_y == -1 and dx <= dy:
                set_pixel(x, y, 255 - int(255 * error * 1.0 / el))
            elif sign_x == 1 and sign_y == -1 and dx > dy:
                set_pixel(x, y, int(255 * error * 1.0 / el))

            elif sign_x == sign_y == -1 and dx <= dy:
                set_pixel(x, y, int(255 * error * 1.0 / el))
            elif sign_x == sign_y == -1 and dx > dy:
                set_pixel(x, y, 255 - int(255 * error * 1.0 / el))

            elif sign_x == -1 and sign_y == 1 and dx <= dy:
                set_pixel(x, y, 255 - int(255 * error * 1.0 / el))
            elif sign_x == -1 and sign_y == 1 and dx > dy:
                set_pixel(x, y, int(255 * error * 1.0 / el))
        else:
            set_pixel(x, y, 255 - int(255 * error * 1.0 / el))


def line(x1, y1, x2, y2):
    global vertex
    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    ax = ay = 0
    if sign_x != 0:
        ax = 1
    if sign_y != 0:
        ay = 1

    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el / 2, 0

    vertex.append([x, y])
    set_pixel(x, y, 255)
    while t < el:
        error -= es
        if error < 0:
            error += el
            if ax == ay == 1:
                if sign_x == sign_y == 1:
                    vertex.append([x, y + 1])
                    set_pixel(x, y + 1, 255)
                if sign_x == sign_y == -1:
                    vertex.append([x, y - 1])
                    set_pixel(x, y - 1, 255)
                if sign_x == 1 and sign_y == -1:
                    vertex.append([x + 1, y])
                    set_pixel(x + 1, y, 255)
                if sign_x == -1 and sign_y == 1:
                    vertex.append([x, y - 1])
                    set_pixel(x - 1, y, 255)

            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        vertex.append([x, y])
        set_pixel(x, y, 255)


def fillUp():
    global Width, Height, help_buffer, buffer, base
    x = base[0]
    y = base[1]

    space = [(255).to_bytes(1, 'big'), (255).to_bytes(1, 'big'), (255).to_bytes(1, 'big')]
    stack = [[x, y]]

    while stack:
        p = stack.pop()
        x = p[0]
        y = p[1]
        xt = x
        Fl = 0
        set_pixel(x, y, 255)

        x = x - 1
        while help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] == space:
            set_pixel(x, y, 255)
            x = x - 1
        xl = x + 1
        x = xt

        x = x + 1
        while help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] == space:
            set_pixel(x, y, 255)
            x = x + 1
        xr = x - 1

        y = y + 1
        x = xl
        while x <= xr:
            Fl = 0
            while help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] == space and x <= xr + 1:
                if Fl == 0:
                    Fl = 1
                x = x + 1

            if Fl == 1:
                if x == xr and help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] == space:
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
                Fl = 0

            xt = x
            while help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] != space and x < xr:
                x = x + 1

            if x == xt:
                x = x + 1

        y = y - 2
        x = xl
        while x <= xr:
            Fl = 0
            while help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] == space and x <= xr + 1:
                if Fl == 0:
                    Fl = 1
                x = x + 1

            if Fl == 1:
                if x == xr and help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] == space:
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
                Fl = 0

            xt = x
            while help_buffer[(x + y * Width) * 3:(x + y * Width) * 3 + 3] != space and x < xr:
                x = x + 1

            if x == xt:
                x = x + 1

    buffer = b"".join(help_buffer)


def set_pixel(x, y, e):
    global help_buffer, Width
    if e == 777:
        help_buffer[(x + y * Width) * 3] = (255).to_bytes(1, 'big')
        help_buffer[(x + y * Width) * 3 + 1] = (0).to_bytes(1, 'big')
        help_buffer[(x + y * Width) * 3 + 2] = (144).to_bytes(1, 'big')
    else:
        if e <= 0:
            e = 1
        f = int((255 - e))
        help_buffer[(x + y * Width) * 3] = f.to_bytes(1, 'big')
        help_buffer[(x + y * Width) * 3 + 1] = f.to_bytes(1, 'big')
        help_buffer[(x + y * Width) * 3 + 2] = f.to_bytes(1, 'big')


@window.event
def on_draw():
    window.clear()
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glEnable(GL_DITHER)
    glRasterPos(0, 0)
    glPixelZoom(zoom, zoom)
    if buffer != '':
        glDrawPixels(Width, Height, GL_RGB, GL_UNSIGNED_BYTE, buffer)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global points, base
    if button == mouse.LEFT:
        points.append([int(x / zoom), int(y / zoom)])
    if button == mouse.RIGHT:
        base = [int(x / zoom), int(y / zoom)]


@window.event
def on_key_press(symbol, modifiers):
    global points, Width, Height
    global fill, zoom, smooth, buffer, help_buffer
    if symbol == key.D:
        points = []
        buffer = ''
        help_buffer = []
    if symbol == key.F:
        fill = not fill
    if symbol == key.ENTER and points != []:
        buffer = ''
    if symbol == key.UP:
        zoom += 1
    if symbol == key.DOWN:
        zoom -= 1
    if symbol == key.S:
        smooth = not smooth
    if points:
        help_buffer = [b'\xff'] * Width * Height * 3
        length = len(points)
        if not smooth:
            for i in range(1, length):
                line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])
            line(points[length - 1][0], points[length - 1][1], points[0][0], points[0][1])
            buffer = b"".join(help_buffer)
        else:
            for i in range(1, length):
                upgrade_line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])
            upgrade_line(points[length - 1][0], points[length - 1][1], points[0][0], points[0][1])
            buffer = b"".join(help_buffer)
        if fill:
            fillUp()


@window.event
def on_resize(width, height):
    global buffer, help_buffer
    global Width, Height
    if Width != int(width / zoom) or Height != int(height / zoom):
        buffer = ''
        Width = int(width / zoom)
        Height = int(height / zoom)
        if points:
            help_buffer = [b'\xff'] * Width * Height * 3
            length = len(points)
            if not smooth:
                for i in range(1, length):
                    line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])
                line(points[0][0], points[0][1], points[length - 1][0], points[length - 1][1])
            else:
                for i in range(1, length):
                    upgrade_line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])
                upgrade_line(points[0][0], points[0][1], points[length - 1][0], points[length - 1][1])
            if fill:
                fillUp()


pyglet.app.run()
