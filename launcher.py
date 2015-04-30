#!/usr/bin/python
import platform
import os
from ed2d import files
# Set PYSDL2_DLL_PATH to deps folder
if platform.system() == 'Windows':
    os.environ['PYSDL2_DLL_PATH'] = files.resolve_path('deps')
from framework import gamemanager

if __name__ == '__main__':
    game = gamemanager.GameManager()
    game.run()
