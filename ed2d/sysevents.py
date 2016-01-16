import platform

# from ed2d.cmdargs import  CmdArgs
# forceSDL = CmdArgs.add_arg('sdl', bool, 'Force sdl2 instead of native.')

osName = platform.system()
# if osName == 'Windows':
#     from ed2d.events.win32 import Events
# elif osName == 'Linux':
#     from ed2d.events.x11 import Events
if osName in ('Windows', 'Darwin', 'Linux'):
    from ed2d.platforms.sdl2events import SystemEvents
else:
    pass

__all__ = ['SystemEvents']
