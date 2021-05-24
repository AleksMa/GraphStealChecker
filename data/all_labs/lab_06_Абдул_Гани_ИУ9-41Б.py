import pyglet
import random
from math import *
from pyglet.gl import *
from pyglet.window import key


def calc_cylinder(c, h, z, q, t):
	array = []
	for i in range(c):
		for j in range(z):
			array.append([sin(i / c * pi * 2) * (j + 1) / z * t, cos(i / c * pi * 2) * (j + 1) / z * t, -h / 2, (j + 1) / z, (j + 1) / z, 0, 0, -1])
			array.append([sin(i / c * pi * 2) * j / z * t, cos(i / c * pi * 2) * j / z * t, -h / 2, j / z, (j + 1) / z, 0, 0, -1])
			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z * t, cos((i + 1) / c * pi * 2) * (j + 1) / z * t, -h / 2, (j + 1) / z, (j + 1) / z, 0, 0, -1])

			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z * t, cos((i + 1) / c * pi * 2) * (j + 1) / z * t, -h / 2, (j + 1) / z, (j + 1) / z, 0, 0, -1])
			array.append([sin((i + 1) / c * pi * 2) * j / z * t, cos((i + 1) / c * pi * 2) * j / z * t, -h / 2, j / z, j / z, 0, 0, -1])
			array.append([sin(i / c * pi * 2) * j / z * t, cos(i / c * pi * 2) * j / z * t, -h / 2, j / z, j / z, 0, 0, -1])

			array.append([sin(i / c * pi * 2) * j / z, cos(i / c * pi * 2) * j / z, h / 2, j / z, j / z, 0, 0, 1])
			array.append([sin(i / c * pi * 2) * (j + 1) / z, cos(i / c * pi * 2) * (j + 1) / z, h / 2, (j + 1) / z, (j + 1) / z, 0, 0, 1])
			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z, cos((i + 1) / c * pi * 2) * (j + 1) / z, h / 2, (j + 1) / z, (j + 1) / z, 0, 0, 1])

			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z, cos((i + 1) / c * pi * 2) * (j + 1) / z, h / 2, (j + 1) / z, (j + 1) / z, 0, 0, 1])
			array.append([sin((i + 1) / c * pi * 2) * j / z, cos((i + 1) / c * pi * 2) * j / z, h / 2, j / z, j / z, 0, 0, 1])
			array.append([sin(i / c * pi * 2) * j / z, cos(i / c * pi * 2) * j / z, h / 2, j / z, j / z, 0, 0, 1])

		for j in range(q):
			array.append([sin(i / c * pi * 2) * t, cos(i / c * pi * 2) * t, h * j / q - h / 2, i / c, 1, sin(i / c * pi * 2), cos(i / c * pi * 2), 0])
			array.append([sin((i + 1) / c * pi * 2) * t, cos((i + 1) / c * pi * 2) * t, h * j / q - h / 2, (i + 1) / c, 1, sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), 0])
			array.append([sin(i / c * pi * 2), cos(i / c * pi * 2), h * (j + 1) / q - h / 2, i / c, 0, sin(i / c * pi * 2), cos(i / c * pi * 2), 0])

			array.append([sin((i + 1) / c * pi * 2) * t, cos((i + 1) / c * pi * 2) * t, h * j / q - h / 2, (i + 1) / c, 1, sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), 0])
			array.append([sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), h * (j + 1) / q - h / 2, (i + 1) / c, 0, sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), 0])
			array.append([sin(i / c * pi * 2), cos(i / c * pi * 2), h * (j + 1) / q - h / 2, i / c, 0, sin(i / c * pi * 2), cos(i / c * pi * 2), 0])
	return array


def mat4(*args):
	return (GLfloat*16)(*list(args))


def vec4(*args):
	return (GLfloat*4)(*list(args))


class Window(pyglet.window.Window):
	def __init__(self, width=800, height=800):
		super(Window, self).__init__(vsync=True, resizable=True)
		self.set_size(width, height)
		self.x = 0  # 0
		self.y = 0  # 1
		self.figure = None
		self.segment = 10  # 2
		self.h = 2  # 3
		self.angleA = 0
		self.angleB = 0
		self.scale = 0.2  # 4
		self.zz = 1  # 5
		self.vv = 1  # 6
		self.counter = 0  # 7
		self.key = None
		self.full = True  # 8 BOOL
		self.anim = False  # 9 BOOL
		self.texture_en = True  # 10 BOOL
		self.light = 0  # 11
		self.light_random = [random.random() for _ in range(48)]  # 12..59
		self.texture = pyglet.resource.image("texture.bmp")
		glViewport(0, 0, width, height)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)
		glEnable(GL_NORMALIZE)
		glEnable(GL_TEXTURE_2D)
		glLineWidth(4)
		pyglet.clock.schedule_interval(self.update, 1.0 / 60.0)

	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glClearColor(0, 0, 0, 1)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		orthox, orthoy = (self.width / self.height, 1) if self.width > self.height else (1, self.height / self.width)
		glOrtho(-orthox, orthox, -orthoy, orthoy, -1000, 1000)
		# big cul
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		SEGMENT_SPEED = 1
		MOVE_SPEED = 0.01
		SCALE_SPEED = 1.015
		SPEED_H = 0.1
		SPEED_Z = 1
		change = self.figure is None
		if self.key == key.Q:
			self.segment += SEGMENT_SPEED
			change = True
		elif self.key == key.E:
			self.segment -= SEGMENT_SPEED
			if self.segment < 3:
				self.segment = 3
			change = True
		elif self.key == key.W:
			self.anim = True
		elif self.key == key.A:
			self.x -= MOVE_SPEED
		elif self.key == key.S:
			self.anim = False
		elif self.key == key.D:
			self.x += MOVE_SPEED
		elif self.key == key.Z:
			self.scale *= SCALE_SPEED
		elif self.key == key.X:
			self.scale /= SCALE_SPEED
		elif self.key == key.U:
			self.h += SPEED_H
			change = True
		elif self.key == key.I:
			self.h -= SPEED_H
			change = True
		elif self.key == key.T:
			self.zz += SPEED_Z
			change = True
		elif self.key == key.Y:
			self.zz -= SPEED_Z
			if self.zz < 1:
				self.zz = 1
			change = True
		elif self.key == key.N:
			self.vv += SPEED_Z
			change = True
		elif self.key == key.M:
			self.vv -= SPEED_Z
			if self.vv < 1:
				self.vv = 1
			change = True

		glMultMatrixf(mat4(  # translate
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			self.x, self.y, 0, 1,
		))
		if self.anim:
			t = pow(abs(1 - (self.counter % 2)), 2)
			mm = pow(1 - t, 2) * 0.7 + 2 * (1 - t) * t * 1.2 + pow(t, 2) * -0.1
			# self.angleB = self.y * 2
			# self.y = 0
			self.counter += 0.01
		else:
			mm = 1
		glMultMatrixf(mat4(  # scale
			self.scale, 0, 0, 0,
			0, self.scale, 0, 0,
			0, 0, self.scale, 0,
			0, 0, 0, 1,
		))
		ax = cos(self.angleA)
		ay = sin(self.angleA) * cos(self.angleB)
		az = sin(self.angleA) * sin(self.angleB)
		c = cos(pi / 3)
		s = sin(pi / 3)
		if mm < 0:
			mm = 0
		glMultMatrixf(mat4(  # rotate
			c + (1 - c) * ax * ax, (1 - c) * ax * ay + s * az, (1 - c) * ax * az - s * ay, 0,
			(1 - c) * ax * ay - s * az, c + (1 - c) * ay * ay, (1 - c) * ay * az + s * ax, 0,
			(1 - c) * ax * az + s * ay, (1 - c) * ay * az - s * ax, c + (1 - c) * az * az, 0,
			0, 0, 0, 1,
		))
		if not self.full:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		self.figure = calc_cylinder(self.segment, self.h, self.zz, self.vv, mm)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
		glBegin(GL_TRIANGLES)
		for i in range(len(self.figure)):
			if self.texture_en:
				glTexCoord2f(self.figure[i][3], self.figure[i][4])
			glNormal3f(self.figure[i][5], self.figure[i][6], self.figure[i][7])
			glVertex3f(self.figure[i][0], self.figure[i][1], self.figure[i][2])
		glEnd()
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		# light
		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec4(1, 1, 1, 1))
		glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec4(1, 1, 1, 1))
		if self.light > 0:
			for i in range(self.light):
				glLightf(GL_LIGHT0 + i, GL_QUADRATIC_ATTENUATION, 0.5)
				glLightf(GL_LIGHT0 + i, GL_LINEAR_ATTENUATION, 0.3)
				glLightf(GL_LIGHT0 + i, GL_CONSTANT_ATTENUATION, 0.8)
				glLightfv(
					GL_LIGHT0 + i, GL_DIFFUSE,
					vec4(self.light_random[i * 6] / 2, self.light_random[i * 6 + 1] / 2, self.light_random[i * 6 + 2] / 2, 0))
				glLightfv(
					GL_LIGHT0 + i, GL_SPECULAR,
					vec4(0.1, 0.1, 0.1, 0))
				glPushMatrix()
				glTranslatef(self.light_random[i * 6 + 3] * 2 - 1, self.light_random[i * 6 + 4] * 2 - 1, self.light_random[i * 6 + 5] * 2 - 1)
				glLightfv(
					GL_LIGHT0 + i, GL_POSITION,
					vec4(self.light_random[i * 6 + 3] * 2 - 1, self.light_random[i * 6 + 4] * 2 - 1, self.light_random[i * 6 + 5] * 2 - 1, 1))
				glPopMatrix()

	def on_key_press(self, symbol, modifier):
		self.key = symbol
		if symbol == key.SPACE:
			self.full ^= True
		elif self.key == key._0:
			self.texture_en ^= True
		elif self.key == key._1:
			self.light -= 1
			if self.light < 1:
				self.light = 0
				glDisable(GL_LIGHTING)
				glDisable(GL_LIGHT0)
			else:
				glDisable(GL_LIGHT0 + self.light)
		elif self.key == key._2:
			if self.light < 8:
				glEnable(GL_LIGHT0 + self.light)
				self.light += 1
				glEnable(GL_LIGHTING)
		elif self.key == key._7:
			with open('save.txt') as f:
				li = [line.split() for line in f]
			fl = [item for sublist in li for item in sublist]
			self.x = float(fl[0])  # 0
			self.y = float(fl[1])  # 1
			self.figure = None
			self.segment = int(fl[2])  # 2
			self.h = float(fl[3])  # 3
			self.scale = float(fl[4])  # 4
			self.zz = int(fl[5])  # 5
			self.vv = int(fl[6])  # 6
			self.counter = float(fl[7])  # 7
			self.full = fl[8] == "True"  # 8 BOOL
			self.anim = fl[9] == "True"  # 9 BOOL
			self.texture_en = fl[10] == "True"  # 10 BOOL
			self.light = int(fl[11])  # 11
			if self.light > 0:
				glEnable(GL_LIGHTING)
				for i in range(self.light):
					glEnable(GL_LIGHT0 + i)
			self.light_random = [float(fl[12 + i]) for i in range(48)]  # 12..59
		elif self.key == key._8:
			swr = ""
			swr += str(self.x) + "\n"  # 0
			swr += str(self.y) + "\n"  # 1
			swr += str(self.segment) + "\n"  # 2
			swr += str(self.h) + "\n"  # 3
			swr += str(self.scale) + "\n"  # 4
			swr += str(self.zz) + "\n"  # 5
			swr += str(self.vv) + "\n"  # 6
			swr += str(self.counter) + "\n"  # 7
			swr += str(self.full) + "\n"  # 8
			swr += str(self.anim) + "\n"  # 9
			swr += str(self.texture_en) + "\n"  # 10
			swr += str(self.light) + "\n"  # 11
			for i in range(len(self.light_random)):
				swr += str(self.light_random[i]) + "\n"  # 12..59
			with open('save.txt', 'w') as f:
				f.write(swr)
		elif self.key == key.BACKSPACE:
			self.light_random = [random.random() for _ in range(48)]

	def on_key_release(self, symbol, modifiers):
		self.key = None

	def on_mouse_motion(self, x, y, dx, dy):
		self.angleA = x / self.width * pi
		self.angleB = y / self.height * pi

	def update(self, n):
		pass


if __name__ == "__main__":
	window = Window()
	pyglet.app.run()
