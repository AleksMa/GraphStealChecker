import copy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return copy.copy(self)


class Edge:
    def __init__(self, point_1, point_2):
        if point_1.y < point_2.y:
            self.right = True
            self.begin = point_1.copy()
            self.end = point_2.copy()
        else:
            self.right = False
            self.begin = point_2.copy()
            self.end = point_1.copy()

    def copy(self):
        return copy.copy(self)


width = 0
height = 0


def InitGL(Width, Height):
    global width, height
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, Width, 0, Height, -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    width, height = Width, Height


edges = None
point_list = []

RESIZE_STEP = 20

def resize_image(height_mod, width_mod):
    for edge in edges:
        edge.begin.x *= width_mod
        edge.begin.x = round(edge.begin.x)
        edge.end.x *= width_mod
        edge.end.x = round(edge.end.x)
        edge.begin.y *= height_mod
        edge.begin.y = round(edge.begin.y)
        edge.end.y *= height_mod
        edge.end.y = round(edge.end.y)


def DrawGLScene():
    global width, height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if edges is None:
        draw_points()
    else:
        old_width = width
        old_height = height
        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)
        if width > old_width + RESIZE_STEP or width < old_width - RESIZE_STEP:
            while width > old_width + RESIZE_STEP or width < old_width - RESIZE_STEP:
                width = old_width + RESIZE_STEP if width > old_width else old_width - RESIZE_STEP
        else:
            width = old_width
        if height > old_height + RESIZE_STEP or height < old_height - RESIZE_STEP:
            while height > old_height + RESIZE_STEP or height < old_height - RESIZE_STEP:
                height = old_height + RESIZE_STEP if height > old_height else old_height - RESIZE_STEP
        else:
            height = old_height

        if height != old_height or width != old_width:
            height_mod = height/old_height
            width_mod = width/old_width
            resize_image(height_mod, width_mod)
        frame = np.zeros(width * height, dtype=int)
        raster(frame)
        bresenham(frame)
        glDrawPixels(width, height, GL_LUMINANCE, GL_UNSIGNED_BYTE, frame)

    glutSwapBuffers()


def draw_points():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    for point in point_list:
        glVertex3f(point.x, point.y, 0)
    glEnd()


def make_edges():
    global edges
    edges = [Edge(point_list[i], point_list[i + 1]) for i in np.arange(0, len(point_list) - 1)]
    edges.append(Edge(point_list[-1], point_list[0]))


def delta_x(edge):
    return (edge.end.x - edge.begin.x) / (edge.end.y - edge.begin.y)


def raster_line(x_1, x_2, y, frame):
    for x in np.arange(x_1+0.5, x_2+0.5, 1): frame[y*width + int(x)] = 255


def not_horizontal(edge):
    return edge.begin.y != edge.end.y


def raster(frame):
    global width, height, edges
    edges_ = edges.copy()
    edges_ = [edge for edge in edges_ if not_horizontal(edge)]
    edges_.sort(key=lambda edge: edge.begin.y)
    active_edges = {}
    for y in range(height, -1, -1):

        to_del = set()
        for k, v in active_edges.items():
            if k.begin.y > y:
                to_del.add(k)
        for k in to_del:
            del active_edges[k]

        to_del = set()
        for i in range(0, len(edges_)):
            if edges_[i].end.y > y:
                active_edges[edges_[i].copy()] = [delta_x(edges_[i]), edges_[i].end.x]
                to_del.add(i)
        edges_ = [j for i, j in enumerate(edges_) if i not in to_del]
        for _, v in active_edges.items():
            v[1] += -v[0]

        x_list = [v[1] for _, v in active_edges.items()]
        x_list.sort()
        for i in range(0, len(x_list), 2):
            raster_line(x_list[i], x_list[i + 1], y, frame)



Q = False
def set_pixel(frame,x_,y_,mod, err, sign_x, sign_y):
    if sign_x == sign_y:
        err = 255 - err
    if mod == 1:
        frame[x_ * width + y_] = err if not Q else 255 - err
    else:
        frame[y_*width +x_] = 255 - err if not Q else err


S = 100000
G = True
def bresenham(frame):
    i = 0
    for edge in edges:
        if (i > S):
            break
        dx = edge.end.x - edge.begin.x
        dy = edge.end.y - edge.begin.y
        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
        if dx < 0: dx = -dx
        if dy < 0: dy = -dy
        arg_step_x, arg_step_y, dy_, dx_, x_, y_, mod = 0, 0, 0, 0, 0, 0, 0
        if dx > dy:
            arg_step_x, arg_step_y = sign_x, 0
            dy_, dx_ = dy, dx
            if edge.right:
                x_ = edge.begin.x
                y_ = edge.begin.y
            else:
                x_ = edge.end.x
                y_ = edge.end.y
                sign_x, sign_y = - sign_x, - sign_y
                arg_step_x, arg_step_y = sign_x, 0
            mod = 0
        else:
            arg_step_x, arg_step_y = 0, sign_y
            dy_, dx_ = dx, dy
            if edge.right:
                x_ = edge.begin.y
                y_ = edge.begin.x
            else:
                x_ = edge.end.y
                y_ = edge.end.x
                sign_x, sign_y = - sign_x, - sign_y
                arg_step_x, arg_step_y = 0, sign_y
            mod = 1

        I = 255
        m = I*(dy_/dx_)
        err, t = I // 2, 0
        delta_err = m
        w = I - m
        set_pixel(frame, x_, y_, mod, err,sign_x, sign_y)
        while t < dx_:
            if err >= w:
                err -= w
                x_ += sign_x if mod == 0 else sign_y
                y_ += sign_y if mod == 0 else sign_x
            else:
                err += delta_err
                x_ += arg_step_x if mod == 0 else arg_step_y
                y_ += arg_step_y if mod == 0 else arg_step_x
            set_pixel(frame,x_,y_,mod,err, sign_x, sign_y)
            t += 1
            i += 1
            if (i > S):
                break


def mouse(button, state, x, y):
    global width, height, point_list
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            point_list.append(Point(x, height - y))
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            make_edges()


def specialkeys(key, x, y):
    global point_list, edges, S, Q, G
    if key == GLUT_KEY_UP:
        edges = None
        point_list = []
    if key == GLUT_KEY_F1:
        S  = 1 if S > 1 else 100000
    if key == GLUT_KEY_F2:
        Q = True ^ Q
    if key == GLUT_KEY_F3:
        G = True ^ G


def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)

    window = glutCreateWindow('OpenGL Python Cube')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutSpecialFunc(specialkeys)
    glutMouseFunc(mouse)
    InitGL(1000, 800)
    glutMainLoop()


if __name__ == "__main__":
    main()
