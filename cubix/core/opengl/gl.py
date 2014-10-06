import sys
import ctypes as ct

from cubix.core.pycompat import *
from cubix.core.opengl.glbind import gl_func, glext_func

c_ptrdiff_t = ct.c_ssize_t

# OpenGL types
GLenum = ct.c_uint
GLbitfield = ct.c_uint
GLuint = ct.c_uint
GLint = ct.c_int
GLsizei = ct.c_int
GLboolean = ct.c_ubyte
GLbyte = ct.c_char
GLshort = ct.c_short
GLubyte = ct.c_ubyte
GLushort = ct.c_ushort
GLulong = ct.c_ulong
GLfloat = ct.c_float
GLclampf = ct.c_float
GLdouble = ct.c_double
GLclampd = ct.c_double
GLsizeiptr = c_ptrdiff_t
GLchar = ct.c_char
GLvoid = None


# There are way to many of these to bind manually(225 actually)
# so for now i will only include the ones we use
GL_MAJOR_VERSION = 0x821B
GL_MINOR_VERSION = 0x821C

GL_COLOR_BUFFER_BIT = 0x00004000
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_STENCIL_BUFFER_BIT = 0x00000400

# glDrawArrays 
GL_POINTS = 0x0000
GL_LINE_STRIP = 0x0003
GL_LINE_LOOP = 0x0002
GL_LINES = 0x0001
GL_LINE_STRIP_ADJACENCY = 0x000B
GL_LINES_ADJACENCY = 0x000A
GL_TRIANGLE_STRIP = 0x0005
GL_TRIANGLE_FAN = 0x0006
GL_TRIANGLES = 0x0004
GL_TRIANGLE_STRIP_ADJACENCY = 0x000D
GL_TRIANGLES_ADJACENCY = 0x000C
GL_PATCHES = 0x000E

# glCreateShader
GL_COMPUTE_SHADER = 0x91B9
GL_VERTEX_SHADER = 0x8B31
GL_TESS_CONTROL_SHADER = 0x8E88
GL_TESS_EVALUATION_SHADER = 0x8E87
GL_GEOMETRY_SHADER = 0x8DD9
GL_FRAGMENT_SHADER = 0x8B30

# glBindBuffer
GL_ARRAY_BUFFER = 0x8892
GL_ATOMIC_COUNTER_BUFFER = 0x92C0
GL_COPY_READ_BUFFER = 0x8F36
GL_COPY_WRITE_BUFFER = 0x8F37
GL_DISPATCH_INDIRECT_BUFFER = 0x90EE
GL_DRAW_INDIRECT_BUFFER = 0x8F3F
GL_ELEMENT_ARRAY_BUFFER = 0x8893
GL_PIXEL_PACK_BUFFER = 0x88EB
GL_PIXEL_UNPACK_BUFFER = 0x88EC
GL_QUERY_BUFFER = 0x9192
GL_SHADER_STORAGE_BUFFER = 0x90D2
GL_TEXTURE_BUFFER = 0x8C2A
GL_TRANSFORM_FEEDBACK_BUFFER = 0x8C8E
GL_UNIFORM_BUFFER = 0x8A11

# glBufferData
GL_STREAM_DRAW = 0x88E0
GL_STREAM_READ = 0x88E1
GL_STREAM_COPY = 0x88E2
GL_STATIC_DRAW = 0x88E4
GL_STATIC_READ = 0x88E5
GL_STATIC_COPY = 0x88E6
GL_DYNAMIC_DRAW = 0x88E8
GL_DYNAMIC_READ = 0x88E9
GL_DYNAMIC_COPY = 0x88EA

# glGetShaderiv
GL_SHADER_TYPE = 0x8B4F
GL_DELETE_STATUS = 0x8B80
GL_COMPILE_STATUS = 0x8B81
GL_INFO_LOG_LENGTH = 0x8B84
GL_SHADER_SOURCE_LENGTH = 0x8B88

#glGetProgramiv
GL_LINK_STATUS = 0x8B82
GL_VALIDATE_STATUS = 0x8B82
GL_INFO_LOG_LENGTH = 0x8B83
GL_ATTACHED_SHADERS = 0x8B85
GL_ACTIVE_ATOMIC_COUNTER_BUFFERS = 0x92D9
GL_ACTIVE_ATTRIBUTES = 0x8B89
GL_ACTIVE_ATTRIBUTE_MAX_LENGTH = 0x8B8A
GL_ACTIVE_UNIFORMS = 0x8B86
GL_ACTIVE_UNIFORM_MAX_LENGTH = 0x8B87
GL_PROGRAM_BINARY_LENGTH = 0x8741
GL_COMPUTE_WORK_GROUP_SIZE = 0x8267
GL_TRANSFORM_FEEDBACK_BUFFER_MODE = 0x8C7F
GL_TRANSFORM_FEEDBACK_VARYINGS = 0x8C83
GL_TRANSFORM_FEEDBACK_VARYING_MAX_LENGTH = 0x8C76
GL_GEOMETRY_VERTICES_OUT = 0x8916
GL_GEOMETRY_INPUT_TYPE = 0x8917
GL_GEOMETRY_OUTPUT_TYPE = 0x8918

GL_BYTE = 0x1400
GL_UNSIGNED_BYTE = 0x1401
GL_SHORT = 0x1402
GL_UNSIGNED_SHORT = 0x1403
GL_INT = 0x1404
GL_UNSIGNED_INT = 0x1405
GL_FLOAT = 0x1406
GL_DOUBLE = 0x140A

GL_FALSE = 0
GL_TRUE = 1

def init():
    '''
    This is basically a hack to allow me to load the opengl functions after
    import time. That way the functions can be loaded after the opengl context
    has been created. This is only required for opengl extension
    however we
    might as well do it for all of them.

    Basically the idea is to grab the module object from sys.modules, and then
    basically inject the functions on initialization.

    '''
    gl = sys.modules['cubix.core.opengl.gl']

    noParms = ()

    # Regular OpenGL functions

    _glGetIntergervParams = (GLenum, ct.POINTER(GLint))
    gl.glGetIntegerv = gl_func( 'glGetIntegerv', None, _glGetIntergervParams)
    
    _glClearColorParams = (GLclampf, GLclampf, GLclampf, GLclampf)
    gl.glClearColor = gl_func( 'glClearColor', None, _glClearColorParams)

    gl.glClear = gl_func( 'glClear', None, (GLbitfield,))

    gl.glDrawArrays = gl_func('glDrawArrays', None, (GLenum, GLint, GLsizei))

    gl.glViewport = gl_func('glViewport', None, (GLint, GLint, GLsizei, GLsizei))

    gl.glGetError = gl_func('glGetError', GLenum, noParms)

    # OpenGL Extention Functions

    gl.glGenBuffers = glext_func('glGenBuffers', None, (GLsizei, ct.POINTER(GLuint)))

    gl.glBindBuffer = glext_func('glBindBuffer', None, (GLenum, GLuint))

    gl.glBufferData = glext_func('glBufferData', None, (GLenum, GLsizeiptr, ct.c_void_p, GLenum))

    gl.glGenVertexArrays = glext_func('glGenVertexArrays', None, (GLsizei, ct.POINTER(GLuint)) )

    gl.glBindVertexArray = glext_func('glBindVertexArray', None, (GLuint,))

    gl.glEnableVertexAttribArray = glext_func('glEnableVertexAttribArray', None, (GLuint,))

    gl.glDisableVertexAttribArray = glext_func('glDisableVertexAttribArray', None, (GLuint,))

    gl.glVertexAttribPointer = glext_func('glVertexAttribPointer', None, (GLuint, GLint, GLenum, GLboolean, GLsizei, ct.c_void_p))

    gl.glCreateShader = glext_func('glCreateShader', GLuint, (GLenum,))

    gl.glShaderSource = glext_func('glShaderSource', None, (GLuint, GLsizei, ct.POINTER(ct.POINTER(GLchar)), ct.POINTER(GLint)))

    gl.glCompileShader = glext_func('glCompileShader', None, (GLuint,))

    gl.glCreateProgram = glext_func('glCreateProgram', GLuint, noParms)

    gl.glAttachShader = glext_func('glAttachShader', None, (GLuint, GLuint))

    gl.glLinkProgram = glext_func('glLinkProgram', None, (GLuint,))

    gl.glUseProgram = glext_func('glUseProgram', None, (GLuint,))

    gl.glGetAttribLocation = glext_func('glGetAttribLocation', GLint, (GLuint, ct.POINTER(GLchar)))

    gl.glGetShaderInfoLog = glext_func('glGetShaderInfoLog', None, (GLuint, GLsizei, ct.POINTER(GLsizei), ct.POINTER(GLchar)))

    gl.glGetProgramInfoLog = glext_func('glGetProgramInfoLog', None, (GLuint, GLsizei, ct.POINTER(GLsizei), ct.POINTER(GLchar)))

    gl.glGetShaderiv = glext_func('glGetShaderiv', None, (GLuint, GLenum, ct.POINTER(GLint)))

    gl.glGetProgramiv = glext_func('glGetProgramiv', None, (GLuint, GLenum, ct.POINTER(GLint)))

    gl.glUniformMatrix2fv = glext_func('glUniformMatrix2fv', None, (GLint, GLsizei, GLboolean, ct.POINTER(GLfloat)))

    gl.glUniformMatrix3fv = glext_func('glUniformMatrix3fv', None, (GLint, GLsizei, GLboolean, ct.POINTER(GLfloat)))

    gl.glUniformMatrix4fv = glext_func('glUniformMatrix4fv', None, (GLint, GLsizei, GLboolean, ct.POINTER(GLfloat)))

    gl.glUniform1i = glext_func('glUniform1i', None, (GLint, GLint))

    gl.glUniform2i = glext_func('glUniform2i', None, (GLint, GLint, GLint))

    gl.glUniform3i = glext_func('glUniform3i', None, (GLint, GLint, GLint, GLint))

    gl.glUniform4i = glext_func('glUniform4i', None, (GLint, GLint, GLint, GLint, GLint))

    gl.glUniform1f = glext_func('glUniform1f', None, (GLint, GLfloat))

    gl.glUniform2f = glext_func('glUniform2f', None, (GLint, GLfloat, GLfloat))

    gl.glUniform3f = glext_func('glUniform3f', None, (GLint, GLfloat, GLfloat, GLfloat))

    gl.glUniform4f = glext_func('glUniform4f', None, (GLint, GLfloat, GLfloat, GLfloat, GLfloat))

    gl.glGetUniformLocation = glext_func('glGetUniformLocation', GLint, (GLuint, ct.POINTER(GLchar)))