import ctypes as ct
from ctypes.util import find_library
from sdl2 import SDL_GL_GetProcAddress

import platform

from ed2d.pycompat import *

class BindGL(object):
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
            libFound = find_library('/System/Library/Frameworks/OpenGL.framework')
            self.lib = ct.CDLL(libFound)
            self.funcType = ct.CFUNCTYPE

    def gl_func(self, name, returnType, paramTypes):
        ''' Define and load an opengl function '''
        function = self.funcType(returnType, *paramTypes)

        try:
            address = getattr(self.lib, name)
        except AttributeError:
            name = name.encode(encoding='UTF-8')
            address = SDL_GL_GetProcAddress(name)

        return ct.cast(address, function)

_glbind = BindGL()
gl_func = _glbind.gl_func

__all__ = ['gl_func']