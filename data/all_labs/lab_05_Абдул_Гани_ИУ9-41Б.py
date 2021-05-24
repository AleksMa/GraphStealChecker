import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse


class Window(pyglet.window.Window):
	def __init__(self, width=800, height=800):
		super(Window, self).__init__(vsync=True, resizable=True)
		self.set_size(width, height)
		glViewport(0, 0, width, height)
		glLineWidth(2)
		self.lines = []
		self.points = []
		self.click = False

	def on_resize(self, width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0, width, 0, height)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def on_draw(self):
		glClearColor(0, 0, 0, 0)
		glClear(GL_COLOR_BUFFER_BIT)
		lines = []
		if self.click:
			if len(self.lines) > 4:
				for j in range(len(self.points) // 2):
					x1 = self.points[j * 2][0]
					y1 = self.points[j * 2][1]
					x2 = self.points[j * 2 + 1][0]
					y2 = self.points[j * 2 + 1][1]
					ts = []
					for i in range(len(self.lines) // 2):
						x3 = self.lines[i * 2 - 2]
						y3 = self.lines[i * 2 - 1]
						x4 = self.lines[i * 2]
						y4 = self.lines[i * 2 + 1]
						zn = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
						px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / zn
						py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / zn
						if (x4 != x3 and 0 < (px - x3) / (x4 - x3) < 1) or (y4 != y3 and 0 < (py - y3) / (y4 - y3) < 1):
							if x2 != x1 and 0 < (px - x1) / (x2 - x1) < 1:
								t = (px - x1) / (x2 - x1)
								ts.append([t, True])
							elif y2 != y1 and 0 < (py - y1) / (y2 - y1) < 1:
								t = (py - y1) / (y2 - y1)
								ts.append([t, True])
							else:
								if x2 != x1:
									t = (px - x1) / (x2 - x1)
								else:
									t = (py - y1) / (y2 - y1)
								ts.append([t, False])
					ts.sort(reverse=True)
					if len(ts) > 1:
						if ts[0][1]:
							lines.append(x1 + ts[0][0] * (x2 - x1))
							lines.append(y1 + ts[0][0] * (y2 - y1))
							lines.append(x2)
							lines.append(y2)
						if ts[1][1]:
							lines.append(x1)
							lines.append(y1)
							lines.append(x1 + ts[1][0] * (x2 - x1))
							lines.append(y1 + ts[1][0] * (y2 - y1))
					else:
						lines.append(x1)
						lines.append(y1)
						lines.append(x2)
						lines.append(y2)
			glColor3f(0.5, 0.5, 1)
		else:
			for j in range(len(self.points) // 2):
				lines.append(self.points[j * 2][0])
				lines.append(self.points[j * 2][1])
				lines.append(self.points[j * 2 + 1][0])
				lines.append(self.points[j * 2 + 1][1])
			glColor3f(0.5, 1, 0.5)
		pyglet.graphics.draw(len(lines) // 2, GL_LINES, ('v2f', lines))
		# glColor3f(1, 0.5, 0.5)
		# pyglet.graphics.draw(len(self.lines) // 2, GL_LINE_LOOP, ('v2f', self.lines))
		glFlush()

	def on_mouse_press(self, x, y, button, modifier):
		if button == mouse.LEFT:
			self.lines.append(x)
			self.lines.append(y)
		elif button == mouse.RIGHT:
			self.points.append([x, y])
		elif button == mouse.MIDDLE:
			self.click ^= True

	def on_key_press(self, symbol, modifier):
		if symbol == key.BACKSPACE:
			self.lines.clear()
			self.points.clear()

	def update(self, n):
		pass


if __name__ == "__main__":
	window = Window()
	pyglet.app.run()
