import pyglet
import random
from math import *
from pyglet.gl import *
from pyglet.window import key


def draw_cube(c):
	glBegin(GL_QUADS)
	glColor3f(c[0], c[1], c[2])
	glVertex3f(0.5, 0.5, 0.5)
	glVertex3f(0.5, -0.5, 0.5)
	glVertex3f(-0.5, -0.5, 0.5)
	glVertex3f(-0.5, 0.5, 0.5)

	glColor3f(c[3], c[4], c[5])
	glVertex3f(0.5, 0.5, -0.5)
	glVertex3f(0.5, -0.5, -0.5)
	glVertex3f(0.5, -0.5, 0.5)
	glVertex3f(0.5, 0.5, 0.5)

	glColor3f(c[6], c[7], c[8])
	glVertex3f(-0.5, 0.5, -0.5)
	glVertex3f(-0.5, -0.5, -0.5)
	glVertex3f(0.5, -0.5, -0.5)
	glVertex3f(0.5, 0.5, -0.5)

	glColor3f(c[9], c[10], c[11])
	glVertex3f(-0.5, 0.5, 0.5)
	glVertex3f(-0.5, -0.5, 0.5)
	glVertex3f(-0.5, -0.5, -0.5)
	glVertex3f(-0.5, 0.5, -0.5)

	glColor3f(c[12], c[13], c[14])
	glVertex3f(0.5, 0.5, -0.5)
	glVertex3f(0.5, 0.5, 0.5)
	glVertex3f(-0.5, 0.5, 0.5)
	glVertex3f(-0.5, 0.5, -0.5)

	glColor3f(c[15], c[16], c[17])
	glVertex3f(0.5, -0.5, -0.5)
	glVertex3f(0.5, -0.5, 0.5)
	glVertex3f(-0.5, -0.5, 0.5)
	glVertex3f(-0.5, -0.5, -0.5)
	glEnd()


def calc_cylinder(c, h, z, q):
	array = []
	for i in range(c):
		for j in range(z):
			array.append([sin(i / c * pi * 2) * (j + 1) / z, cos(i / c * pi * 2) * (j + 1) / z, -h / 2])
			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z, cos((i + 1) / c * pi * 2) * (j + 1) / z, -h / 2])
			array.append([sin(i / c * pi * 2) * j / z, cos(i / c * pi * 2) * j / z, -h / 2])

			array.append([sin((i + 1) / c * pi * 2) * j / z, cos((i + 1) / c * pi * 2) * j / z, -h / 2])
			array.append([sin(i / c * pi * 2) * j / z, cos(i / c * pi * 2) * j / z, -h / 2])
			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z, cos((i + 1) / c * pi * 2) * (j + 1) / z, -h / 2])

			array.append([sin(i / c * pi * 2) * (j + 1) / z, cos(i / c * pi * 2) * (j + 1) / z, h / 2])
			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z, cos((i + 1) / c * pi * 2) * (j + 1) / z, h / 2])
			array.append([sin(i / c * pi * 2) * j / z, cos(i / c * pi * 2) * j / z, h / 2])

			array.append([sin((i + 1) / c * pi * 2) * j / z, cos((i + 1) / c * pi * 2) * j / z, h / 2])
			array.append([sin(i / c * pi * 2) * j / z, cos(i / c * pi * 2) * j / z, h / 2])
			array.append([sin((i + 1) / c * pi * 2) * (j + 1) / z, cos((i + 1) / c * pi * 2) * (j + 1) / z, h / 2])

		for j in range(q):
			array.append([sin(i / c * pi * 2), cos(i / c * pi * 2), h * j / q - h / 2])
			array.append([sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), h * j / q - h / 2])
			array.append([sin(i / c * pi * 2), cos(i / c * pi * 2), h * (j + 1) / q - h / 2])

			array.append([sin(i / c * pi * 2), cos(i / c * pi * 2), h * (j + 1) / q - h / 2])
			array.append([sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), h * (j + 1) / q - h / 2])
			array.append([sin((i + 1) / c * pi * 2), cos((i + 1) / c * pi * 2), h * j / q - h / 2])
	return array


def mat4(*args):
	return (GLfloat*16)(*list(args))


class Window(pyglet.window.Window):
	def __init__(self, width=800, height=800):
		super(Window, self).__init__(vsync=True, resizable=True)
		self.set_size(width, height)
		self.x = 0
		self.figure = None
		self.y = 0
		self.segment = 10
		self.h = 2
		self.angleA = 0
		self.angleB = 0
		self.scale = 0.5
		self.zz = 1
		self.vv = 1
		self.key = None
		self.full = True
		self.color1 = [random.random() for _ in range(18)]
		self.color2 = [random.random() for _ in range(18)]
		glViewport(0, 0, width, height)
		glEnable(GL_DEPTH_TEST)
		glLineWidth(4)
		pyglet.clock.schedule_interval(self.update, 1.0 / 120.0)

	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glClearColor(0, 0, 0, 1)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		orthox, orthoy = (self.width / self.height, 1) if self.width > self.height else (1, self.height / self.width)
		glOrtho(-orthox, orthox, -orthoy, orthoy, -1000, 1000)
		glRotatef(30, 1, 0, 0)
		glRotatef(30, 0, 1, 0)
		glMatrixMode(GL_MODELVIEW)
		# big cul
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
			self.y += MOVE_SPEED
		elif self.key == key.A:
			self.x -= MOVE_SPEED
		elif self.key == key.S:
			self.y -= MOVE_SPEED
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
		glMultMatrixf(mat4(  # rotate
			c + (1 - c) * ax * ax, (1 - c) * ax * ay + s * az, (1 - c) * ax * az - s * ay, 0,
			(1 - c) * ax * ay - s * az, c + (1 - c) * ay * ay, (1 - c) * ay * az + s * ax, 0,
			(1 - c) * ax * az + s * ay, (1 - c) * ay * az - s * ax, c + (1 - c) * az * az, 0,
			0, 0, 0, 1,
		))
		if not self.full:
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		if change:
			self.figure = calc_cylinder(self.segment, self.h, self.zz, self.vv)
		glBegin(GL_TRIANGLES)
		for i in range(len(self.figure)):
			if i % 12 == 0:
				glColor3f(abs(1 - self.figure[i][0] * 2), abs(1 - self.figure[i][1] * 2), 0.5)
			elif i % 12 == 6:
				glColor3f(abs(1 - self.figure[i][0] * 2), 0.5, abs(1 - self.figure[i][1] * 2))
			glVertex3f(self.figure[i][0], self.figure[i][1], self.figure[i][2])
		glEnd()
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		# small cube
		glLoadIdentity()
		x = -0.9
		y = -0.65
		glMultMatrixf(mat4(  # translate
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			x, y, 0, 1,
		))
		scale = 0.2
		glMultMatrixf(mat4(  # scale
			scale, 0, 0, 0,
			0, scale, 0, 0,
			0, 0, scale, 0,
			0, 0, 0, 1,
		))
		ax = 1 / sqrt(2)
		ay = 1 / sqrt(2)
		az = 0
		angle = 0
		c = cos(angle)
		s = sin(angle)
		glMultMatrixf(mat4(  # rotate
			c + (1 - c) * ax * ax, (1 - c) * ax * ay + s * az, (1 - c) * ax * az - s * ay, 0,
			(1 - c) * ax * ay - s * az, c + (1 - c) * ay * ay, (1 - c) * ay * az + s * ax, 0,
			(1 - c) * ax * az + s * ay, (1 - c) * ay * az - s * ax, c + (1 - c) * az * az, 0,
			0, 0, 0, 1,
		))
		draw_cube(self.color2)

	def on_key_press(self, symbol, modifier):
		self.key = symbol
		if symbol == key.SPACE:
			self.full ^= True
		elif symbol == key.BACKSPACE:
			self.color1 = [random.random() for _ in range(18)]
			self.color2 = [random.random() for _ in range(18)]

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
