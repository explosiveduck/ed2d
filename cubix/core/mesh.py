
from cubix.core.pycompat import *
from cubix.core import glmath
from cubix.core.opengl import gl, pgl


def buffer_object(data):
    vbo = pgl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    pgl.glBufferData(gl.GL_ARRAY_BUFFER, data, gl.GL_STATIC_DRAW)
    return vbo

def bind_object(dataLoc, vbo):
    gl.glEnableVertexAttribArray(dataLoc)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    pgl.glVertexAttribPointer(dataLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

def unbind_object(dataLoc):

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glDisableVertexAttribArray(dataLoc)

class Mesh(object):

    def __init__(self, program, texture):
        self.program = program
        self.vertLoc = self.program.get_attribute(b'position')
        self.UVLoc = self.program.get_attribute(b'vertexUV')
        self.program.new_uniform(b'model')
        self.texture = texture

        self.xPos = 0
        self.yPos = 0

        self._scale = 1

        self.modelMatrix = glmath.Matrix(4)

        self.data = [
             [0.0, 1.0],
             [1.0, 1.0],
             [0.0, 0.0],
             [1.0, 0.0],
        ]
        self.texCoord = self.data

        self.nverts = 4

        self.vao = pgl.glGenVertexArrays(1)
        self.buffer_objects()

    def scale(self, value):
        self._scale = value

    def translate(self, x, y):
        self.xPos = x
        self.yPos = y

    def update(self):

        vecTrans = glmath.Vector(3, data=(self.xPos, self.yPos, 0.0))
        vecScale = glmath.Vector(3, data=(self._scale, self._scale, 0.0))

        self.modelMatrix = glmath.Matrix(4).i_scale(vecScale).i_translate(vecTrans)


    def render(self):
        
        self.program.set_uniform(b'model', self.modelMatrix)

        gl.glBindVertexArray(self.vao)
        self.texture.bind()

        bind_object(self.vertLoc, self.vbo)
        bind_object(self.UVLoc, self.uvbo)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.nverts)

        unbind_object(self.UVLoc)
        unbind_object(self.vertLoc)

        gl.glBindVertexArray(0)

    def buffer_objects(self):
        self.vbo = buffer_object(self.data)
        self.uvbo = buffer_object(self.texCoord)
