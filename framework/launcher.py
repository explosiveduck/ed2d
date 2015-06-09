#!/usr/bin/python
import platform
import os
import sys
import argparse


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

def cmd_args():
    parser = argparse.ArgumentParser(description='Welcome to the ED2D Framework!')

    parser.add_argument('-g', '--game', type=str, help='The gamemodule to import, by default gamemanager is used.')

    args = vars(parser.parse_args())

    return args

# Set PYSDL2_DLL_PATH to deps folder
if platform.system() == 'Windows':
    os.environ['PYSDL2_DLL_PATH'] = files.resolve_path('deps')



if __name__ == '__main__':
    args = cmd_args()

    importSet = False

    # Process the command line arguments and remove any that have not been used
    delItems = []
    for item in args:
        if args[item] is None:
            delItems.append(item)
            
    
    if args['game']:
        if 'framework.' in args['game']:
            importSet = True
        delItems.append('game')
    
    if importSet == True:
        gamemanager = __import__(args['game'], fromlist=[args['game']])
    else:
        from framework import gamemanager

    # You cant delete an item when iterating on it so we delete it afterwards
    for item in delItems:
        del args[item]
    if hasattr(gamemanager, 'GameManager'):
        game = gamemanager.GameManager()
        game.run()
    else:
        print ('Module does not contain GameManager.')
