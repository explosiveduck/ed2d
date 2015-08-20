from ed2d.opengl import gl, pgl
from ed2d import files
from ed2d.opengl import typeutils
from ed2d.glmath import Matrix, Vector


class ShaderBase(object):
    def create(self):
        self.shader = gl.glCreateShader(self.shaderType)
        pgl.glShaderSource(self.shader, self.shaderData)
        gl.glCompileShader(self.shader)

        status = pgl.glGetShaderiv(self.shader, gl.GL_COMPILE_STATUS)

        if not status:
            print(self.shaderErrorMessage)
            print(pgl.glGetShaderInfoLog(self.shader))
        else:
            print(self.shaderSuccessMessage)


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

        self.uniforms = []
        self.uniformNames = {}

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
            print('Linking error:')
            print(pgl.glGetProgramInfoLog(self.program))
        else:
            print('Program Linked successfully.')

    def use(self, using=True):
        if using is False:
            prog = 0
        else:
            prog = self.program

        gl.glUseProgram(prog)

    def get_attribute(self, name):
        return gl.glGetAttribLocation(self.program, name)

    def get_uniform_name(self, uniID):
        return self.uniformNames[uniID]

    def new_uniform(self, name):
        uniID = len(self.uniforms)
        self.uniformNames[uniID] = name
        self.uniforms.append(gl.glGetUniformLocation(self.program,
                                                     bytes(name)))
        return uniID

    def set_uniform_matrix(self, uniID, value, uniform=None, size=None):
        if not uniform:
            uniform = self.uniforms[uniID]
        if not size:
            size = value.size

        if size == 4:
            pgl.glUniformMatrix4fv(uniform, 1, gl.GL_FALSE, value.c_matrix)
        elif size == 3:
            pgl.glUniformMatrix3fv(uniform, 1, gl.GL_FALSE, value.c_matrix)
        elif size == 2:
            pgl.glUniformMatrix2fv(uniform, 1, gl.GL_FALSE, value.c_matrix)

    def set_uniform_array(self, uniID, value):
        uniform = self.uniforms[uniID]
        try:

            if isinstance(value, Vector):
                value = value.vector
            size = len(value)
            if isinstance(value[0], int):
                if size == 4:
                    gl.glUniform4i(uniform, *value)
                elif size == 3:
                    gl.glUniform3i(uniform, *value)
                elif size == 2:
                    gl.glUniform2i(uniform, *value)
            elif isinstance(value[0], float):
                if size == 4:
                    gl.glUniform4f(uniform, *value)
                elif size == 3:
                    gl.glUniform3f(uniform, *value)
                elif size == 2:
                    gl.glUniform2f(uniform, *value)
        except:
            raise typeError

    def get_uniform(self, uniID):

        uniform = self.uniforms[uniID]

        return uniform

    def set_uniform(self, uniID, value):

        uniform = self.uniforms[uniID]

        # Need to imeplement the matrix uniforms after I
        # Implement the matrix math library
        if isinstance(value, int):
            gl.glUniform1i(uniform, value)
        elif isinstance(value, float):
            gl.glUniform1f(uniform, value)
        else:
            raise TypeError
