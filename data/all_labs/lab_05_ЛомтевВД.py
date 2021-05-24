import copy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from goto import with_goto
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return copy.copy(self)


class Inter_point:
    def __init__(self, point, cl):
        self.x = point.x
        self.y = point.y
        self.cl = cl
        self.processed = False

    def copy(self):
        return copy.copy(self)


class Edge:
    def __init__(self, point_1, point_2):
        self.begin = point_1.copy()
        self.end = point_2.copy()
        self.intersecs = []

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


Q = False
edges_1 = None
point_list_1 = []
edges_2 = None
point_list_2 = []


def DrawGLScene():
    global width, height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if edges_1 is None or edges_2 is None:
        draw_points()
    else:
        glColor(1,1,1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        clip(edges_1, edges_2)

    glutSwapBuffers()


ENTRY = True
EXIT = False
first_time = True
mod = 1
has_intersec = False


@with_goto
def clip(edges_1, edges_2):
    global first_time, ENTRY, EXIT, has_intersec, mod
    if first_time:
        has_intersec = classify_intersec(edges_1, edges_2)
        first_time = False
    completed_list_1 = complete_list(edges_1)
    completed_list_2 = complete_list(edges_2)

    if mod == 2:
        ENTRY = False  # Для пересечения
        EXIT = True  # Для пересечения
    else:
        ENTRY = True  # Для остального
        EXIT = False  # Для остального
    if has_intersec:
        len_1 = len(completed_list_1)
        len_2 = len(completed_list_2)
        intersec_figs_list = []
        i = 0
        j = 0
        while not all_processed(completed_list_1):
            while not hasattr(completed_list_1[i], "cl") or (
                    completed_list_1[i].cl != ENTRY or completed_list_1[i].processed):
                i += 1
                i %= len_1
            completed_list_1[i].processed = True
            fig_list = []
            entry_point = completed_list_1[i]

            label .begin
            while not hasattr(completed_list_1[i], "cl") or not completed_list_1[i].cl == EXIT:
                fig_list.append(completed_list_1[i])
                i += 1
                i %= len_1

            j = find_in_list(completed_list_1[i], completed_list_2)
            while not hasattr(completed_list_2[j], "cl") or not completed_list_2[j].cl == ENTRY:
                fig_list.append(completed_list_2[j])
                if mod == 3:
                    j += 1
                else:
                    j -= 1  #  минус для пересечения и объединения, плюс для разности
                j %= len_2
            if same_point(completed_list_2[j], entry_point):
                i += 1
                i %= len_1
                intersec_figs_list.append(fig_list)
            else:
                i = find_in_list(completed_list_2[j], completed_list_1)
                completed_list_1[i].processed = True
                goto .begin
        for fig in intersec_figs_list:
            glBegin(GL_LINE_STRIP)
            for point in fig:
                glVertex3f(point.x, point.y, 0)
            glVertex3f(fig[0].x, fig[0].y, 0)
            glEnd()
    else:
        point = edges_1[0].begin
        g = 0
        inside_1 = False
        inside_2 = False
        for edge in edges_2:
            if traverse(point, edge):
                g += 1
        if g % 2 == 1:
            inside_1 = True
            g = 0
        if not inside_1:
            point = edges_2[0].begin
            for edge in edges_1:
                if traverse(point, edge):
                    g += 1
            if g % 2 == 1:
                inside_2 = True
        if mod == 1:
            if inside_1:
                draw_figs(completed_list_2)
            elif inside_2:
                 draw_figs(completed_list_1)
            else:
                draw_figs(completed_list_1, completed_list_2)
        elif mod == 2:
            if inside_1:
                draw_figs(completed_list_1)
            elif inside_2:
                draw_figs(completed_list_2)
        elif mod == 3:
            if inside_2:
                draw_figs(completed_list_1, completed_list_2)
            elif not inside_1:
                draw_figs(completed_list_1)


def traverse(point, edge):
    edge_ = Edge(point, Point(point.x, point.y + width))
    return classify_intersec([edge_], [edge])


def draw_figs(*figs):
    for fig in figs:
        glBegin(GL_LINE_STRIP)
        for point in fig:
            glVertex3f(point.x, point.y, 0)
        glVertex3f(fig[0].x, fig[0].y, 0)
        glEnd()


def same_point(point_1, point_2):
    return point_1.x == point_2.x and point_1.y == point_2.y


def all_processed(lst):
    for point in lst:
        if hasattr(point, "processed") and not point.processed and point.cl == ENTRY:
            return False
    return True


def find_in_list(point, point_list):
    for i in range(len(point_list)):
        if same_point(point, point_list[i]):
            return i
    return None


def classify_intersec(edges_1, edges_2):
    intersec_ = False
    for i in range(0, len(edges_2)):
        for j in range(0, len(edges_1)):
            intersec_point = intersec(edges_2[i], edges_1[j])
            if intersec_point is not None:
                if not intersec_:
                    intersec_ = True
                if cross_product(edges_1[j], edges_2[i].end) < 0:
                    # RIGHT
                    edges_2[i].intersecs.append(Inter_point(intersec_point, copy.copy(ENTRY)))
                    edges_1[j].intersecs.append(Inter_point(intersec_point, copy.copy(ENTRY)))
                else:
                    # LEFT
                    edges_2[i].intersecs.append(Inter_point(intersec_point, copy.copy(EXIT)))
                    edges_1[j].intersecs.append(Inter_point(intersec_point, copy.copy(EXIT)))
    return intersec_


def intersec(line_1, line_2):
    i1_x = [min(line_1.begin.x, line_1.end.x), max(line_1.begin.x, line_1.end.x)]
    i2_x = [min(line_2.begin.x, line_2.end.x), max(line_2.begin.x, line_2.end.x)]
    i_x = [max(i1_x[0], i2_x[0]), min(i1_x[1], i2_x[1])]
    i1_y = [min(line_1.begin.y, line_1.end.y), max(line_1.begin.y, line_1.end.y)]
    i2_y = [min(line_2.begin.y, line_2.end.y), max(line_2.begin.y, line_2.end.y)]
    i_y = [max(i1_y[0], i2_y[0]), min(i1_y[1], i2_y[1])]
    a1 = line_1.end.y - line_1.begin.y
    b1 = line_1.begin.x - line_1.end.x
    c1 = a1 * line_1.begin.x + b1 * line_1.begin.y

    a2 = line_2.end.y - line_2.begin.y
    b2 = line_2.begin.x - line_2.end.x
    c2 = a2 * line_2.begin.x + b2 * line_2.begin.y

    det = a1 * b2 - a2 * b1
    if det == 0: return None
    x = ((b2 * c1) - (b1 * c2)) // det
    y = ((a1 * c2) - (a2 * c1)) // det
    if i_x[0] <= x <= i_x[1] and i_y[0] <= y <= i_y[1]:
        return Point(x, y)
    else:
        return None


def cross_product(vector, point):
    a = [vector.begin.x - point.x, vector.begin.y - point.y]
    b = [vector.end.x - point.x, vector.end.y - point.y]
    return a[0] * b[1] - a[1] * b[0]


def complete_list(edges):
    points = []
    len_edges = len(edges)
    for i in range(len_edges):
        points.append(edges[i].begin.copy())
        if edges[i].end.x - edges[i].begin.x > 0:
            edges[i].intersecs.sort(key=lambda x_: x_.x)
        elif edges[i].end.x - edges[i].begin.x < 0:
            edges[i].intersecs.sort(key=lambda x_: -x_.x)
        elif edges[i].end.y - edges[i].begin.y > 0:
            edges[i].intersecs.sort(key=lambda x_: x_.y)
        else:
            edges[i].intersecs.sort(key=lambda x_: -x_.y)
        for point in edges[i].intersecs:
            points.append(point.copy())
    return points


def draw_points():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glColor3f(255, 0, 0)
    for point in point_list_1:
        glVertex3f(point.x, point.y, 0)
    glEnd()
    glBegin(GL_POLYGON)
    glColor3f(0, 0, 255)
    for point in point_list_2:
        glVertex3f(point.x, point.y, 0)
    glEnd()


def make_edges():
    global edges_1, edges_2
    if not Q:
        edges_1 = [Edge(point_list_1[i], point_list_1[i + 1]) for i in np.arange(0, len(point_list_1) - 1)]
        edges_1.append(Edge(point_list_1[-1], point_list_1[0]))
    else:
        edges_2 = [Edge(point_list_2[i], point_list_2[i + 1]) for i in np.arange(0, len(point_list_2) - 1)]
        edges_2.append(Edge(point_list_2[-1], point_list_2[0]))


def mouse(button, state, x, y):
    global width, height, point_list_1, point_list_2, Q
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if not Q:
                point_list_1.append(Point(x, height - y))
            else:
                point_list_2.append(Point(x, height - y))
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            make_edges()
            Q = True


def specialkeys(key, x, y):
    global point_list_1, point_list_2, edges_1, edges_2, mod, first_time, Q
    if key == GLUT_KEY_F1:
        mod = 1
    if key == GLUT_KEY_F2:
        mod = 2
    if key == GLUT_KEY_F3:
        mod = 3
    if key == GLUT_KEY_UP:
        Q = False
        point_list_1 = []
        point_list_2 = []
        edges_1 = None
        edges_2 = None
        first_time = True



def main():
    global window, mod
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
