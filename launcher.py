#!/usr/bin/python
import platform
import os
from cubix.core import files
# Set PYSDL2_DLL_PATH to deps folder
if platform.system() == 'Windows':
    os.environ['PYSDL2_DLL_PATH'] = files.resolve_path('deps')
from cubix.game import gamemanager

if __name__ == '__main__':
    game = gamemanager.GameManager()
    game.run()
