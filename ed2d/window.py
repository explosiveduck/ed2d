import platform

# from ed2d.cmdargs import  CmdArgs
# forceSDL = CmdArgs.add_arg('sdl', bool, 'Force sdl2 instead of native.')

# osName = platform.system()
# if osName == 'Windows':
# 	from ed2d.window.win32 import Window
# # elif osName == 'Linux':
# 	# from ed2d.window.x11 import Window
# elif osName in ('Darwin', 'Linux'):
# 	from ed2d.window.sdl2 import Window
# else:
# 	pass

from ed2d.platforms.window.sdl import *

__all__ = ['WindowedMode', 'FullscreenMode', 'BorderlessMode', 'Window']
