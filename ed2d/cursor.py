import platform

# from ed2d.cmdargs import  CmdArgs
# forceSDL = CmdArgs.add_arg('sdl', bool, 'Force sdl2 instead of native.')

osName = platform.system()
# if osName == 'Windows':
# 	from ed2d.context.sdl2cursor import Cursor
# # elif osName == 'Linux':
# 	# from ed2d.context.sdl2cursor import Cursor
if osName in ('Windows', 'Darwin', 'Linux'):
    from ed2d.platforms.sdl2cursor import *
else:
    pass

__all__ = ['show_cursor', 'hide_cursor', 'get_cursor_state',
           'move_cursor', 'set_relative_mode', 'is_relative']
