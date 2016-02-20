'''
Python GL Wrapper for opengl, gives cleaner access to the opengl api.
Aims to be similar PyOpenGL where it makes sense.
'''

import ctypes as ct

from ed2d.opengl import gl
from ed2d import typeutils



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
    if not typeutils.is_sequence(string):
        string = [string]
    count = len(string)

    strings = []

    for item in string:
         strings.append(typeutils.to_c_str(item))

    cStrings = typeutils.conv_list(strings, ct.POINTER(ct.c_char))

    gl.glShaderSource(shader, count, cStrings, None)


# target, size, data, usage
def glBufferData(target, data, dataType, usage):

    if typeutils.is_sequence(data[0]):
        cData = typeutils.conv_list_2d(data, dataType)
    else:
        cData = typeutils.conv_list(data, dataType)

    cDataPtr = typeutils.cast_ptr(cData, dataType)
    dataSize = ct.sizeof(cData)

    gl.glBufferData(target, dataSize, cDataPtr, usage)

_glTypeMap = {
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

    if not data is None:
        castType = _glTypeMap[ptype]
        try:
            data[0][0]
        except TypeError:
            cData = typeutils.conv_list(data, gl.GLfloat)
        else:
            cData = typeutils.conv_list_2d(data, gl.GLfloat)
        cDataPtr = typeutils.cast_ptr(cData, castType)

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
    length = glGetShaderiv(shader, gl.GL_INFO_LOG_LENGTH)
    infoLog = (gl.GLchar * length)()
    infoLogPtr = typeutils.cast_ptr(infoLog, gl.GLchar)
    gl.glGetShaderInfoLog(shader, length, None, infoLogPtr)
    return infoLog.value


def glGetProgramInfoLog(program):

    length = int(glGetProgramiv(program, gl.GL_INFO_LOG_LENGTH))
    infoLog = (gl.GLchar * length)()
    infoLogPtr = typeutils.cast_ptr(infoLog, gl.GLchar)
    gl.glGetProgramInfoLog(program, length, None, infoLogPtr)
    return infoLog.value


def glGetShaderiv(shader, pname):
    params = gl.GLint(-1)
    gl.glGetShaderiv(shader, pname, ct.byref(params))
    return params.value


def glGetProgramiv(program, pname):
    params = gl.GLint(-1)
    gl.glGetProgramiv(program, pname, ct.byref(params))
    return params.value


def glUniformMatrix2fv(location, count, transpose, value):

    # Check if its 2d or 1d
    if isinstance(value, (list, tuple)):
        if typeutils.is_sequence(value[0]):
            cData = typeutils.conv_list_2d(value, gl.GLfloat)
        else:
            cData = typeutils.conv_list(value, gl.GLfloat)
    else:
        cData = value

    cDataPtr = typeutils.cast_ptr(cData, gl.GLfloat)

    gl.glUniformMatrix2fv(location, count, transpose, cDataPtr)


def glUniformMatrix3fv(location, count, transpose, value):

    # Check if its 2d or 1d
    if isinstance(value, (list, tuple)):
        if typeutils.is_sequence(value[0]):
            cData = typeutils.conv_list_2d(value, gl.GLfloat)
        else:
            cData = typeutils.conv_list(value, gl.GLfloat)
    else:
        cData = value

    cDataPtr = typeutils.cast_ptr(cData, gl.GLfloat)

    gl.glUniformMatrix3fv(location, count, transpose, cDataPtr)


def glUniformMatrix4fv(location, count, transpose, value):
    try:
        gl.glUniformMatrix4fv(location, count, transpose, value[0])
    except Exception: # not sure yet what type the exception it :/
        try:
            cDataPtr = typeutils.cast_ptr(value, gl.GLfloat)
        except TypeError:
            try:
                value[0][0]
            except TypeError:
                cData = typeutils.conv_list(value, gl.GLfloat)
            else:
                cData = typeutils.conv_list_2d(value, gl.GLfloat)
            cDataPtr = typeutils.cast_ptr(cData, gl.GLfloat)

        gl.glUniformMatrix4fv(location, count, transpose, cDataPtr)


def glGenTextures(n):
    textures = (gl.GLuint * n)()
    texPtr = typeutils.cast_ptr(textures, gl.GLuint)
    gl.glGenTextures(n, texPtr)
    return textures[0]


def glTexImage2D(target, level, internalformat, width, height, border, formatGl, dataType, pixels):
    if not (pixels == 0 or pixels is None):
        castType = _glTypeMap[dataType]
        if typeutils.is_sequence(pixels[0]):
            cData = typeutils.conv_list_2d(pixels, castType)
        else:
            cData = typeutils.conv_list(pixels, castType)

        cPixelPtr = typeutils.cast_ptr(cData, castType)
    else:
        cPixelPtr = 0
    gl.glTexImage2D(target, level, internalformat, width, height, border, formatGl, dataType, cPixelPtr)


def glTexSubImage2D(target, level, xoffset, yoffset, width, height, formatGl, dataType, pixels):
    castType = _glTypeMap[dataType]
    if typeutils.is_sequence(pixels[0]):
        cData = typeutils.conv_list_2d(pixels, castType)
    else:
        cData = typeutils.conv_list(pixels, castType)

    cPixelPtr = typeutils.cast_ptr(cData, castType)
    gl.glTexSubImage2D(target, level, xoffset, yoffset, width, height, formatGl, dataType, cPixelPtr)
