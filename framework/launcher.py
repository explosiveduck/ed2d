#!/usr/bin/python
import platform
import os
import sys


# This function is copied from ed2d.files but since it needs
# to be accessable before ed2d is imported it has been copied
# here.
def get_path():

    path0 = os.path.realpath(sys.path[0])
    path1 = os.path.realpath(sys.path[1])

    pathtest = os.sep.join(path0.split(os.sep)[:-1])

    if pathtest == path1:
        return path1
    else:
        return path0

try:
	# Test if the ed2d package is found.
	import ed2d
	del ed2d

except ImportError:

	# Get path of one directory up to get development location.
	path = os.sep.join(get_path().split(os.sep)[:-1])

	# add path where ed2d package is located.
	sys.path.insert(0, path)

from ed2d import files

# Set PYSDL2_DLL_PATH to deps folder
if platform.system() == 'Windows':
    os.environ['PYSDL2_DLL_PATH'] = files.resolve_path('deps')

from framework import gamemanager

if __name__ == '__main__':
    game = gamemanager.GameManager()
    game.run()
