import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse


class Window(pyglet.window.Window):
	def __init__(self, width=800, height=800):
		super(Window, self).__init__(vsync=True, resizable=True)
		self.set_size(width, height)
		glViewport(0, 0, width, height)
		self.data = (GLfloat * (self.width * self.height * 3))(0.0)
		self.new_data = (GLfloat * (self.width * self.height * 3))(0.0)
		self.points = []
		self.t_fill = []
		self.flag = False
		self.click1 = False
		self.click2 = False

	def draw_line(self, x1, y1, x2, y2):
		dx = abs(x2 - x1)
		dy = abs(y2 - y1)
		signX = 1 if x1 < x2 else -1
		signY = 1 if y1 < y2 else -1
		e1 = dx - dy
		for i in range(3):
			self.data[(y2 * window.width + x2) * 3 + i] = 1
		while x1 != x2 or y1 != y2:
			for i in range(3):
				self.data[(y1 * window.width + x1) * 3 + i] = 1
			e2 = 2 * e1
			if e2 > -dy:
				e1 -= dy
				x1 += signX
			elif e2 <= dx:
				e1 += dx
				y1 += signY
				self.t_fill.append([x1, y1])
		self.t_fill.append([x2, y2])

	def put_pixel(self, x, y, intens=1):
		for i in range(3):
			self.new_data[(y * window.width + x) * 3 + i] = intens

	def my_accum(self, x, y):
		left_up = self.data[((y + 1) * window.width + x - 1) * 3]
		up = self.data[((y + 1) * window.width + x) * 3]
		right_up = self.data[((y + 1) * window.width + x + 1) * 3]
		left = self.data[(y * window.width + x - 1) * 3]
		this = self.data[(y * window.width + x) * 3]
		right = self.data[(y * window.width + x + 1) * 3]
		left_down = self.data[((y - 1) * window.width + x - 1) * 3]
		down = self.data[((y - 1) * window.width + x) * 3]
		right_down = self.data[((y - 1) * window.width + x + 1) * 3]
		k = 16
		# 1 2 1
		# 2 4 2
		# 1 2 1
		intensity = this + left_up + up + right_up + left + right + left_down + down + right_down
		self.put_pixel(x - 1, y + 1, intens=intensity / k * 1)
		self.put_pixel(x, y + 1, intens=intensity / k * 2)
		self.put_pixel(x + 1, y + 1, intens=intensity / k * 1)
		self.put_pixel(x - 1, y, intens=intensity / k * 2)
		self.put_pixel(x, y, intens=intensity / k * 4)
		self.put_pixel(x + 1, y, intens=intensity / k * 2)
		self.put_pixel(x - 1, y - 1, intens=intensity / k * 1)
		self.put_pixel(x, y - 1, intens=intensity / k * 2)
		self.put_pixel(x + 1, y - 1, intens=intensity / k * 1)

	def post_filtration(self):
		for i in range(1, self.width - 1):
			for j in range(1, self.height - 1):
				self.my_accum(i, j)

	def on_resize(self, width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0, width, 0, height)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def fill(self):
		for j in range(self.height):
			for i in range(self.width):
				for _ in range(self.t_fill.count([i, j])):
					self.flag ^= True
				if self.flag:
					for k in range(3):
						self.data[(j * window.width + i) * 3 + k] = 1

	def fill_prepare(self, x, y):
		if self.data[(y * self.width + x) * 3] != 0:
			return
		while True:
			if x == 0 or self.data[(y * self.width + x - 1) * 3] != 0:
				break
			x -= 1
		st_x = x
		st_y = y
		st = True
		while st or st_x != x or st_y != y:
			st = False
			# self.data[(y * self.width + x) * 3 + 1] = 1  # красим границу
			# print(x, y)
			if x == 0 or self.data[(y * self.width + x - 1) * 3] != 0:  # слева
				self.t_fill.append([x, y])
				if y == self.height - 1 or self.data[((y + 1) * self.width + x) * 3] != 0:  # слева сверху
					if x == self.width - 1 or self.data[(y * self.width + x + 1) * 3] != 0:  # слева сверху справа
						if y == 0 or self.data[((y - 1) * self.width + x) * 3] != 0:  # слева сверху справа снизу
							break
						y -= 1
						t = 4
					else:
						x += 1
						t = 3
				else:
					y += 1
					t = 2
			elif y == self.height - 1 or self.data[((y + 1) * self.width + x) * 3] != 0:  # сверху
				if x == self.width - 1 or self.data[(y * self.width + x + 1) * 3] != 0:  # сверху справа
					if y == 0 or self.data[((y - 1) * self.width + x) * 3] != 0:  # сверху справа снизу
						x -= 1
						t = 1
					else:
						y -= 1
						t = 4
				else:
					tx = x
					while True:
						if tx == 0 or y == self.height - 1 or self.data[(y * self.width + tx) * 3] != 0 or (self.data[(y * self.width + tx - 1) * 3] != 0 and self.data[((y + 1) * self.width + tx) * 3] != 0):
							break
						tx -= 1
					if tx == 0 or self.data[(y * self.width + tx - 1) * 3] != 0 or self.data[(y * self.width + tx) * 3] == 0:
						self.t_fill.append([tx, y])
					x += 1
					t = 3
			elif x == self.width - 1 or self.data[(y * self.width + x + 1) * 3] != 0:  # справа
				self.t_fill.append([x, y])
				if y == 0 or self.data[((y - 1) * self.width + x) * 3] != 0:  # справа снизу
					x -= 1
					t = 1
				else:
					y -= 1
					t = 4
			else:
				x -= 1
				t = 1
			if not (x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1 or self.data[(y * self.width + x - 1) * 3] != 0 or self.data[((y + 1) * self.width + x) * 3] != 0 or self.data[(y * self.width + x + 1) * 3] != 0 or self.data[((y - 1) * self.width + x) * 3] != 0):
				if t == 1:
					y -= 1
				elif t == 2:
					x -= 1
				elif t == 3:
					y += 1
				elif t == 4:
					x += 1
		print(self.t_fill)

	def on_draw(self):
		glClearColor(0, 0, 0, 0)
		glClear(GL_COLOR_BUFFER_BIT)
		self.flag = False
		del self.data
		self.data = (GLfloat * (self.width * self.height * 3))(0.0)
		self.t_fill.clear()
		for i in range(len(self.points)):
			self.draw_line(self.points[i][0], self.points[i][1], self.points[i - 1][0], self.points[i - 1][1])
		if self.click2:
			self.fill()
		if self.click1:
			del self.new_data
			self.new_data = (GLfloat * (self.width * self.height * 3))(0.0)
			self.post_filtration()
			glDrawPixels(self.width, self.height, GL_RGB, GL_FLOAT, self.new_data)
		else:
			glDrawPixels(self.width, self.height, GL_RGB, GL_FLOAT, self.data)
		glFlush()

	def on_mouse_press(self, x, y, button, modifier):
		if button == mouse.LEFT:
			self.points.append([x, y])
		elif button == mouse.RIGHT:
			self.click1 ^= True
		elif button == mouse.MIDDLE:
			self.click2 ^= True

	def on_key_press(self, symbol, modifier):
		if symbol == key.BACKSPACE:
			self.points.clear()

	def update(self, n):
		pass


if __name__ == "__main__":
	window = Window()
	pyglet.app.run()
