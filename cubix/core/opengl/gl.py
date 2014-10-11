import sys
import ctypes as ct

from cubix.core.pycompat import *
from cubix.core.opengl.glbind import gl_func

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

# glTexImage2d
GL_TEXTURE_2D = 0x0DE1
GL_PROXY_TEXTURE_2D = 0x8064
GL_TEXTURE_1D_ARRAY = 0x8C18
GL_PROXY_TEXTURE_1D_ARRAY = 0x8C19
GL_TEXTURE_RECTANGLE = 0x84F5
GL_PROXY_TEXTURE_RECTANGLE = 0x84F7
GL_TEXTURE_CUBE_MAP_POSITIVE_X = 0x8515
GL_TEXTURE_CUBE_MAP_NEGATIVE_X = 0x8516
GL_TEXTURE_CUBE_MAP_POSITIVE_Y = 0x8517
GL_TEXTURE_CUBE_MAP_NEGATIVE_Y = 0x8518
GL_TEXTURE_CUBE_MAP_POSITIVE_Z = 0x8519
GL_TEXTURE_CUBE_MAP_NEGATIVE_Z = 0x851A
GL_PROXY_TEXTURE_CUBE_MAP = 0x851B

# glTexImage2d
GL_RED = 0x1903
GL_RG = 0x8227
GL_RGB = 0x1907
GL_BGR = 0x80E0
GL_RGBA = 0x1908
GL_BGRA = 0x80E1
GL_RED_INTEGER = 0x8D94
GL_RG_INTEGER = 0x8228
GL_RGB_INTEGER = 0x8D98
GL_BGR_INTEGER = 0x8D9A
GL_RGBA_INTEGER = 0x8D99
GL_BGRA_INTEGER = 0x8D9B
GL_STENCIL_INDEX = 0x1901
GL_DEPTH_COMPONENT = 0x1902
GL_DEPTH_STENCIL = 0x84F9

# glTexParameteri
GL_TEXTURE_1D = 0x0DE0
# GL_TEXTURE_2D
GL_TEXTURE_3D = 0x806F
# GL_TEXTURE_1D_ARRAY
GL_TEXTURE_2D_ARRAY = 0x8C1A
# GL_TEXTURE_RECTANGLE
GL_TEXTURE_CUBE_MAP = 0x8513

# glTexParameteri
GL_DEPTH_STENCIL_TEXTURE_MODE = 0x90EA
GL_TEXTURE_BASE_LEVEL = 0x813C
GL_TEXTURE_COMPARE_FUNC = 0x884D
GL_TEXTURE_COMPARE_MODE = 0x884C
GL_TEXTURE_LOD_BIAS = 0x8501
GL_TEXTURE_MIN_FILTER = 0x2801
GL_TEXTURE_MAG_FILTER = 0x2800
GL_TEXTURE_MIN_LOD = 0x813A
GL_TEXTURE_MAX_LOD = 0x813B
GL_TEXTURE_MAX_LEVEL = 0x813D
GL_TEXTURE_SWIZZLE_R = 0x8E42
GL_TEXTURE_SWIZZLE_G = 0x8E43
GL_TEXTURE_SWIZZLE_B = 0x8E44
GL_TEXTURE_SWIZZLE_A = 0x8E45
GL_TEXTURE_WRAP_S = 0x2802
GL_TEXTURE_WRAP_T = 0x2803
GL_TEXTURE_WRAP_R = 0x8072

GL_NEVER = 0x0200
GL_LESS = 0x0201
GL_EQUAL = 0x0202
GL_LEQUAL = 0x0203
GL_GREATER = 0x0204
GL_NOTEQUAL = 0x0205
GL_GEQUAL = 0x0206
GL_ALWAYS = 0x0207

# GL_DEPTH_COMPONENT
GL_DEPTH_COMPONENTS = 0x8284
GL_STENCIL_COMPONENTS = 0x8285

GL_TEXTURE_BORDER_COLOR = 0x1004
GL_TEXTURE_SWIZZLE_RGBA = 0x8E46

GL_COMPARE_REF_TO_TEXTURE = 0x884E
GL_NONE = 0

#GL_RED
GL_GREEN = 0x1904
GL_BLUE = 0x1905
GL_ALPHA = 0x1906
GL_ZERO = 0
GL_ONE = 1

GL_CLAMP_TO_EDGE = 0x812F
GL_CLAMP_TO_BORDER = 0x812D
GL_MIRRORED_REPEAT = 0x8370
GL_REPEAT = 0x2901
GL_MIRROR_CLAMP_TO_EDGE = 0x8743

GL_NEAREST = 0x2600
GL_LINEAR = 0x2601
GL_NEAREST_MIPMAP_NEAREST = 0x2700                    
GL_LINEAR_MIPMAP_NEAREST = 0x2701
GL_NEAREST_MIPMAP_LINEAR = 0x2702
GL_LINEAR_MIPMAP_LINEAR = 0x2703

# glBindTexture
# GL_TEXTURE_1D
# GL_TEXTURE_2D
# GL_TEXTURE_3D
# GL_TEXTURE_1D_ARRAY
# GL_TEXTURE_2D_ARRAY
# GL_TEXTURE_RECTANGLE
#GL_TEXTURE_CUBE_MAP
GL_TEXTURE_CUBE_MAP_ARRAY = 0x9009
#GL_TEXTURE_BUFFER
GL_TEXTURE_2D_MULTISAMPLE = 0x9100
GL_TEXTURE_2D_MULTISAMPLE_ARRAY = 0x9102

GL_TEXTURE0 = 0x84C0
GL_TEXTURE1 = 0x84C1
GL_TEXTURE2 = 0x84C2
GL_TEXTURE3 = 0x84C3
GL_TEXTURE4 = 0x84C4
GL_TEXTURE5 = 0x84C5
GL_TEXTURE6 = 0x84C6
GL_TEXTURE7 = 0x84C7
GL_TEXTURE8 = 0x84C8
GL_TEXTURE9 = 0x84C9
GL_TEXTURE10 = 0x84CA
GL_TEXTURE11 = 0x84CB
GL_TEXTURE12 = 0x84CC
GL_TEXTURE13 = 0x84CD
GL_TEXTURE14 = 0x84CE
GL_TEXTURE15 = 0x84CF
GL_TEXTURE16 = 0x84D0
GL_TEXTURE17 = 0x84D1
GL_TEXTURE18 = 0x84D2
GL_TEXTURE19 = 0x84D3
GL_TEXTURE20 = 0x84D4
GL_TEXTURE21 = 0x84D5
GL_TEXTURE22 = 0x84D6
GL_TEXTURE23 = 0x84D7
GL_TEXTURE24 = 0x84D8
GL_TEXTURE25 = 0x84D9
GL_TEXTURE26 = 0x84DA
GL_TEXTURE27 = 0x84DB
GL_TEXTURE28 = 0x84DC
GL_TEXTURE29 = 0x84DD
GL_TEXTURE30 = 0x84DE
GL_TEXTURE31 = 0x84DF

# glPixelStorei
GL_PACK_SWAP_BYTES = 0x0D00
GL_PACK_LSB_FIRST = 0x0D01
GL_PACK_ROW_LENGTH = 0x0D02
GL_PACK_IMAGE_HEIGHT = 0x806C
GL_PACK_SKIP_ROWS = 0x0D03
GL_PACK_SKIP_PIXELS = 0x0D04
GL_PACK_SKIP_IMAGES = 0x806B
GL_PACK_ALIGNMENT = 0x0D05
GL_UNPACK_SWAP_BYTES = 0x0CF0
GL_UNPACK_LSB_FIRST = 0x0CF1
GL_UNPACK_ROW_LENGTH = 0x0CF2
GL_UNPACK_IMAGE_HEIGHT = 0x806E
GL_UNPACK_SKIP_ROWS = 0x0CF3
GL_UNPACK_SKIP_PIXELS = 0x0CF4
GL_UNPACK_SKIP_IMAGES = 0x806D
GL_UNPACK_ALIGNMENT = 0x0CF5

# glBlendFunc
#GL_ZERO
#GL_ONE
GL_SRC_COLOR = 0x0300
GL_ONE_MINUS_SRC_COLOR = 0x0301
GL_DST_COLOR = 0x0306
GL_ONE_MINUS_DST_COLOR = 0x0307
GL_SRC_ALPHA = 0x0302
GL_ONE_MINUS_SRC_ALPHA = 0x0303
GL_DST_ALPHA = 0x0304
GL_ONE_MINUS_DST_ALPHA = 0x0305
GL_CONSTANT_COLOR = 0x8001
GL_ONE_MINUS_CONSTANT_COLOR = 0x8002
GL_CONSTANT_ALPHA = 0x8003
GL_ONE_MINUS_CONSTANT_ALPHA = 0x8004
GL_SRC_ALPHA_SATURATE = 0x0308
GL_SRC1_COLOR = 0x88F9
GL_ONE_MINUS_SRC1_COLOR = 0x88FA
GL_SRC1_ALPHA = 0x8589
GL_ONE_MINUS_SRC1_ALPHA = 0x88FB

# glEnable
GL_BLEND = 0x0BE2
GL_MULTISAMPLE = 0x809D

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

    gl.glGenTextures = gl_func('glGenTextures', None, (GLsizei, ct.POINTER(GLuint)))

    gl.glBindTexture = gl_func('glBindTexture', None, (GLenum, GLuint))

    gl.glTexImage2D = gl_func('glTexImage2D', None, (GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, ct.POINTER(GLvoid)))

    gl.glTexParameteri = gl_func('glTexParameteri', None, (GLenum, GLenum, GLint))

    gl.glPixelStorei = gl_func('glPixelStorei', None, (GLenum, GLint))

    gl.glTexSubImage2D = gl_func('glTexSubImage2D', None, (GLenum, GLint, GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, ct.c_void_p))

    # OpenGL Extension Functi ons

    gl.glGenBuffers = gl_func('glGenBuffers', None, (GLsizei, ct.POINTER(GLuint)))

    gl.glBindBuffer = gl_func('glBindBuffer', None, (GLenum, GLuint))

    gl.glBufferData = gl_func('glBufferData', None, (GLenum, GLsizeiptr, ct.c_void_p, GLenum))

    gl.glGenVertexArrays = gl_func('glGenVertexArrays', None, (GLsizei, ct.POINTER(GLuint)) )

    gl.glBindVertexArray = gl_func('glBindVertexArray', None, (GLuint,))

    gl.glEnableVertexAttribArray = gl_func('glEnableVertexAttribArray', None, (GLuint,))

    gl.glDisableVertexAttribArray = gl_func('glDisableVertexAttribArray', None, (GLuint,))

    gl.glVertexAttribPointer = gl_func('glVertexAttribPointer', None, (GLuint, GLint, GLenum, GLboolean, GLsizei, ct.c_void_p))

    gl.glCreateShader = gl_func('glCreateShader', GLuint, (GLenum,))

    gl.glShaderSource = gl_func('glShaderSource', None, (GLuint, GLsizei, ct.POINTER(ct.POINTER(GLchar)), ct.POINTER(GLint)))

    gl.glCompileShader = gl_func('glCompileShader', None, (GLuint,))

    gl.glCreateProgram = gl_func('glCreateProgram', GLuint, noParms)

    gl.glAttachShader = gl_func('glAttachShader', None, (GLuint, GLuint))

    gl.glLinkProgram = gl_func('glLinkProgram', None, (GLuint,))

    gl.glUseProgram = gl_func('glUseProgram', None, (GLuint,))

    gl.glGetAttribLocation = gl_func('glGetAttribLocation', GLint, (GLuint, ct.POINTER(GLchar)))

    gl.glGetShaderInfoLog = gl_func('glGetShaderInfoLog', None, (GLuint, GLsizei, ct.POINTER(GLsizei), ct.POINTER(GLchar)))

    gl.glGetProgramInfoLog = gl_func('glGetProgramInfoLog', None, (GLuint, GLsizei, ct.POINTER(GLsizei), ct.POINTER(GLchar)))

    gl.glGetShaderiv = gl_func('glGetShaderiv', None, (GLuint, GLenum, ct.POINTER(GLint)))

    gl.glGetProgramiv = gl_func('glGetProgramiv', None, (GLuint, GLenum, ct.POINTER(GLint)))

    gl.glUniformMatrix2fv = gl_func('glUniformMatrix2fv', None, (GLint, GLsizei, GLboolean, ct.POINTER(GLfloat)))

    gl.glUniformMatrix3fv = gl_func('glUniformMatrix3fv', None, (GLint, GLsizei, GLboolean, ct.POINTER(GLfloat)))

    gl.glUniformMatrix4fv = gl_func('glUniformMatrix4fv', None, (GLint, GLsizei, GLboolean, ct.POINTER(GLfloat)))

    gl.glUniform1i = gl_func('glUniform1i', None, (GLint, GLint))

    gl.glUniform2i = gl_func('glUniform2i', None, (GLint, GLint, GLint))

    gl.glUniform3i = gl_func('glUniform3i', None, (GLint, GLint, GLint, GLint))

    gl.glUniform4i = gl_func('glUniform4i', None, (GLint, GLint, GLint, GLint, GLint))

    gl.glUniform1f = gl_func('glUniform1f', None, (GLint, GLfloat))

    gl.glUniform2f = gl_func('glUniform2f', None, (GLint, GLfloat, GLfloat))

    gl.glUniform3f = gl_func('glUniform3f', None, (GLint, GLfloat, GLfloat, GLfloat))

    gl.glUniform4f = gl_func('glUniform4f', None, (GLint, GLfloat, GLfloat, GLfloat, GLfloat))

    gl.glGetUniformLocation = gl_func('glGetUniformLocation', GLint, (GLuint, ct.POINTER(GLchar)))

    gl.glActiveTexture = gl_func('glActiveTexture', None, (GLenum,))

    gl.glBlendFunc = gl_func('glBlendFunc', None, (GLenum, GLenum))

    gl.glEnable = gl_func('glEnable', None, (GLenum,))