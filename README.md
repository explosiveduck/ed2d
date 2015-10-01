[![Codacy Badge](https://api.codacy.com/project/badge/8f1fcec7fc2a4b95b170cfbdbe1a8952)](https://www.codacy.com/app/matthewsitton/ed2d)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/explosiveduck/ed2d/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/explosiveduck/ed2d/?branch=master)
[![Code Health](https://landscape.io/github/explosiveduck/ed2d/master/landscape.svg?style=flat)](https://landscape.io/github/explosiveduck/ed2d/master)
ed2d
=====
This library/engine/framework started out originally as an entry for pyweek 19. We didnt get that far with the game, but we decided to keep the code around and continue extending it. We hope to have an alpha release soon.

Currently written in python using pysdl2 and freetype-py. We only support python 3.3+.

We have created our own opengl binding because originally we had some issues with PyOpenGL that we didn't have time to figure out.The opengl binding is currently located at ed2d/opengl/ if you want to try and extend it any. Hopefully in the future we can split it out into its own repo.

Potential Plans:
* Move away from pysdl2 (We have some features we want that arn't available in SDL2)
  * This would be done with an custom platform implementations on supported platforms.
* Split the opengl binding out from this repo.
* Generate the opengl binding from the xml opengl registry.
* Probably other stuff.
* Easy to use opengl ui framework?

Check the issue tracker for our current and future plans.

Windows Setup:
Download freetype from here(copy the dll acording to the version of python you have installed):
https://dl.dropboxusercontent.com/u/37405488/freetype-vs13-winxp.zip

Download SDL2 from here (again make sure its the currect arch):
https://www.libsdl.org/download-2.0.php

Put both dll's in the deps folder within your project folder (framework in this repo)

Install pysdl2 and freetype-py using pip
pip install pysdl2
pip install freetype-py
