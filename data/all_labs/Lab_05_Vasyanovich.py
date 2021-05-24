import copy
from pyglet.gl import *
from pyglet.window import key, mouse
from shapely.geometry import LineString


Width = 1200
Height = 1200
window = pyglet.window.Window(Width, Height, resizable=True)
window.set_minimum_size(100, 100)
glClearColor(1, 1, 1, 1)
state = -1
victim = []
cutter = []
current_circuit = []
result = []


class Point:
    x = 0
    y = 0
    type = -1
    visited = False
    linker = []
    index = 0

    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy

    def set_index(self, ind):
        self.index = ind

    def set_visited(self):
        self.visited = True
        if len(self.linker) == 2:
            self.linker[0].visited = True
            self.linker[1].visited = True


class Segment:
    start = Point(0, 0)
    stop = Point(0, 0)

    def __init__(self, one, two):
        self.start = one
        self.stop = two


def draw_circuit(circuit, color):
    glBegin(GL_LINE_LOOP)
    glColor3f(*color)
    for point in circuit:
        glVertex2i(point.x, point.y)
    glEnd()


def fill_vertices_list(lists, segments, source):
    for counter in source:
        new = counter.copy()
        pos = len(lists)
        for point in new:
            point.type = -1
            point.index = pos
        lists.append(new)
        i = 0
        j = 1
        length = len(new)
        while i != length:
            segments.append(Segment(new[i], new[j]))
            i += 1
            j += 1
            if j == length:
                j = 0


def insert_point(lis, start, stop, pointer):
    # print(start.x, start.y, "---------", stop.x, stop.y, "----pointer----", pointer.x, pointer.y)
    # for l in lis:
    #     print(l.x, l.y)
    dx = abs(pointer.x - start.x)
    dy = abs(pointer.y - start.y)
    is_delta_x = dx >= dy
    delta_origin = 0
    if is_delta_x:
        delta_origin = dx
    else:
        delta_origin = dy

    start_pos = stop_pos = 0
    length = len(lis)
    for i in range(length):
        cur = lis[i]
        if start.x == cur.x and start.y == cur.y:
            start_pos = i
        if stop.x == cur.x and stop.y == cur.y:
            stop_pos = i
    # print(start_pos, stop_pos, length)
    it = start_pos
    it += 1
    delta = 0
    if stop_pos < start_pos:
        stop_pos += length
    if is_delta_x:
        if it < length:
            delta = abs(lis[it].x - start.x)
        else:
            delta = abs(lis[it - length].x - start.x)
    else:
        if it < length:
            delta = abs(lis[it].y - start.y)
        else:
            delta = abs(lis[it - length].y - start.y)
    while delta < delta_origin:
        if it >= stop_pos:
            break
        it += 1
        if is_delta_x:
            if it < length:
                delta = abs(lis[it].x - start.x)
            else:
                delta = abs(lis[it - length].x - start.x)
        else:
            if it < length:
                delta = abs(lis[it].y - start.y)
            else:
                delta = abs(lis[it - length].y - start.y)
    lis.insert(it, pointer)


def check_inside(pointer, segments):
    counter = 0
    for segment in segments:
        pointer1 = segment.start
        pointer2 = segment.stop
        if pointer1.y == pointer2.y or (pointer1.x < pointer.x and pointer2.x < pointer.x) or ((pointer1.y > pointer.y) == (pointer2.y > pointer.y)):
            continue
        elif pointer1.x >= pointer.x >= pointer2.x:
            t = float(pointer.y - pointer1.y) / float(pointer2.y - pointer1.y)
            x = pointer1.x + t * (pointer2.x - pointer1.x)
            if x <= pointer.x + 0.001:
                continue
        counter += 1
    return counter % 2 != 0


def show_bounds():
    global victim, cutter, state, current_circuit
    for i in victim:
        draw_circuit(i, (0, 0, 0))
    for j in cutter:
        draw_circuit(j, (1, 0, 0))
    if state != 1:
        draw_circuit(current_circuit, (0, 0, 1))


def add_circuit(destination):
    global current_circuit
    if len(current_circuit) > 2:
        destination.append(current_circuit)
    current_circuit = []
    return destination


def draw():
    global victim, cutter, result

    exits = []
    d_segments = []
    r_segments = []
    d_list = []
    r_list = []
    # free_list = []
    d_alone_counter = [False] * len(victim)
    r_alone_counter = [False] * len(cutter)
    fill_vertices_list(d_list, d_segments, victim)
    fill_vertices_list(r_list, r_segments, cutter)

    for d_seg in d_segments:
        for r_seg in r_segments:
            d = LineString(((d_seg.start.x, d_seg.start.y), (d_seg.stop.x, d_seg.stop.y)))
            r = LineString(((r_seg.start.x, r_seg.start.y), (r_seg.stop.x, r_seg.stop.y)))
            res = r.intersection(d)
            if not res.is_empty:
                cross = Point(int(res.x), int(res.y))
                d_alone_counter[d_seg.start.index] = True
                r_alone_counter[r_seg.start.index] = True

                point1 = r_seg.start
                point2 = r_seg.stop
                point3 = d_seg.start
                if (point3.x - point1.x) * (point2.y - point1.y) - (point3.y - point1.y) * (point2.x - point1.x) < 0:
                    cross.type = 0
                else:
                    cross.type = 1

                lis1 = copy.deepcopy(cross)
                lis2 = copy.deepcopy(cross)
                lis1.index = d_seg.start.index
                lis2.index = r_seg.start.index
                link = [lis1, lis2]
                lis1.linker = link
                lis2.linker = link
                insert_point(d_list[d_seg.start.index], d_seg.start, d_seg.stop, lis1)
                insert_point(r_list[r_seg.start.index], r_seg.start, r_seg.stop, lis2)
                if cross.type == 1:
                    exits.append(lis1)

    while len(exits) > 0:
        j = 0
        if exits[-1].visited:
            exits.pop()
            continue
        current_result = []
        current_point = exits[-1]

        start_point = current_point
        while True:
            i = 0
            index = current_point.index
            while i < len(d_list[index]):
                if d_list[index][i].x == current_point.x and d_list[index][i].y == current_point.y:
                    break
                i += 1

            while current_point.type != 0:
                current_point.set_visited()
                current_result.append(current_point)
                i += 1
                if i >= len(d_list[index]):
                    i = 0
                current_point = d_list[index][i]

            current_point = current_point.linker[1]
            index = current_point.index
            i = 0
            while True:
                if r_list[index][i].x == current_point.x and r_list[index][i].y == current_point.y:
                    break
                i += 1

            while current_point.type != 1:
                current_point.set_visited()
                current_result.append(current_point)
                i -= 1
                if i <= 0:
                    i = len(r_list[index]) - 1
                current_point = r_list[index][i]

            current_point = current_point.linker[0]

            if current_point.x == start_point.x and current_point.y == start_point.y:
                break

        result.append(current_result)

    for i in range(len(d_alone_counter)):
        if not d_alone_counter[i]:
            if not check_inside(d_list[i][0], r_segments):
                result.append(d_list[i])

    for i in range(len(r_alone_counter)):
        if not r_alone_counter[i]:
            if check_inside(r_list[i][0], d_segments):
                result.append(r_list[i])


@window.event
def on_draw():
    global result
    window.clear()

    show_bounds()

    for res in result:
        draw_circuit(res, (0, 1, 0))


@window.event
def on_mouse_press(x, y, button, modifiers):
    global current_circuit
    if button == mouse.LEFT:
        if state != 1:
            current_circuit.append(Point(int(x), int(y)))


@window.event
def on_key_press(symbol, modifiers):
    global state, current_circuit, victim, cutter
    if symbol == key.ENTER:
        if state == -1:
            victim = add_circuit(victim)
        elif state == 0:
            cutter = add_circuit(cutter)
    elif symbol == key.SPACE:
        if state == -1:
            state = 0
            victim = add_circuit(victim)
        elif state == 0:
            state = 1
            cutter = add_circuit(cutter)
            draw()


@window.event
def on_resize(width, height):
    global Width, Height
    Width = width
    Height = height


pyglet.app.run()
