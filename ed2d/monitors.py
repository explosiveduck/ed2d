import platform

# from ed2d.cmdargs import  CmdArgs
# forceSDL = CmdArgs.add_arg('sdl', bool, 'Force sdl2 instead of native.')

osName = platform.system()
# if osName == 'Windows':
#     from ed2d.monitors.win32 import Monitors
# elif osName == 'Linux':
#     from ed2d.monitors.x11 import Monitors
if osName in ('Windows', 'Darwin', 'Linux'):
    from ed2d.platforms.sdl2monitors import Monitors
else:
    pass

__all__ = ['Monitors']
