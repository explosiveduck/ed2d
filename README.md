ed2d
=====
This library/engine/framework started out originally as an entry for pyweek 19. We didnt get that far with the game, but we decided to keep the code around and continue extending it. We hope to have a first release in a usable state for pyWeek 20 within the next week or so.

Currently written in python using pysdl2 and freetype-py.

We have created our own opengl binding because originally we had some issues with PyOpenGL that we didn't have time to figure out.The opengl binding is currently located at ed2d/opengl/ if you want to try and extend it any. Hopefully in the future we can split it out into its own repo

Future Wants
* Move away from pysdl2 (We have some features we want that arn't available in SDL2)
  * This would be done with an custom platform implementations on supported platforms.
* Split the opengl binding out from this repo.
* Generate the opengl binding from the xml opengl registry.
* Probably other stuff.
* Easy to use opengl ui framework?

View our current todo list here:
[TODO List](https://msitton.com/pad/p/r.5ac11357a3c159c9dda4a4e33badf95e)

Windows Setup:
Download freetype from here(copy the dll acording to the version of python you have installed):
https://dl.dropboxusercontent.com/u/37405488/freetype-vs13-winxp.zip

Download SDL2 from here (again make sure its the currect arch):
https://www.libsdl.org/download-2.0.php

Put both dll's in the deps folder within your project folder (framework in this repo)

Install pysdl2 and freetype-py using pip
pip install pysdl2
pip install freetype-py

Currently we are only going to offically support python 3.3+. Currently the code does run under python 2.7, however we have plans in the short-term to drop our naive python 2.7 support. We might look into using something like six, or 3to2 in the future, but it is currently advised to stick to 3.3+.
