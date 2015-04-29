import platform
from cx_Freeze import setup, Executable
osname = platform.system()

#if osname == "Windows":
    #base = "Win32GUI"
#else:
base = None

setup(
        name = 'ED2D',
        version = '0.2',
        description = '2D Game Engine',
        executables = [Executable('launcher.py', base=base)]
)