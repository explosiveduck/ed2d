
import sdl2 as sdl
from ed2d.core.pycompat import *

def init_video():
    ''' Prepare sdl for subsystem initialization, and init sdl video. '''
    sdl.SDL_Init(0)
    sdl.SDL_InitSubSystem(sdl.SDL_INIT_VIDEO)

class Window(object):
    '''
    Creates and manages window related resources.
    This should also support the creation of multiple windows, if you handle
    the events correctly.
    '''
    def __init__(self, title, width, height, fullscreen):
        # TODO - implement fullscreen mode

        # Convert the title to bytes
        self.title = title.encode(encoding='UTF-8')
        self.width = width
        self.height = height
        self.fullscreen = fullscreen

        self.xpos = sdl.SDL_WINDOWPOS_CENTERED
        self.ypos = sdl.SDL_WINDOWPOS_CENTERED

        self.flags = sdl.SDL_WINDOW_OPENGL | sdl.SDL_WINDOW_RESIZABLE

        self.window = sdl.SDL_CreateWindow(self.title,
            self.xpos, self.ypos, self.width, self.height, self.flags)


    def make_current(self, context):
        ''' Make the specified rendering context apply to the window '''
        if context:
            window = self.window
            self.context = context
            context.window = self
            context = context.context

        else:
            if self.context:
                self.context.window = None

            window = None
            context = None
            self.context = None

        sdl.SDL_GL_MakeCurrent(window, context)

    def flip(self):
        ''' Flip the back buffer to the front. '''
        sdl.SDL_GL_SwapWindow(self.window)

    def destroy(self):
        ''' Destroy the window '''
        sdl.SDL_DestroyWindow(self.window)