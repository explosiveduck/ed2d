from cubix.core.pycompat import *
from cubix.core.opengl import gl, pgl
from cubix.core import files
#import OpenGL.GL as gl2


class ShaderBase(object):
    def create(self):
        self.shader = gl.glCreateShader(self.shaderType)
        pgl.glShaderSource(self.shader, self.shaderData)
        gl.glCompileShader(self.shader)

        status = pgl.glGetShaderiv(self.shader, gl.GL_COMPILE_STATUS)

        if not status:
            print (self.shaderErrorMessage)
            print (pgl.glGetShaderInfoLog(self.shader))
        else:
            print (self.shaderSuccessMessage)

class VertexShader(ShaderBase):
    def __init__(self, path):
        self.shaderData = files.read_file(path)
        self.shaderType = gl.GL_VERTEX_SHADER
        self.shaderErrorMessage = 'Vertex Shader compilation error.'
        self.shaderSuccessMessage = 'Vertex Shader compiled successfully.'

class FragmentShader(ShaderBase):
    def __init__(self, path):
        self.shaderData = files.read_file(path)
        self.shaderType = gl.GL_FRAGMENT_SHADER
        self.shaderErrorMessage = 'Fragment Shader compilation error.'
        self.shaderSuccessMessage = 'Fragment Shader compiled successfully.'

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

        status = pgl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)

        if not status:
            print ('Linking error:')
            print (pgl.glGetProgramInfoLog(self.program))
        else:
            print ('Program Linked successfully.')

    def use(self, using=True):
        if using is False:
            prog = 0
        else:
            prog = self.program

        gl.glUseProgram(prog)

    def get_attribute(self, name):
        return gl.glGetAttribLocation(self.program, name)

    def new_uniform(self, name):
        pass

    def set_uniform(self, name, value):
        pass