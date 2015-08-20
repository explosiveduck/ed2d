#!/usr/bin/python
import platform
import os
import sys

# This function is simplified from ed2d.files. It needed to be used find ed2d
# in development environments. However this limited use case allows for a
# simpler function
def get_path():
    return os.path.realpath(__file__).rsplit(os.path.sep, 1)[0]

try:
    # Test if the ed2d package is found with the python installation.
    import ed2d
    del ed2d

except ImportError:
        # If its not assume its located 1 directory above.
    # Get path of one directory up to get development location.
    path = get_path().rsplit(os.sep, 1)[0]

    # add location of the ed2d package to the python path so
    # it can be imported.
    sys.path.append(path)
    
    import ed2d

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

    game = game()


    if game:
        gamemanager = __import__(game, fromlist=[game])
    else:
        from game import gamemanager

    if hasattr(gamemanager, 'GameManager'):
        game = gamemanager.GameManager()
        game.run()
    else:
        print('Module does not contain GameManager.')
