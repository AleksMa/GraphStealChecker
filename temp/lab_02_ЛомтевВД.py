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
    glOrtho(-2,2,-2,2,-1000,1000)
    glMatrixMode(GL_MODELVIEW)


def draw_cube():
    glBegin(GL_QUADS)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()




zoom = 1
zpos = 0
ypos = 0
xpos = 0
def DrawGLScene():
    global X_AXIS, Y_AXIS, Z_AXIS
    global xpos, ypos, zpos
    global DIRECTION
    global zoom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    glViewport(0,0,240,240)
    #glTranslatef(0.0, 0.0, -6.0)

    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    glScalef(zoom,zoom,zoom)
    draw_cube()

####
    glLoadIdentity()
    glViewport(320,0,240,240)
    glRotatef(X_AXIS+45, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS-45, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    glMultMatrixd([1, 0, 0, 0,
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   xpos, ypos, zpos, 1])
    draw_cube()
####

    glLoadIdentity()
    glViewport(0, 240, 240, 240)
    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    draw_cube()

    glLoadIdentity()
    glViewport(320, 240, 240, 240)
    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
    glRotatef(-90, 0.0, 1.0, 0.0)
    draw_cube()

    glutSwapBuffers()


def specialkeys(key, x, y):
    global X_AXIS
    global Y_AXIS
    global zoom
    global zpos, xpos, ypos
    if key == GLUT_KEY_UP:
        X_AXIS -= 1
    if key == GLUT_KEY_DOWN:
        X_AXIS += 1
    if key == GLUT_KEY_LEFT:
        Y_AXIS -= 1
    if key == GLUT_KEY_RIGHT:
        Y_AXIS += 1
    if key == GLUT_KEY_F1:
        xpos += 1
    if key == GLUT_KEY_F2:
        xpos -= 1
    if key == GLUT_KEY_F3:
        ypos += 1
    if key == GLUT_KEY_F4:
        ypos -= 1
    if key == GLUT_KEY_F5:
        zpos += 1
    if key == GLUT_KEY_F6:
        zpos -= 1
    if key == GLUT_KEY_F11:
        zoom -= 0.05
    if key == GLUT_KEY_F12:
        zoom += 0.05
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
    if button == GLUT_RIGHT_BUTTON:
        X_AXIS = 0
        Y_AXIS = -90

def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow('OpenGL Python Cube')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutSpecialFunc(specialkeys)
    glutMouseFunc(mouse)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()
