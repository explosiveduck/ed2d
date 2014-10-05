import ctypes as ct
from cubix.core.opengl import gl
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

