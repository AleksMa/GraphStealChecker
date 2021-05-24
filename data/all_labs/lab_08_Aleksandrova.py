import pyglet
from pyglet import *
from pyglet.gl import *
import ratcave as rc
from pyglet.window import key

vert_shader = """
 #version 120
 attribute vec4 vertexPosition;
 uniform mat4 projection_matrix, view_matrix, model_matrix;

 void main()
 {
    gl_Position = projection_matrix * view_matrix * model_matrix * vertexPosition;
 }
 """

frag_shader = """
 #version 120
 uniform vec3 diffuse;
 void main()
 {
    gl_FragColor = vec4(diffuse, 1.);
 }
"""

shader =  rc.Shader(vert = vert_shader,  frag = frag_shader)

window = pyglet.window.Window()
obj_reader = rc.WavefrontReader(rc.resources.obj_primitives)
Cube =  obj_reader.get_mesh('Cube',  position = (0, 0, - 5))
Cube.uniforms['diffuse'] = [0.5, 0.0, 0.8]
Cube1 =  obj_reader.get_mesh('Cube', scale=.7, position = (-6, -5, -12))
Cube1.uniforms['diffuse'] = [0.2, 0.0, 0.8]

scene =  rc.Scene(meshes = [Cube, Cube1])

@window.event
def on_key_press(symbol, modkey):
    if symbol == pyglet.window.key.Q:
        Cube.rotation.x += 10
    if symbol == pyglet.window.key.E:
        Cube.rotation.x -= 10
    if symbol == pyglet.window.key.A:
        Cube.rotation.y += 10
    if symbol == pyglet.window.key.D:
        Cube.rotation.y -= 10
    if symbol == pyglet.window.key.Z:
        Cube.rotation.z += 10
    if symbol == pyglet.window.key.C:
        Cube.rotation.z -= 10

@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()
