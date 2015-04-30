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
