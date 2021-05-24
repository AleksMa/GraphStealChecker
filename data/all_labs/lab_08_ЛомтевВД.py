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
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)


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
all_circle_dots, all_bottom_dots, quads, quads_bottom, fan, fan_bottom = None, None, None, None, None, None
quads_color, quads_bottom_color, fan_color, fan_bottom_color = None, None, None, None


def find_c(lst):
    return [abs(x)/(lst[0]**2+lst[1]**2+lst[2]**2 + 0.001) for x in range(3)]

def count_dots():
    global slice_len, bottom_slice_len
    global all_circle_dots, all_bottom_dots, quads, quads_bottom, fan, fan_bottom
    global quads_color, quads_bottom_color, fan_color, fan_bottom_color, list_was_created
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
    fan = [cone_top]
    fan_color = [find_c(cone_top)]
    for dot in all_circle_dots[0]:
        fan.append(dot)
        fan_color.append(find_c(dot))
    fan.append(all_circle_dots[0][0])
    fan_color.append(find_c(all_circle_dots[0][0]))
    quads = []
    quads_color = []
    for slice_num in range(0, vert_slices - 1):
        for i in range(0, 360 // step - 1):
            quads.append(all_circle_dots[slice_num][i])
            quads.append(all_circle_dots[slice_num][i + 1])
            quads.append(all_circle_dots[slice_num + 1][i + 1])
            quads.append(all_circle_dots[slice_num + 1][i])
            quads_color.append(find_c(all_circle_dots[slice_num][i]))
            quads_color.append(find_c(all_circle_dots[slice_num][i + 1]))
            quads_color.append(find_c(all_circle_dots[slice_num + 1][i + 1]))
            quads_color.append(find_c(all_circle_dots[slice_num + 1][i]))
        quads.append(all_circle_dots[slice_num][0])
        quads.append(all_circle_dots[slice_num][360 // step - 1])
        quads.append(all_circle_dots[slice_num + 1][360 // step - 1])
        quads.append(all_circle_dots[slice_num + 1][0])
        quads_color.append(find_c(all_circle_dots[slice_num][0]))
        quads_color.append(find_c(all_circle_dots[slice_num][360 // step - 1]))
        quads_color.append(find_c(all_circle_dots[slice_num + 1][360 // step - 1]))
        quads_color.append(find_c(all_circle_dots[slice_num + 1][0]))
    fan_bottom = [cone_centre]
    fan_bottom_color = [find_c(cone_centre)]
    for dot in all_bottom_dots[0]:
        fan_bottom.append(dot)
        fan_bottom_color.append(find_c(dot))
    # one more fan_bottom comand?
    quads_bottom = []
    quads_bottom_color = []
    for slice_num in range(0, bottom_slices - 1):
        for i in range(0, 360 // step - 1):
            quads_bottom.append(all_bottom_dots[slice_num][i])
            quads_bottom.append(all_bottom_dots[slice_num][i + 1])
            quads_bottom.append(all_bottom_dots[slice_num + 1][i + 1])
            quads_bottom.append(all_bottom_dots[slice_num + 1][i])
            quads_bottom_color.append(find_c(all_bottom_dots[slice_num][i]))
            quads_bottom_color.append(find_c(all_bottom_dots[slice_num][i + 1]))
            quads_bottom_color.append(find_c(all_bottom_dots[slice_num + 1][i + 1]))
            quads_bottom_color.append(find_c(all_bottom_dots[slice_num + 1][i]))
        quads_bottom.append(all_bottom_dots[slice_num][0])
        quads_bottom.append(all_bottom_dots[slice_num][360 // step - 1])
        quads_bottom.append(all_bottom_dots[slice_num + 1][360 // step - 1])
        quads_bottom.append(all_bottom_dots[slice_num + 1][0])
        quads_bottom_color.append(find_c(all_bottom_dots[slice_num][0]))
        quads_bottom_color.append(find_c(all_bottom_dots[slice_num][360 // step - 1]))
        quads_bottom_color.append(find_c(all_bottom_dots[slice_num + 1][360 // step - 1]))
        quads_bottom_color.append(find_c(all_bottom_dots[slice_num + 1][0]))
    list_was_created = False



count_dots()

list_was_created, dp_lst = False, None
def draw_elliptic_cone():
    global a_mod
    global b_mod
    global top_x, top_y, top_z
    global all_circle_dots, all_bottom_dots, quads, quads_bottom, fan, fan_bottom, list_was_created, dp_lst
    global quads_color, quads_bottom_color, fan_color, fan_bottom_color
    if (not list_was_created):
        dp_lst = glGenLists(1)
        glNewList(dp_lst, GL_COMPILE)
        glVertexPointer(3, GL_FLOAT, 0, fan)
        glColorPointer(3, GL_FLOAT, 0, fan_color)
        glDrawArrays(GL_TRIANGLE_FAN, 0, len(fan))
        glVertexPointer(3, GL_FLOAT, 0, quads)
        glColorPointer(3, GL_FLOAT, 0, quads_color)
        glDrawArrays(GL_QUADS, 0, len(quads))
        glVertexPointer(3, GL_FLOAT, 0, fan_bottom)
        glColorPointer(3, GL_FLOAT, 0, fan_bottom_color)
        glDrawArrays(GL_TRIANGLE_FAN, 0, len(fan_bottom))
        glVertexPointer(3, GL_FLOAT, 0, quads_bottom)
        glColorPointer(3, GL_FLOAT, 0, quads_bottom_color)
        glDrawArrays(GL_QUADS, 0, len(quads_bottom))
        glEndList()
        list_was_created = True
    glCallList(dp_lst)

zoom = 1

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


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
    print(key)
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

    vert_sh = create_shader(GL_VERTEX_SHADER, """
        varying vec4 vertex_color;
        void main(){
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            vertex_color = gl_Color;
        }
    """)

    frag_sh = create_shader(GL_FRAGMENT_SHADER, """
        varying vec4 vertex_color;
        void main() {
            gl_FragColor = vertex_color;
        }
    """)
    program = glCreateProgram()
    glAttachShader(program, vert_sh)
    glAttachShader(program, frag_sh)
    glLinkProgram(program)
    glUseProgram(program)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()
