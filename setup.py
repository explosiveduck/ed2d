import platform
from cx_Freeze import setup, Executable
osname = platform.system()

#if osname == "Windows":
    #base = "Win32GUI"
#else:
base = None

setup(
        name = 'Cubix',
        version = '0.1',
        description = 'Cubix 2d Game.',
        executables = [Executable('launcher.py', base=base)]
)