from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

window = 0

# rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0

DIRECTION = 1


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


a_mod = 1.0
b_mod = 1.4
top_x = 0.0
top_y = 1.0
top_z = 1.5

cone_centre = [0.0, 0.0, 0.0]  # customizable
cone_top = [top_x, top_y, top_z]  # customizable
axis_vector = [cone_top[i] - cone_centre[i] for i in range(3)]
vert_slices = 10
slice_len = None
step = 10
bottom_slices = 10
bottom_slice_len = None
all_circle_dots, all_bottom_dots = None, None


def count_dots():
    global slice_len, bottom_slice_len
    global all_circle_dots, all_bottom_dots
    slice_len = 1 / vert_slices
    bottom_slice_len = 1 / bottom_slices
    all_circle_dots, all_bottom_dots = [[
        [(slice_len * a_mod * math.cos(math.radians(angle)) * (vert_slices - slice_part) + slice_len *
          axis_vector[0] * slice_part,
          slice_len * axis_vector[1] * slice_part,
          slice_len * b_mod * math.sin(math.radians(angle)) * (vert_slices - slice_part) + slice_len *
          axis_vector[2] * slice_part)
         for angle in range(0, 360, step)]
        for slice_part in range(vert_slices - 1, -1, -1)],
        [
            [(bottom_slice_len * a_mod * math.cos(math.radians(angle)) * (bottom_slices - slice_part) + cone_centre[0],
              cone_centre[1],
              bottom_slice_len * b_mod * math.sin(math.radians(angle)) * (bottom_slices - slice_part) + cone_centre[2])
             for angle in range(0, 360, step)]
            for slice_part in range(bottom_slices - 1, -1, -1)]]


count_dots()


def draw_elliptic_cone():
    global a_mod
    global b_mod
    global top_x, top_y, top_z
    global all_circle_dots, all_bottom_dots
    glBegin(GL_TRIANGLE_FAN)

    glColor3f(0, 1, 0)
    glVertex3f(*cone_top)
    glColor3f(0, 0, 1)
    for dot in all_circle_dots[0]:
        glVertex3f(*dot)
    glVertex3f(*all_circle_dots[0][0])
    glEnd()
    glBegin(GL_QUADS)
    for slice_num in range(0, vert_slices - 1):
        for i in range(0, 360 // step - 1):
            glVertex3f(*all_circle_dots[slice_num][i])
            glVertex3f(*all_circle_dots[slice_num][i + 1])
            glVertex3f(*all_circle_dots[slice_num + 1][i + 1])
            glVertex3f(*all_circle_dots[slice_num + 1][i])
        glVertex3f(*all_circle_dots[slice_num][0])
        glVertex3f(*all_circle_dots[slice_num][360 // step - 1])
        glVertex3f(*all_circle_dots[slice_num + 1][360 // step - 1])
        glVertex3f(*all_circle_dots[slice_num + 1][0])
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(*cone_centre)
    for dot in all_bottom_dots[0]:
        glVertex3f(*dot)
    glVertex3f(*all_bottom_dots[0][0])
    glEnd()
    glBegin(GL_QUADS)
    for slice_num in range(0, bottom_slices - 1):
        for i in range(0, 360 // step - 1):
            glVertex3f(*all_bottom_dots[slice_num][i])
            glVertex3f(*all_bottom_dots[slice_num][i + 1])
            glVertex3f(*all_bottom_dots[slice_num + 1][i + 1])
            glVertex3f(*all_bottom_dots[slice_num + 1][i])
        glVertex3f(*all_bottom_dots[slice_num][0])
        glVertex3f(*all_bottom_dots[slice_num][360 // step - 1])
        glVertex3f(*all_bottom_dots[slice_num + 1][360 // step - 1])
        glVertex3f(*all_bottom_dots[slice_num + 1][0])
    glEnd()


zoom = 1


def DrawGLScene():
    global X_AXIS, Y_AXIS, Z_AXIS
    global xpos, ypos, zpos
    global DIRECTION
    global zoom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glViewport(0, 0, 400, 400)
    # glTranslatef(0.0, 0.0, -6.0)

    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    #glScalef(zoom, zoom, zoom)
    draw_elliptic_cone()

    glLoadIdentity()
    glViewport(0, 400, 400, 400)
    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    draw_elliptic_cone()

    glLoadIdentity()
    glViewport(500, 400, 400, 400)
    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    glRotatef(-90, 0.0, 1.0, 0.0)
    draw_elliptic_cone()

    glutSwapBuffers()


def specialkeys(key, x, y):
    global X_AXIS, a_mod
    global Y_AXIS, b_mod
    global top_x, top_y, top_z, zoom
    global all_circle_dots, all_bottom_dots
    global  bottom_slices, vert_slices
    if key == GLUT_KEY_UP:
        X_AXIS -= 1
    if key == GLUT_KEY_DOWN:
        X_AXIS += 1
    if key == GLUT_KEY_LEFT:
        Y_AXIS -= 1
    if key == GLUT_KEY_RIGHT:
        Y_AXIS += 1
    if key == GLUT_KEY_F1:
        a_mod -= 0.05
        count_dots()
    if key == GLUT_KEY_F2:
        a_mod += 0.05
        count_dots()
    if key == GLUT_KEY_F3:
        b_mod -= 0.05
        count_dots()
    if key == GLUT_KEY_F4:
        b_mod += 0.05
        count_dots()
    if key == GLUT_KEY_F5:
        top_x -= 0.05
        count_dots()
    if key == GLUT_KEY_F6:
        top_x += 0.05
        count_dots()
    if key == GLUT_KEY_F7:
        top_y -= 0.05
        count_dots()
    if key == GLUT_KEY_F8:
        top_y += 0.05
        count_dots()
    if key == GLUT_KEY_F9:
        vert_slices += 1
        count_dots()
    if key == GLUT_KEY_F10 and vert_slices > 1:
        vert_slices -= 1
        count_dots()
    if key == GLUT_KEY_F11:
        bottom_slices += 1
        count_dots()
    if key == GLUT_KEY_F12 and bottom_slices > 1:
        bottom_slices -= 1
        count_dots()
    if key == GLUT_KEY_PAGE_UP:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    if key == GLUT_KEY_PAGE_DOWN:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glutPostRedisplay()


def mouse(button, state, x, y):
    global X_AXIS
    global Y_AXIS
    if button == GLUT_LEFT_BUTTON:
        X_AXIS = 0
        Y_AXIS = 0


def keyboard(key, x, y):
    global vert_slices, bottom_slices
    #print(key)
    if key == b"w":
        vert_slices += 1
        count_dots()
    elif key == b"s" and vert_slices > 1:
        vert_slices -= 1
        count_dots()
    elif key == b"d":
        bottom_slices += 1
        count_dots()
    elif key == b"a" and bottom_slices > 1:
        bottom_slices -= 1
        count_dots()


def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow('OpenGL Python Cube')
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutSpecialFunc(specialkeys)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()
