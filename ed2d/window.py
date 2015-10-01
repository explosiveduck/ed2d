import platform

# from ed2d.cmdargs import  CmdArgs
# forceSDL = CmdArgs.add_arg('sdl', bool, 'Force sdl2 instead of native.')

osName = platform.system()
# if osName == 'Windows':
#     from ed2d.window.win32 import Window
# elif osName == 'Linux':
#    from ed2d.window.x11 import Window
if osName in ('Windows', 'Darwin', 'Linux'):
    from ed2d.platforms.window.sdl import *
else:
    pass

__all__ = ['WindowedMode', 'FullscreenMode', 'BorderlessMode', 'Window']
