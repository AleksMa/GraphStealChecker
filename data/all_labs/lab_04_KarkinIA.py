import threading

import glfw
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import math
from array import array


class Frame:
    def __init__(self, sze_x, sze_y):
        self.array = array('B', [0] * (3 * sze_x * sze_y))
        self.x = sze_x
        self.y = sze_y

    def get(self, x, y):
        if self.x <= x or self.y <= y or x < 0 or y < 0:
            return None
        return self.array[int(3 * (self.x * y + x))], self.array[int(3 * (self.x * y + x) + 1)], \
               self.array[int(3 * (self.x * y + x) + 2)]

    def set(self, pos, val):
        if pos[0] >= self.x or pos[1] >= self.y or pos[0] < 0 or pos[1] < 0:
            return
        self.array[int(3 * (self.x * pos[1] + pos[0]))] = int(val[0])
        self.array[int(3 * (self.x * pos[1] + pos[0]) + 1)] = int(val[1])
        self.array[int(3 * (self.x * pos[1] + pos[0]) + 2)] = int(val[2])

    def to_print(self):
        return self.array.tobytes()


size_x, size_y = 200, 200
yellow = (255, 255, 0)
frame = Frame(size_x, size_y)

pos = []
stack = []
end_input = False
smooth = False


def extract(color, k):
    return (color[0] * k, color[1] * k, color[2] * k)


def draw_line(first_pos, second_pos):
    if first_pos[0] > second_pos[0]:
        first_pos, second_pos = second_pos, first_pos
    if first_pos[0] == second_pos[0]:
        i = min(first_pos[1], second_pos[1])
        while i <= max(first_pos[1], second_pos[1]):
            frame.set((first_pos[0], i), yellow)
            if smooth:
                frame.set((first_pos[0] + 1, i), yellow)
                frame.set((first_pos[0] - 1, i), yellow)
            i += 1
    else:
        delta = ((second_pos[0] - first_pos[0]), (second_pos[1] - first_pos[1]))
        # y reverse octants
        if 0 <= delta[1] <= delta[0]:  # 1 oct
            e = -delta[0]
            de = 2 * delta[1]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_x <= second_pos[0]:
                frame.set((pos_x, pos_y), yellow)
                e += de
                pos_x += 1
                if e >= 0:
                    pos_y += 1
                    e -= 2 * delta[0]
                if smooth:
                    cur_int = (e + 2 * delta[0]) / (2 * delta[0])
                    frame.set((pos_x, pos_y - 1), yellow)
                    if pos_x == first_pos[0] or pos_x == second_pos[0]:
                        continue
                    if frame.get(pos_x, pos_y + 1) is not None and \
                            frame.get(pos_x, pos_y + 1)[0] < extract(yellow, cur_int)[0]:
                        frame.set((pos_x, pos_y + 1), extract(yellow, cur_int))
                    if frame.get(pos_x, pos_y - 2) is not None and \
                            frame.get(pos_x, pos_y - 2)[0] < extract(yellow, (1 - cur_int))[0]:
                        frame.set((pos_x, pos_y - 2), extract(yellow, (1 - cur_int)))

        elif delta[1] > delta[0]:  # 2 oct
            e = -delta[1]
            de = 2 * delta[0]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_y <= second_pos[1]:
                frame.set((pos_x, pos_y), yellow)
                e += de
                pos_y += 1
                if e >= 0:
                    pos_x += 1
                    e -= 2 * delta[1]
                if smooth:
                    cur_int = (e + 2 * delta[1]) / (2 * delta[1])
                    frame.set((pos_x + 1, pos_y), yellow)
                    if pos_y == first_pos[1] or pos_y == second_pos[1]:
                        continue
                    if frame.get(pos_x + 2, pos_y) is not None and \
                            frame.get(pos_x + 2, pos_y)[0] < extract(yellow, cur_int)[0]:
                        frame.set((pos_x + 2, pos_y), extract(yellow, cur_int))
                    if frame.get(pos_x - 1, pos_y) is not None and \
                            frame.get(pos_x - 1, pos_y)[0] < extract(yellow, (1 - cur_int))[0]:
                        frame.set((pos_x - 1, pos_y), extract(yellow, (1 - cur_int)))
        elif 0 > delta[1] >= -delta[0]:  # 8 oct
            e = -delta[0]
            de = 2 * delta[1]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_x <= second_pos[0]:
                frame.set((pos_x, pos_y), yellow)
                e -= de
                pos_x += 1
                if e >= 0:
                    pos_y -= 1
                    e -= 2 * delta[0]
                if smooth:
                    cur_int = (e + 2 * delta[0]) / (2 * delta[0])
                    frame.set((pos_x, pos_y - 1), yellow)
                    if pos_x == first_pos[0] or pos_x == second_pos[0]:
                        continue
                    if frame.get(pos_x, pos_y - 2) is not None and \
                            frame.get(pos_x, pos_y - 2)[0] < extract(yellow, cur_int)[0]:
                        frame.set((pos_x, pos_y - 2), extract(yellow, cur_int))
                    if frame.get(pos_x, pos_y + 1) is not None and \
                            frame.get(pos_x, pos_y + 1)[0] < extract(yellow, (1 - cur_int))[0]:
                        frame.set((pos_x, pos_y + 1), extract(yellow, (1 - cur_int)))

        elif delta[1] < - delta[0]:  # 7 oct
            e = delta[1]
            de = 2 * delta[0]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_y >= second_pos[1]:
                frame.set((pos_x, pos_y), yellow)
                e += de
                pos_y -= 1
                if e >= 0:
                    pos_x += 1
                    e += 2 * delta[1]
                if smooth:
                    cur_int = (e - 2 * delta[1]) / (-2 * delta[1])
                    frame.set((pos_x + 1, pos_y), yellow)
                    if pos_y == first_pos[1] or pos_y == second_pos[1]:
                        continue
                    if frame.get(pos_x + 2, pos_y) is not None and \
                            frame.get(pos_x + 2, pos_y)[0] < extract(yellow, cur_int)[0]:
                        frame.set((pos_x + 2, pos_y), extract(yellow, cur_int))
                    if frame.get(pos_x - 1, pos_y) is not None and \
                            frame.get(pos_x - 1, pos_y)[0] < extract(yellow, (1 - cur_int))[0]:
                        frame.set((pos_x - 1, pos_y), extract(yellow, (1 - cur_int)))


def fill():
    while len(stack) > 0:
        pos = stack.pop()
        frame.set(pos, yellow)
        left = pos[0] - 1
        right = pos[0] + 1
        while left >= 0 and frame.get(left, pos[1]) != yellow:
            frame.set((left, pos[1]), yellow)
            left -= 1
        while right < size_x and frame.get(right, pos[1]) != yellow:
            frame.set((right, pos[1]), yellow)
            right += 1
        def fill_line(dl):
            colored_list = [left]
            for i in range(int(left), int(right + 1)):
                if frame.get(i, pos[1] + dl) == yellow:
                    colored_list.append(i)
            colored_list.append(right)
            for i in range(len(colored_list) - 1):
                val = int((colored_list[i] + colored_list[i + 1]) / 2)
                if frame.get(val, pos[1] + dl) is not None and frame.get(val, pos[1] + dl) != yellow:
                    stack.append((val, pos[1] + dl))
        fill_line(-1)
        fill_line(1)


def button_press(window, key, scancode, action, mods):
    global end_input, smooth
    if chr(key) == 'F' and action == 1:
        end_input = not end_input
        if len(pos) >= 3:
            draw_line(pos[0], pos[len(pos) - 1])
    if chr(key) == 'S' and action == 1:
        smooth = not smooth
        draw_line((450, 300), (300 + 150 * 0.7, 300 - 150 * 0.7))
        draw_line((300 + 150 * 0.7, 300 - 150 * 0.7), (300, 150))
        draw_line((300, 150), (300 - 0.7 * 150, 300 - 0.7 * 150))
        draw_line((300 - 0.7 * 150, 300 - 0.7 * 150), (150, 300))
        draw_line((150, 300), (300 - 0.7 * 150, 300 + 0.7 * 150))
        draw_line((300 - 0.7 * 150, 300 + 0.7 * 150), (300, 450))
        draw_line((300, 450), (300 + 0.7 * 150, 300 + 0.7 * 150))
        draw_line((300 + 0.7 * 150, 300 + 0.7 * 150), (450, 300))


def click_mouse(window, button, action, mods):
    global pos
    cursor_pos = glfw.get_cursor_pos(window)
    cursor_pos = (cursor_pos[0], size_y - cursor_pos[1])
    if button == 0 and action == 1 and not end_input:
        pos.append(cursor_pos)
        if len(pos) == 1:
            draw_line(pos[0], (pos[0][0], pos[0][1] + 2) if smooth else pos[0])
        if len(pos) >= 2:
            draw_line(pos[len(pos) - 2], pos[len(pos) - 1])
    elif button == 0 and action == 1 and end_input:
        stack.append(cursor_pos)
        fill()


x_resize, y_resize = size_x, size_y
def resize_start(window, width, height):
    global x_resize, y_resize
    x_resize = (width + 99) // 100 * 100
    y_resize = (height + 99) // 100 * 100


def resize(window, width, height):
    global frame, size_x, size_y
    glfw.set_window_size(window, width, height)
    size_x = width
    size_y = height
    tmp = Frame(width, height)
    for i in range(min(width, frame.x)):
        for j in range(min(height, frame.y)):
            color = frame.get(i, j)
            if color is not None:
                tmp.set((i, j), color)
    frame = tmp


def check_resize(window):
    if size_x != x_resize or size_y != y_resize:
        resize(window, x_resize, y_resize)


def main():
    if not glfw.init():
        return
    window = glfw.create_window(size_x, size_y, "window", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, click_mouse)
    glfw.set_key_callback(window, button_press)
    glfw.set_window_size_callback(window, resize_start)

    timer = time.time()

    def func():
        glDrawPixels(size_x, size_y, GL_RGB, GL_UNSIGNED_BYTE, frame.to_print())

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        t = time.time()
        if t - timer > 0.5:
            timer = t
            check_resize(window)
        func()

        glfw.swap_buffers(window)
        glfw.wait_events()
        time.sleep(0.01)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()