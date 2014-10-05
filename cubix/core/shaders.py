from cubix.core.pycompat import *
from cubix.core.opengl import gl, pgl
from cubix.core import files
#import OpenGL.GL as gl2


class ShaderBase(object):
    def create(self):
        self.shader = gl.glCreateShader(self.shaderType)
        pgl.glShaderSource(self.shader, self.shaderData)
        gl.glCompileShader(self.shader)

        # Add error checking here need to define the functions in the gl binding

class VertexShader(ShaderBase):
    def __init__(self, path):
        self.shaderData = files.read_file(path)
        self.shaderType = gl.GL_VERTEX_SHADER

class FragmentShader(ShaderBase):
    def __init__(self, path):
        self.shaderData = files.read_file(path)
        self.shaderType = gl.GL_FRAGMENT_SHADER

class ShaderProgram(object):
    def __init__(self, vertex, fragment):
        
        self.vertex = vertex
        self.fragment = fragment

        self.vertex.create()
        self.fragment.create()

        self.program = gl.glCreateProgram()

        gl.glAttachShader(self.program, self.vertex.shader)
        gl.glAttachShader(self.program, self.fragment.shader)

        gl.glLinkProgram(self.program)

        # TODO - add some error checking here

    def use(self, using=True):
        if using is False:
            prog = 0
        else:
            prog = self.program
        print (type(self.program), self.program)
        gl.glUseProgram(prog)

    def get_attribute(self, name):
        return gl.glGetAttribLocation(self.program, name)

    def new_uniform(self, name):
        pass

    def set_uniform(self, name, value):
        pass