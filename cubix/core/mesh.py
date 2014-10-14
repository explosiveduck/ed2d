
from cubix.core.pycompat import *
from cubix.core import glmath
from cubix.core.opengl import gl, pgl


def buffer_object(data):
    vbo = pgl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    pgl.glBufferData(gl.GL_ARRAY_BUFFER, data, gl.GL_STATIC_DRAW)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    return vbo

def bind_object(dataLoc, vbo):
    gl.glEnableVertexAttribArray(dataLoc)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    pgl.glVertexAttribPointer(dataLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

def unbind_object(dataLoc):
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glDisableVertexAttribArray(dataLoc)

class Mesh(object):

    def __init__(self, program, physicsObject, texture):
        self.program = program
        self.vertLoc = self.program.get_attribute(b'position')
        self.UVLoc = self.program.get_attribute(b'vertexUV')
        self.modelID = self.program.new_uniform(b'model')
        self.texture = texture

        self.nverts = 4
        self.rect = physicsObject.getCollisionModel().getModel()
        self.data = self.rect.getVertices()
        self.texCoord = self.rect.getVertices()
        self.modelMatrix = self.rect.getModelMatrix()

        self.buffer_objects()

    def update(self, physicsObject):
        self.rect = physicsObject.getCollisionModel().getModel()
        self.modelMatrix = self.rect.getModelMatrix()

    def render(self):
        
        self.program.set_uniform_matrix(self.modelID, self.modelMatrix)

        self.texture.bind()

        bind_object(self.vertLoc, self.vbo)
        bind_object(self.UVLoc, self.uvbo)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.nverts)

        unbind_object(self.UVLoc)
        unbind_object(self.vertLoc)

    def buffer_objects(self):
        self.vbo = buffer_object(self.data)
        self.uvbo = buffer_object(self.texCoord)
