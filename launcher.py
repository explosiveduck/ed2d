#!/usr/bin/python
import platform
import os
from ed2d.core import files
# Set PYSDL2_DLL_PATH to deps folder
if platform.system() == 'Windows':
    os.environ['PYSDL2_DLL_PATH'] = files.resolve_path('deps')
from ed2d.game import gamemanager

if __name__ == '__main__':
    game = gamemanager.GameManager()
    game.run()
