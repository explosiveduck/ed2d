import ctypes as ct
from ctypes.util import find_library
from sdl2 import SDL_GL_GetProcAddress

import platform

from cubix.core.pycompat import *

def gl_func(name, returnType, paramTypes):
    ''' Define and load an opengl function '''

    osName = platform.system()

    if osName == 'Linux':
        function = ct.CFUNCTYPE(returnType, *paramTypes)
        libFound = find_library('GL')
        lib = ct.CDLL(libFound)
    elif osName == 'Windows':
        function = ct.WINFUNCTYPE(returnType, *paramTypes)
        libFound = find_library('opengl32')
        lib = ct.WinDLL(libFound)
    elif osName == 'Darwin': # Mac OS X
        function = ct.CFUNCTYPE(returnType, *paramTypes)
        libFound = find_library('/System/Library/Frameworks/OpenGL.framework')
        lib = ct.CDLL(libFound)

    address = getattr(lib, name)

    return ct.cast(address, function)

def glext_func(name, returnType, paramTypes):
    ''' Define and load an opengl extension function '''

    osName = platform.system()

    # Convert the name to bytes
    name = name.encode(encoding='UTF-8')

    if osName == 'Windows':
        function = ct.WINFUNCTYPE(returnType, *paramTypes)
    if osName == 'Linux' or osName == 'Darwin':
        function = ct.CFUNCTYPE(returnType, *paramTypes)

    print (name)
    return ct.cast(SDL_GL_GetProcAddress(name), function)
