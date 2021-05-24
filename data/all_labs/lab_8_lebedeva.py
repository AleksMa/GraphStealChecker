# Проверено на Windows

import ctypes
from math import pi, sin, cos, asin, sqrt
import numpy
from pyglet.gl import *
import pyglet
from pyglet.window import key
import OpenGL.GL.shaders as glShaders

config = Config(sample_buffers=1, samples=4,
                depth_size=16, double_buffer=True, )
window = pyglet.window.Window(resizable=True, config=config)
glClearColor(0.3, 0.3, 0.3, 1)
glEnable(GL_DEPTH_TEST)


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


def vec(*args):
    return (GLfloat * len(args))(*args)


ambient = vec(1, 1, 1, 1)
diffuse = vec(1, 1, 1, 1)
specular = vec(1, 1, 1, 1)


# Управлпние
@window.event
def on_key_press(symbol, modifiers):
    alfa = 0.1
    global rx, ry, rz, ambient, diffuse, specular
    if symbol == key.Q:  # нажатие на Q, W, A, S, Z, X вращение вокруг осей
        torus.rx += alfa
        obj.updateRotateValue(torus.rx, True, False, False)
    elif symbol == key.W:
        torus.rx -= alfa
        obj.updateRotateValue(torus.rx, True, False, False)
    elif symbol == key.A:
        torus.ry += alfa
        obj.updateRotateValue(torus.ry, False, True, False)
    elif symbol == key.S:
        torus.ry -= alfa
        obj.updateRotateValue(torus.ry, False, True, False)
    elif symbol == key.Z:
        torus.rz += alfa
        obj.updateRotateValue(torus.rz, False, False, True)
    elif symbol == key.X:
        torus.rz -= alfa
        obj.updateRotateValue(torus.rz, False, False, True)
    elif symbol == key.SPACE:  # Пробел - представление фигуры в виде сетки или закрашенного
        torus.fill = not torus.fill  # Цифры от 1 до 9 - изменение характеристик света
    elif symbol == key._1:
        r = (ambient[0] + 1) % 2
        g = ambient[1]
        b = ambient[2]
        ambient = vec(r, g, b, 1)
    elif symbol == key._2:
        g = (ambient[1] + 1) % 2
        r = ambient[0]
        b = ambient[2]
        ambient = vec(r, g, b, 1)
    elif symbol == key._3:
        b = (ambient[2] + 1) % 2
        g = ambient[1]
        r = ambient[0]
        ambient = vec(r, g, b, 1)
    elif symbol == key._4:
        r = (diffuse[0] + 1) % 2
        g = diffuse[1]
        b = diffuse[2]
        diffuse = vec(r, g, b, 1)
    elif symbol == key._5:
        g = (diffuse[1] + 1) % 2
        r = diffuse[0]
        b = diffuse[2]
        diffuse = vec(r, g, b, 1)
    elif symbol == key._6:
        b = (diffuse[2] + 1) % 2
        g = diffuse[1]
        r = diffuse[0]
        diffuse = vec(r, g, b, 1)
    elif symbol == key._7:
        r = (specular[0] + 1) % 2
        g = specular[1]
        b = specular[2]
        specular = vec(r, g, b, 1)
    elif symbol == key._8:
        g = (specular[1] + 1) % 2
        r = specular[0]
        b = specular[2]
        specular = vec(r, g, b, 1)
    elif symbol == key._9:
        b = (specular[2] + 1) % 2
        g = specular[1]
        r = specular[0]
        specular = vec(r, g, b, 1)
    elif symbol == key.ENTER:  # Вкл и выкл анимации (движение внутри куба)
        torus.stop = not torus.stop
    elif symbol == key.K:  # Вкл и выкл постоянного вращения
        torus.spin = not torus.spin
    elif symbol == key.T:  # Вкл и выкл текстуры
        torus.show_tex = not torus.show_tex
    elif symbol == key.L:  # Вкл и выкл освещения
        torus.show_light = not torus.show_light
    elif symbol == key.C:  # сохранить текущее положение
        save()
    elif symbol == key.O:  # Начать отрисовку с сохраненного состояния
        try:
            open_save()
        except:
            print("Состояние не было полностью восстановлно")

    if (symbol == key._1 or symbol == key._2 or symbol == key._3 or symbol == key._4 or symbol == key._5
            or symbol == key._6 or symbol == key._7 or symbol == key._8 or symbol == key._9):
        print('abmbient ', *ambient)
        print('diffuse ', *diffuse)
        print('specular ', *specular)
        print()
        setup_light()  # Если были нажаты цифры, то изменить настройки света


def update(dt):
    if not torus.stop:
        torus.intersection_with_box(box)
        for i in range(3): torus.cur_pos[i] += torus.speed_vec[i]
        obj.updateTranslate(torus.cur_pos[0], torus.cur_pos[1], torus.cur_pos[2])
    if torus.spin:
        dt = dt
        torus.rx += dt * 1
        torus.ry += dt * 80
        torus.rz += dt * 30
        torus.rx %= 360
        torus.ry %= 360
        torus.rz %= 360
        torus.rx /= 57
        torus.ry /= 57
        torus.rz /= 57
        obj.updateRotateValue(torus.rx, True, False, False)
        obj.updateRotateValue(torus.ry, False, True, False)
        obj.updateRotateValue(torus.rz, False, False, True)


pyglet.clock.schedule(update)


@window.event
def on_draw():
    window.clear()
    # if torus.show_tex: glEnable(GL_TEXTURE_2D)
    # else: glDisable(GL_TEXTURE_2D)
    # if torus.show_light: glEnable(GL_LIGHTING)
    # else: glDisable(GL_LIGHTING)
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glMatrixMode(GL_MODELVIEW)
    if not torus.fill:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    # glLoadIdentity()
    # glPushMatrix()
    # glTranslatef(0+torus.cur_pos[0], 0+torus.cur_pos[1], -4+torus.cur_pos[2])
    # glRotatef(torus.rz, 0, 0, 1)
    # glRotatef(torus.ry, 0, 1, 0)
    # glRotatef(torus.rx, 1, 0, 0)
    # torus.draw()
    # glPopMatrix()
    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    # glPushMatrix()
    # glTranslatef(0, 0, -4)
    box.draw()
    # glPopMatrix()
    glDrawElements(GL_TRIANGLES, obj.size_ind, GL_UNSIGNED_INT, 0)


def setup_light():
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, vec(-10, 5, 1, 0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, vec(0.1, 0.1, 0.1, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, vec(1, 0.8, 1, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128)  # ширина бликов 128 - маленький, 1 - большой


# Класс коробки, в которой летает Тор
class Box:
    def __init__(self, q=1.5):
        self.q = q
        self.min_box = [-q, -q, -q / 2]
        self.max_box = [q, q, q / 2]
        colors_box = [[0.8, 0.7, 0.1], [0.25, 0.5, 0.25], [0.4, 0.3, 0.9], [0.1, 0.1, 0.55], [0.6, 0.3, 0.9],
                      [0.75, 0.5, 0.65]]
        lbf = 0
        rbf = 1
        rtf = 2
        ltf = 3
        lbn = 4
        rbn = 5
        rtn = 6
        ltn = 7
        self.list = glGenLists(1)
        vertices = list()
        vertices.extend([-q, -q, -q / 2])
        vertices.extend([q, -q, -q / 2])
        vertices.extend([q, q, -q / 2])
        vertices.extend([-q, q, -q / 2])
        vertices.extend([-q, -q, q / 2])
        vertices.extend([q, -q, q / 2])
        vertices.extend([q, q, q / 2])
        vertices.extend([-q, q, q / 2])
        indices = list()
        indices.extend([lbn, lbf, rbf, rbn])
        indices.extend([lbf, ltf, rtf, rbf])
        indices.extend([lbn, lbf, ltf, ltn])
        indices.extend([rbn, rbf, rtf, rtn])
        indices.extend([ltn, ltf, rtf, rtn])
        indices.extend([lbn, ltn, rtn, rbn])
        colors = list()
        for i in range(6): colors.extend([*colors_box[i]])
        indices = (GLuint * len(indices))(*indices)
        vertices = (GLfloat * len(vertices))(*vertices)
        colors = (GLfloat * len(colors))(*colors)
        # glNewList(self.list, GL_COMPILE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        # glEnableClientState(GL_VERTEX_ARRAY)
        # glEnableClientState(GL_COLOR_ARRAY)
        # glVertexPointer(3, GL_FLOAT, 0, vertices)
        # glColorPointer(3, GL_FLOAT, 0, colors)
        # glDrawElements(GL_QUADS, len(indices), GL_UNSIGNED_INT, indices)
        # glPopClientAttrib()
        # glEndList()

    def draw(self):
        glCallList(self.list)


# Класс Тора
class Torus:
    def __init__(self, radius, inner_radius, slices, inner_slices, speed_vec):
        vertices = list()
        normals = list()
        ver = []
        self.speed_vec = speed_vec
        self.rx = 0
        self.ry = 0
        self.rz = 0
        self.spin = False
        self.stop = True
        self.show_tex = False
        self.show_light = False
        self.fill = False
        self.cur_pos = [0, 0, 0]

        u_step = 2 * pi / (slices - 1)
        v_step = 2 * pi / (inner_slices - 1)
        u = pi
        # инициализация координат полигона
        for i in range(slices):
            cos_u = cos(u)
            sin_u = sin(u)
            v = pi
            for j in range(inner_slices):
                cos_v = cos(v)
                sin_v = sin(v)

                d = (radius + inner_radius * cos_v)
                x = d * cos_u
                y = d * sin_u
                z = inner_radius * sin_v

                nx = cos_u * cos_v
                ny = sin_u * cos_v
                nz = sin_v
                k = 2
                vertices.extend([x / k, y / k, z / k])
                ver.append([x / k, y / k, z / k])
                normals.extend([nx, ny, nz])
                v += v_step
            u += u_step

        np_ar = numpy.array(ver)
        self.max_torus = numpy.amax(np_ar, axis=0)
        self.min_torus = numpy.amin(np_ar, axis=0)

        texture = list()
        div_x = numpy.linspace(0, 1, slices)
        div_y = numpy.linspace(0, 1, inner_slices)
        for i in range(len(div_x)):
            for j in range(len(div_y)):
                texture.extend([div_x[i], div_y[j]])

        indices = list()
        for i in range(slices - 1):
            for j in range(inner_slices - 1):
                p = i * inner_slices + j
                indices.extend([p, p + inner_slices, p + inner_slices + 1])
                indices.extend([p, p + inner_slices + 1, p + 1])
        self.ver_sh = vertices
        self.ind_sh = indices
        self.tex_sh = texture
        self.nor_sh = normals
        self.indices = indices
        indices = (GLuint * len(indices))(*indices)
        vertices = (GLfloat * len(vertices))(*vertices)
        normals = (GLfloat * len(normals))(*normals)
        texture = (GLfloat * len(texture))(*texture)

        # self.list = glGenLists(1)
        # glNewList(self.list, GL_COMPILE)
        # glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        # glEnableClientState(GL_VERTEX_ARRAY)
        # # glEnableClientState(GL_NORMAL_ARRAY)
        # glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        # glVertexPointer(3, GL_FLOAT, 0, vertices)
        # glNormalPointer(GL_FLOAT, 0, normals)
        # glTexCoordPointer(2, GL_FLOAT, 0, texture)
        # glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
        # glPopClientAttrib()
        # glEndList()

    def draw(self):
        glCallList(self.list)

    # Проверка столновения. Если оно произошло, то изменить напрвление вектора скорости
    def intersection_with_box(self, box):
        max_torus = self.max_torus
        min_torus = self.min_torus
        max_box = box.max_box
        min_box = box.min_box
        cur = self.cur_pos

        for i in range(3):
            if cur[i] + max_torus[i] >= max_box[i]:
                self.speed_vec[i] *= -1
        for i in range(3):
            if cur[i] + min_torus[i] <= min_box[i]:
                self.speed_vec[i] *= -1


# Загрузка текстуры
def load_textures():
    img = pyglet.image.load('cake.bmp')
    textures = GLuint()
    glGenTextures(1, ctypes.pointer(textures))
    glBindTexture(GL_TEXTURE_2D, textures)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    data = img._current_data
    glTexImage2D(GL_TEXTURE_2D, 0, 3, img.width, img.height, 0, GL_BGR, GL_UNSIGNED_BYTE, data)


# Инициализировать параметры Тора из файла
def open_save():
    f = open('save.txt', 'r')
    text = f.read()
    param = text.split('\n')
    torus.cur_pos = [float(param[0]), float(param[1]), float(param[2])]
    torus.rx = float(param[3])
    torus.ry = float(param[4])
    torus.rz = float(param[5])
    if param[6] == 'True':
        torus.show_tex = True
    else:
        torus.show_tex = False
    if param[7] == 'True':
        torus.show_light = True
    else:
        torus.show_light = False
    if param[8] == 'True':
        torus.spin = True
    else:
        torus.spin = False
    if param[9] == 'True':
        torus.stop = True
    else:
        torus.stop = False
    torus.speed_vec = [float(param[10]), float(param[11]), float(param[12])]
    if param[13] == 'True':
        torus.fill = True
    else:
        torus.fill = False


# Сохранить параметры Тора
def save():
    f = open('save.txt', 'w')
    f.write(str(torus.cur_pos[0]) + '\n')
    f.write(str(torus.cur_pos[1]) + '\n')
    f.write(str(torus.cur_pos[2]) + '\n')
    f.write(str(torus.rx) + '\n')
    f.write(str(torus.ry) + '\n')
    f.write(str(torus.rz) + '\n')
    f.write(str(torus.show_tex) + '\n')
    f.write(str(torus.show_light) + '\n')
    f.write(str(torus.spin) + '\n')
    f.write(str(torus.stop) + '\n')
    f.write(str(torus.speed_vec[0]) + '\n')
    f.write(str(torus.speed_vec[1]) + '\n')
    f.write(str(torus.speed_vec[2]) + '\n')
    f.write(str(torus.fill) + '\n')


class Object():
    def __init__(self):
        self.transl_x = 0
        self.transl_y = 0
        self.transl_z = 0
        self.index = torus.ind_sh
        self.vertex = torus.ver_sh
        self.texture = torus.tex_sh
        self.normal = torus.nor_sh
        self.buff = []
        m = (int)(len(self.vertex) / 3)
        for i in range(m):
            self.buff.extend(self.vertex[3 * i:3 * i + 3])
            self.buff.extend(self.normal[3 * i:3 * i + 3])
        # self.buff = self.vertex
        self.size_buff = len(self.buff)

        self.size = len(self.vertex)
        self.size_ind = len(self.index)
        shader_code = ShaderCode()
        self.vertex_shader_source = shader_code.vertex_shader
        self.fragment_shader_source = shader_code.fragment_shader
        self.shaderProgram = glShaders.GL.shaders.compileProgram(
            glShaders.GL.shaders.compileShader(self.vertex_shader_source, GL_VERTEX_SHADER),
            glShaders.GL.shaders.compileShader(self.fragment_shader_source, GL_FRAGMENT_SHADER))
        self.use()

    def use(self):
        glUseProgram(self.shaderProgram)
        vertex_buffer_object = GLuint(0)
        index_buffer_object = GLuint(0)
        glGenBuffers(1, vertex_buffer_object)
        glGenBuffers(1, index_buffer_object)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
        glBufferData(GL_ARRAY_BUFFER,
                     4 * self.size_buff,
                     (GLfloat * self.size_buff)(*self.buff),
                     GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer_object)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.size_ind, (GLuint * self.size_ind)(*self.index), GL_STATIC_DRAW)
        # pos
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6,
                              ctypes.c_void_p(0))  # 5 - number values in row (for one point)
        glEnableVertexAttribArray(0)
        # normal
        # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(12))
        # glEnableVertexAttribArray(1)

    def updateScale(self, scale):
        Scale_location = glGetUniformLocation(self.shaderProgram, bytes('Scale', encoding='utf - 8'))
        glUniform1f(Scale_location, scale)

    def updateRotateValue(self, angle, ort_x, ort_y, ort_z):
        if ort_x:
            rotateAngle_x_location = glGetUniformLocation(self.shaderProgram,
                                                          bytes('rotateAngle_x', encoding='utf - 8'))
            glUniform1f(rotateAngle_x_location, angle)
        if ort_y:
            rotateAngle_y_location = glGetUniformLocation(self.shaderProgram,
                                                          bytes('rotateAngle_y', encoding='utf - 8'))
            glUniform1f(rotateAngle_y_location, angle)
        if ort_z:
            rotateAngle_z_location = glGetUniformLocation(self.shaderProgram,
                                                          bytes('rotateAngle_z', encoding='utf - 8'))
            glUniform1f(rotateAngle_z_location, angle)

    def updateTranslate(self, x, y, z):
        self.transl_x = x
        self.transl_y = y
        self.transl_z = z
        translate_location_x = glGetUniformLocation(self.shaderProgram, bytes('Translate_x', encoding='utf - 8'))
        glUniform1f(translate_location_x, self.transl_x)
        translate_location_y = glGetUniformLocation(self.shaderProgram, bytes('Translate_y', encoding='utf - 8'))
        glUniform1f(translate_location_y, self.transl_y)
        translate_location_z = glGetUniformLocation(self.shaderProgram, bytes('Translate_z', encoding='utf - 8'))
        glUniform1f(translate_location_z, self.transl_z)

    def changeBuffer(self, vertex):
        glUseProgram(0)
        self.vertex = vertex
        self.size = len(vertex)
        self.use()

    def changeTexture(self):
        Texture_location = glGetUniformLocation(self.shaderProgram, bytes('texture', encoding='utf - 8'))
        glUniform1i(Texture_location, 0)

    def chagneTextureFlag(self, flag):
        Texture_on = glGetUniformLocation(self.shaderProgram, bytes('texture_on', encoding='utf - 8'))
        glUniform1i(Texture_on, flag)

    def changeLightflag(self, flag):
        Light_on = glGetUniformLocation(self.shaderProgram, bytes('light_on', encoding='utf - 8'))
        glUniform1i(Light_on, flag)

    def changeLightPos(self, v):
        Light_pos = glGetUniformLocation(self.shaderProgram, bytes('light_position', encoding='utf - 8'))
        glUniform3fv(Light_pos, 1, (GLfloat * len(v))(*v))

    def Ortho(self, left, right, bottom, top, znear, zfar):
        tx = (-right - left) / (right - left)
        ty = (-top - bottom) / (top - bottom)
        tz = (-zfar - znear) / (zfar - znear)
        mat = [2 / (right - left), 0, 0, tx,
               0, 2 / (top - bottom), 0, ty,
               0, 0, -2 / (zfar - znear), tz,
               0, 0, 0, 1]
        Ortho_location = glGetUniformLocation(self.shaderProgram, bytes('Projection', encoding='utf - 8'))
        glUniformMatrix4fv(Ortho_location, 1, False, (GLfloat * len(mat))(*mat))

    def Proj(self):
        self.Ortho(-1, 1, -1, 1, -1, 1)
        self.updateScale(0.5)

    def myProj(self):
        f = 3 / 8
        a = asin(f / sqrt(2))
        b = asin(f / sqrt(2 - f * f))
        mat = [cos(b), 0, sin(b), 0,
               sin(b)*sin(a), cos(a), -cos(b)*sin(a), 0,
               sin(b)*cos(a), -sin(a), -cos(b)*cos(a), 0,
               0, 0, 0, 1]
        Ortho_location = glGetUniformLocation(self.shaderProgram, bytes('Projection', encoding='utf - 8'))
        glUniformMatrix4fv(Ortho_location, 1, False, (GLfloat * len(mat))(*mat))


def getVertexShader():
    return """
    #version 330 core
    layout (location = 0) in vec3 position;
    out vec3 newColor;


    uniform float Scale = 0.5;
    uniform float rotateAngle_x = 0;
    uniform float rotateAngle_y = 0.3;
    uniform float rotateAngle_z = 0;
    uniform float Translate_x = 0;
    uniform float Translate_y = 0;
    uniform float Translate_z = 0;

    //Projection and ViewPort
    uniform mat4 Projection = mat4(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
    );

        void main()
        {  
            mat3 rot_x = mat3(  
                1.0, 0.0, 0.0,
                0.0, cos(rotateAngle_x), -sin(rotateAngle_x),
                0.0, sin(rotateAngle_x), cos(rotateAngle_x)
            );

            mat3 rot_y = mat3(
                cos(rotateAngle_y), 0.0, sin(rotateAngle_y),
                0.0, 1.0, 0.0,
                -sin(rotateAngle_y), 0.0, cos(rotateAngle_y)
            );

            mat3 rot_z = mat3(
                cos(rotateAngle_z), -sin(rotateAngle_z), 0.0, 
                sin(rotateAngle_z), cos(rotateAngle_z), 0.0, 
                0.0, 0.0, 1.0
            );

            vec3 translate_vec = vec3(Translate_x, Translate_y, Translate_z);
            vec3 pos = vec3(((((position * Scale) * rot_x) * rot_y) * rot_z) + translate_vec);
            vec4 position = vec4(pos, 1) * Projection;     
            gl_Position = position;                                                
            newColor = vec3(1.0, 1.0, 0.0);
        }
    """


def getFragmentShader():
    return """
                                    #version 330
                                    in vec3 newColor;
                                    out vec4 outColor;
                                    void main()
                                    {
                                        outColor =  vec4(newColor, 1);
                                    }
            """


class ShaderCode:
    def __init__(self):
        self.vertex_shader = getVertexShader()
        self.fragment_shader = getFragmentShader()


# setup_light()
# load_textures()
box = Box()
torus = Torus(1, 0.8, 50, 30, speed_vec=[0.05, 0.02, 0.03])
obj = Object()
obj.Proj()
pyglet.app.run()