import ctypes as ct
from ctypes.util import find_library
from sdl2 import SDL_GL_GetProcAddress

import platform

from cubix.core.pycompat import *

class BindGL(object):
    def __init__(self):
        self.osName = platform.system()

        if self.osName == 'Linux':
            libFound = find_library('GL')
            self.lib = ct.CDLL(libFound)
        elif self.osName == 'Windows':
            libFound = find_library('opengl32')
            self.lib = ct.WinDLL(libFound)
        elif self.osName == 'Darwin': # Mac OS X
            libFound = find_library('/System/Library/Frameworks/OpenGL.framework')
            self.lib = ct.CDLL(libFound)

    def gl_func(self, name, returnType, paramTypes):
        ''' Define and load an opengl function '''

        if self.osName == 'Linux' or self.osName == 'Darwin':
            function = ct.CFUNCTYPE(returnType, *paramTypes)
        elif self.osName == 'Windows':
            function = ct.WINFUNCTYPE(returnType, *paramTypes)

        try:
            address = getattr(self.lib, name)
        except AttributeError:
            address = SDL_GL_GetProcAddress(name)

        return ct.cast(address, function)

_glbind = BindGL()
gl_func = _glbind.gl_func

__all__ = ['gl_func']