import threading

import glfw
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import copy
from array import array

size_x, size_y = 1000, 1000

mode = 0
pos = [[], [], [], [], []]  # [[mode 0 points - empty], ..., [mode n points: [sub objects], []]]
res1 = None


def inters_p(p1, p2, p3, p4):
    dir_2 = (p4[0] - p3[0], p4[1] - p3[1])
    dir_2_perp = (-dir_2[1], dir_2[0])
    dir_1 = (p2[0] - p1[0], p2[1] - p1[1])
    p1p3 = (p3[0] - p1[0], p3[1] - p1[1])
    if (dir_2_perp[0] * dir_1[0] + dir_2_perp[1] * dir_1[1]) == 0 or dir_2[0] == 0:
        return None
    t_1 = (dir_2_perp[0] * p1p3[0] + dir_2_perp[1] * p1p3[1]) / (dir_2_perp[0] * dir_1[0] + dir_2_perp[1] * dir_1[1])
    t_2 = (dir_1[0] * t_1 - p1p3[0]) / dir_2[0]
    if 0 <= t_1 <= 1 and 0 <= t_2 <= 1:
        return (p1[0] + dir_1[0] * t_1, p1[1] + dir_1[1] * t_1)
    return None


def into_circuit(p, circ):
    count = 0
    for i in range(len(circ) - 1):
        if inters_p(circ[i], circ[i + 1], p, (p[0] + 10, p[1])) is not None:
            count += 1
    return count % 2 == 1


def azerton(circ1, circ2, sign_obj, sign_sub):  # 1 внешний контур и несколько внутренних
    # каждый раз при изменении будем проверять, можно ли применить контур из c1[1], чтобы перевести его в границу
    # если разбили контур на 2, то для каждого проверка, и тп.
    c1 = copy.deepcopy(circ1)
    c2 = copy.deepcopy(circ2)
    res = [[], []]
    starts = []
    ends = []
    new_p_after_c1 = dict()
    new_p_after_c2 = dict()
    for i in range(len(circ1[0][0]) - 1):
        for j in range(len(circ2[0][0]) - 1):
            pnt = inters_p(circ1[0][0][i], circ1[0][0][i + 1], circ2[0][0][j], circ2[0][0][j + 1])
            if pnt is not None:
                if new_p_after_c1.get(i) is None:
                    new_p_after_c1[i] = []
                if new_p_after_c2.get(j) is None:
                    new_p_after_c2[j] = []
                new_p_after_c1[i].append(pnt)
                new_p_after_c2[j].append(pnt)
                v1x = circ1[0][0][i + 1][0] - circ1[0][0][i][0]
                v1y = circ1[0][0][i + 1][1] - circ1[0][0][i][1]
                v2x = circ2[0][0][j][0] - circ1[0][0][i][0]
                v2y = circ2[0][0][j][1] - circ1[0][0][i][1]
                if v1x * v2y - v1y * v2x > 0:
                    starts.append(pnt)
                else:
                    ends.append(pnt)
    k = 0
    kk = 0
    while len(c1[0][0]) != k - 1:
        def dist_sqr(p1):
            return (p1[0] - c1[0][0][k][0]) ** 2 + (p1[1] - c1[0][0][k][1]) ** 2
        if new_p_after_c1.get(kk) is not None:
            new_p_after_c1[kk].sort(key=dist_sqr)
            for el in new_p_after_c1[kk]:
                c1[0][0].insert(k + 1, el)
                k += 1
        k += 1
        kk += 1
    k = 0
    kk = 0
    while len(c2[0][0]) != k - 1:
        def dist_sqr(p1):
            return (p1[0] - c2[0][0][k][0]) ** 2 + (p1[1] - c2[0][0][k][1]) ** 2
        if new_p_after_c2.get(kk) is not None:
            new_p_after_c2[kk].sort(key=dist_sqr)
            for el in new_p_after_c2[kk]:
                c2[0][0].insert(k + 1, el)
                k += 1
        k += 1
        kk += 1
    # если контур внутри, то все его границы становятся вырезанными для основного, а вырезанные вырезанного
    # -- "врезанными"
    if len(starts) == 0:  # непересек
        return None

    while len(starts) > 0:
        res[0].append([])
        st_p = starts[0]
        ind = c1[0][0].index(st_p)
        while True:
            while not (c1[0][0][ind] in ends):
                res[0][len(res[0]) - 1].append(c1[0][0][ind])
                if sign_obj > 0:
                    ind = 0 if ind == len(c1[0][0]) - 2 else ind + 1
                else:
                    ind = len(c2[0][0]) - 2 if ind == 0 else ind - 1
            ends.remove(c1[0][0][ind])
            ind = c2[0][0].index(c1[0][0][ind])
            while not (c2[0][0][ind] in starts):
                res[0][len(res[0]) - 1].append(c2[0][0][ind])
                if sign_sub > 0:
                    ind = 0 if len(c1[0][0]) - 2 == ind else ind + 1
                else:
                    ind = len(c2[0][0]) - 2 if ind == 0 else ind - 1
            starts.remove(c2[0][0][ind])
            if st_p == c2[0][0][ind]:
                res[0][len(res[0]) - 1].append(st_p)
                break
            ind = c1[0][0].index(c2[0][0][ind])
    return res


def azerton_helper(pos):
    # после кажного изменения проверить, нельзя ли связать внутренние контуры с внешним
    # [[pos[1][0]], []] - начальный контур - внешний
    # signs for azerton: 1, 1 - union; 1, -1 - sub; -1, -1 - inters
    # пересекаем с pos[4]
    # выкидываем контур pos 3
    # вырезаем и1з obj и sub union все обр контуры
    res1 = [[], []]
    pos4_new = []
    for p4 in pos[4]:
        a = azerton([[p4], []], [pos[1], []], -1, -1)
        print(a)
        if a is None:
            if into_circuit(p4[0], pos[1][0]):
                pos4_new.append([[p4], []])
        else:
            for a0 in a[0]:
                a0.reverse()
                pos4_new.append([[a0], a[1]])
    p1_new = []
    tmp = azerton([pos[1], []], [pos[3], []], 1, -1)
    if tmp is None:
        if into_circuit(pos[3][0][0], pos[1][0]):
            tmp = [pos[1], pos[3]]
        elif into_circuit(pos[1][0][0], pos[3][0]):
            tmp = [[], []]
        else:
            tmp = [pos[1], []]
    for p1 in tmp[0]:
        p1_new.append([p1, tmp[1]])
    res_list = []
    for p in pos4_new:
        tmpp = p
        take = True
        for sub in pos[2]:
            a = azerton(tmpp, [[sub], []], 1, -1)
            if a is None:
                if into_circuit(tmpp[0][0][0], sub):
                    take = False
                elif into_circuit(sub[0], tmpp[0][0]):
                    tmpp[1].append(sub)
            else:
                tmpp = a
        if take:
            res_list.append(tmpp)
    for p1 in p1_new:  # в p1_new[1] может быть только вычитаемый контур
        tmpp = [[p1[0]], p1[1]]
        take = True
        for sub in pos[2]:
            a = azerton(tmpp, [[sub], []], 1, -1)
            if a is None:
                if into_circuit(tmpp[0][0][0], sub):
                    take = False
                elif into_circuit(sub[0], tmpp[0][0]):
                    if len(tmpp[1]) != 0:
                        a = azerton([[tmp[1][0]], []], [[sub], []], 1, 1)
                        if a is None:
                            if into_circuit(tmp[1][0][0], sub):
                                tmp[1][0] = sub
                            elif not into_circuit(sub[0], tmp[1][0]):
                                tmp[1].append(sub)
                        else:
                            tmp[1][0] = a[0][0]

                    else:
                        tmpp[1].append(sub)
            else:
                tmpp[0] = a[0]
        if take:
            res_list.append(tmpp)
    for r in res_list:
        for rr in r[0]:
            res1[0].append(rr)
        for rr in r[1]:
            res1[1].append(rr)
    return res1




def button_press(window, key, scancode, action, mods):
    global mode, res1, pos
    if '0' <= chr(key) <= '4' and action == 1 and len(pos[mode]) > 0 and len(pos[mode][len(pos[mode]) - 1]) > 0:
        pos[mode][len(pos[mode]) - 1].append(pos[mode][len(pos[mode]) - 1][0])
    if chr(key) == 'S' and action == 1:
        res1 = azerton_helper(pos)
    if chr(key) == '0' and action == 1:  # end write line
        mode = 0
    if '1' <= chr(key) <= '4' and action == 1:
        mode = key - 48
        pos[mode].append([])
    if chr(key) == 'C' and action == 1:  # clear
        mode = 0
        pos = [[], [], [], [], []]
        res1 = None
    if action == 1:
        print('mode:', mode)
    return 0


def click_mouse(window, button, action, mods):
    global pos
    if mode == 0 or action != 1:
        return
    cur_pos = glfw.get_cursor_pos(window)
    pos[mode][len(pos[mode]) - 1].append(((cur_pos[0] - size_x / 2) / size_x * 2,
                                          -(cur_pos[1] - size_y / 2) / size_y * 2))


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

    def func():
        global res1
        # first circuit
        glColor(0, 1, 0)
        for i in range(len(pos[1])):
            glBegin(GL_LINE_STRIP)
            for pnt in pos[1][i]:
                glVertex2f(pnt[0], pnt[1])
            glEnd()
        # first hole
        glColor(0, 1, 1)
        for i in range(len(pos[2])):
            glBegin(GL_LINE_STRIP)
            for pnt in pos[2][i]:
                glVertex2f(pnt[0], pnt[1])
            glEnd()
        # neg circuit
        glColor(1, 0, 0)
        for i in range(len(pos[3])):
            glBegin(GL_LINE_STRIP)
            for pnt in pos[3][i]:
                glVertex2f(pnt[0], pnt[1])
            glEnd()
        # neg hole
        glColor(1, 0.5, 0)
        for i in range(len(pos[4])):
            glBegin(GL_LINE_STRIP)
            for pnt in pos[4][i]:
                glVertex2f(pnt[0], pnt[1])
            glEnd()
        if res1 is not None:
            glColor(1, 1, 1)
            for i in range(len(res1[0])):
                glBegin(GL_LINE_STRIP)
                for p in res1[0][i]:
                    glVertex2f(p[0], p[1])
                glEnd()
            glColor(0.5, 0.5, 0.5)
            for i in range(len(res1[1])):
                glBegin(GL_LINE_STRIP)
                for p in res1[1][i]:
                    glVertex2f(p[0], p[1])
                glEnd()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        func()

        glfw.swap_buffers(window)
        glfw.wait_events()
        time.sleep(0.01)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()