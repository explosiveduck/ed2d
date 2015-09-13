import ctypes as ct
from ctypes.util import find_library

import platform
osName = platform.system()

def define_function(libName, name, returnType, params):
    '''Helper function to help in binding functions'''
    if osName == "Windows":
        function = ct.WINFUNCTYPE(returnType, *params)
        lib = ct.WinDLL(libName)
    elif osName == "Darwin" or osName == "Linux":
        function = ct.FUNCTYPE(returnType, *params)
        lib = ct.CDLL(find_library(libName))

    address = getattr(lib, name)
    new_func = ct.cast(address, function)

    return new_func

if osName == "Windows":
    glGetProcAddress = define_function('opengl32', 'wglGetProcAddress',
            ct.POINTER(ct.c_int), (ct.c_char_p,))

elif osName in ('Linux', 'Darwin', 'Windows'):
    from sdl2 import SDL_GL_GetProcAddress
    glGetProcAddress = SDL_GL_GetProcAddress


class _BindGL(object):
    def __init__(self):
        self.osName = platform.system()

        if self.osName == 'Linux':
            libFound = find_library('GL')
            self.lib = ct.CDLL(libFound)
            self.funcType = ct.CFUNCTYPE
        elif self.osName == 'Windows':
            libFound = find_library('opengl32')
            self.lib = ct.WinDLL(libFound)
            self.funcType = ct.WINFUNCTYPE
        elif self.osName == 'Darwin': # Mac OS X
            libraryPath = '/System/Library/Frameworks/OpenGL.framework'
            libFound = find_library(libraryPath)
            self.lib = ct.CDLL(libFound)
            self.funcType = ct.CFUNCTYPE

    def gl_func(self, name, returnType, paramTypes):
        ''' Define and load an opengl function '''
        function = self.funcType(returnType, *paramTypes)

        try:
            address = getattr(self.lib, name)
        except AttributeError:
            name = name.encode(encoding='UTF-8')
            address = glGetProcAddress(name.encode(encoding='UTF-8'))

        return ct.cast(address, function)


_glbind = _BindGL()
gl_func = _glbind.gl_func

__all__ = ['gl_func', 'define_function']
