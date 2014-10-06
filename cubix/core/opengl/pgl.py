import ctypes as ct

from cubix.core.pycompat import *
from cubix.core.opengl import gl
from cubix.core.opengl import typeutils
from cubix.core.opengl.typeutils import conv_list_2d, is_sequence
from cubix.core.opengl.typeutils import conv_list, cast_ptr

'''
Python GL Wrapper for opengl for cleaner access.
Similar to PyOpenGL in some cases.
'''

def glGetInteger(pname):
    # because this function can return differant amounts of data
    # we need to work around that

    value = (gl.GLint * 16)(*[-1]*16)
    ptr = ct.cast(ct.byref(value), ct.POINTER(gl.GLint))

    gl.glGetIntegerv(pname, ptr)

    valueList = []
    for item in value:
        if item == -1:
            break
        valueList.append(item)
        
    if len(valueList) == 1:
        valueList = valueList[0]

    return valueList

def glShaderSource(shader, string):
    count = 1
    cStrLife = []
    # if is_sequence(string):
    #     count = len(string)
    #     maxStrLen = 0

    #     for item in string:
    #         if len(item) > maxStrLen:
    #             maxStrLen = len(item)

    #     strings = (ct.c_char * maxStrLen * count)
    #     for i, item in enumerate(string):
    #         strings[i] = typeutils.to_c_str(item, cStrLife, True)
    #     cString = ct.cast(strings, ct.POINTER(ct.c_char))

    cString = typeutils.to_c_str(string, cStrLife, True)
    
    gl.glShaderSource(shader, count, ct.pointer(cString), None)

    del cStrLife[:]

# target, size, data, usage
def glBufferData(target, data, usage):

    if is_sequence(data[0]):
        cData = conv_list_2d(data, gl.GLfloat)

    else:
        cData = conv_list(data, gl.GLfloat)

    cDataPtr = cast_ptr(ct.byref(cData), gl.GLfloat)
    dataSize = ct.sizeof(cData)
    
    gl.glBufferData(target, dataSize, cDataPtr, usage)


glTypeMap = {
    gl.GL_BYTE: gl.GLbyte,
    gl.GL_UNSIGNED_BYTE: gl.GLubyte,
    gl.GL_SHORT: gl.GLshort,
    gl.GL_UNSIGNED_SHORT: gl.GLushort,
    gl.GL_INT: gl.GLint,
    gl.GL_UNSIGNED_INT: gl.GLuint,
    gl.GL_FLOAT: gl.GLfloat,
    gl.GL_DOUBLE: gl.GLdouble,
}


# index, size, type, normalized, stride, pointer
def glVertexAttribPointer(index, size, ptype, normalized, stride, data):

    castType = glTypeMap[ptype]
    if data is not None:
        if is_sequence(data[0]):
            cData = conv_list_2d(data, castType)
        else:
            cData = conv_list(data, castType)

        cDataPtr = cast_ptr(ct.byref(cData), castType)

    else:
        cDataPtr = 0


    gl.glVertexAttribPointer(index, size, ptype, normalized, stride, cDataPtr)

# n, arrays
def glGenVertexArrays(n):
    if n > 1:
        arrays = (gl.GLuint * n)
    else:
        arrays = gl.GLuint(0)

    gl.glGenVertexArrays(n, arrays)
    return arrays

# (GLsizei n, GLuint *buffers);
def glGenBuffers(n):
    if n > 1:
        buffers = (gl.GLuint * n)
    else:
        buffers = gl.GLuint(0)
    gl.glGenBuffers(n, ct.pointer(buffers))
    return buffers

def glGetShaderInfoLog(shader):

    length = gl.GLsizei(0)
    infoLog = (gl.GLchar * 2048)()
    infoLogPtr = cast_ptr(infoLog, gl.GLchar)
    gl.glGetShaderInfoLog(shader, 2048, ct.pointer(length), infoLogPtr)
    return infoLog.value

def glGetProgramInfoLog(program):

    length = gl.GLsizei(0)
    infoLog = (gl.GLchar * 2048)()
    infoLogPtr = cast_ptr(infoLog, gl.GLchar)
    gl.glGetProgramInfoLog(program, 2048, ct.pointer(length), infoLogPtr)
    return infoLog.value

def glGetShaderiv(shader, pname):
    params = gl.GLint(-1)
    gl.glGetShaderiv(shader, pname, ct.byref(params))
    return params

def glGetProgramiv(program, pname):
    params = gl.GLint(-1)
    gl.glGetProgramiv(program, pname, ct.byref(params))
    return params