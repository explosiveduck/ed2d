import platform

# from ed2d.cmdargs import  CmdArgs
# forceSDL = CmdArgs.add_arg('sdl', bool, 'Force sdl2 instead of native.')

osName = platform.system()
# if osName == 'Windows':
# 	from ed2d.context.win32 import Context
# # elif osName == 'Linux':
# 	# from ed2d.context.x11 import Context
if osName in ('Windows', 'Darwin', 'Linux'):
    from ed2d.platforms.context.sdl import Context
else:
    pass



__all__ = ['Context']
