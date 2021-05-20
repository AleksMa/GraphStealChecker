# диметрия
import ctypes

from OpenGL.raw.GLUT import glutInitDisplayMode
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from math import *
import pyglet

incPos = 0.1
incK = 0.3
alfa = 5
@window.event
def on_key_press(symbol, modifiers):
    global pos
    global k
    if symbol == key.U:
        pos[1] += incPos
    elif symbol == key.J:
        pos[1] -= incPos
    elif symbol == key.I:
        pos[2] -= incPos
    elif symbol == key.K:
        pos[2] += incPos
    elif symbol == key.N:
        pos[0] -= incPos
    elif symbol == key.M:
        pos[0] += incPos
    elif symbol == key.W:
        fi[0] += alfa
    elif symbol == key.E:
        fi[0] -= alfa
    elif symbol == key.S:
        fi[1] += alfa
    elif symbol == key.D:
        fi[1] -= alfa
    elif symbol == key.X:
        fi[2] += alfa
    elif symbol == key.C:
        fi[2] -= alfa
    elif symbol == key.UP:
        k += incK
    elif symbol == key.DOWN:
        k -= incK




pyglet.app.run()