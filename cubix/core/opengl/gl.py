import sys
import ctypes as ct

from cubix.core.opengl.glbind import gl_func

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
GLvoid = None

def init():
    '''
    This is basically a hack to allow me to load the opengl functions after
    import time. That way the functions can be loaded after the opengl context
    has been created. This is only required for opengl extension, however we
    might as well do it for all of them.

    Basically the idea is to grab the module object from sys.modules, and then
    basically inject the functions on initialization.

    '''
    gl = sys.modules['cubix.core.opengl.gl']

    gl.GL_MAJOR_VERSION = 0x821B
    gl.GL_MINOR_VERSION = 0x821C

    gl.GL_COLOR_BUFFER_BIT = 0x00004000
    gl.GL_DEPTH_BUFFER_BIT = 0x00000100
    gl.GL_STENCIL_BUFFER_BIT = 0x00000400

    _glGetIntergervParams = (GLenum, ct.POINTER(GLint))
    gl.glGetIntegerv = gl_func( 'glGetIntegerv', None, _glGetIntergervParams)
    
    _glClearColorParams = (GLclampf, GLclampf, GLclampf, GLclampf)
    gl.glClearColor = gl_func( 'glClearColor', None, _glClearColorParams)

    gl.glClear = gl_func( 'glClear', None, (GLbitfield,))





