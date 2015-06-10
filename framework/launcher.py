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
from ed2d import cmdargs

# Put the deps folder at the beginning of the path on windows so ctypes finds all of our dlls.
if platform.system() == 'Windows':
    os.environ["PATH"] = os.pathsep.join((files.resolve_path('deps'), os.environ["PATH"]))

if __name__ == '__main__':
    cmd = cmdargs.CmdArgs

    cmd.set_description('Welcome to the ED2D Framework!')

    game = cmd.add_arg('game', str, 'The gamemodule to import, by default framework.gamemanager is used.')

    cmd.parse_args()

    importSet = False
    game = game()
    if game:
        if 'framework.' in game:
            importSet = True
    
    
    if importSet == True:
        gamemanager = __import__(game, fromlist=[game])
    else:
        from framework import gamemanager

    if hasattr(gamemanager, 'GameManager'):
        game = gamemanager.GameManager()
        game.run()
    else:
        print ('Module does not contain GameManager.')
