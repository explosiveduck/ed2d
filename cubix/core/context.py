import sdl2 as sdl

class Context(object):
    ''' An OpenGL rendering context '''
    def __init__(self, major, minor, msaa):
        self.major = major
        self.minor = minor
        self.msaa = msaa

        self.profile = sdl.SDL_GL_CONTEXT_PROFILE_CORE

        self.context = None
        self._window = None

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DOUBLEBUFFER, 1)

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MAJOR_VERSION, self.major)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MINOR_VERSION, self.minor)

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_PROFILE_MASK, self.profile)

        if self.msaa < 0:
            sdl.SDL_GL_SetAttribute(sdl.SDL_GL_MULTISAMPLEBUFFERS, 1)
            sdl.SDL_GL_SetAttribute(sdl.SDL_GL_MULTISAMPLESAMPLES, self.msaa)

    def destroy(self):
        ''' Destroy the rendering context '''
        sdl.SDL_GL_DeleteContext(self.context)

    @property
    def window(self):
        return self._window
    @window.setter
    def window(self, window):
        # this mainly exists because we need the sdl window object
        # to be able to create a context
        self._window = window
        if self.context == None:
            # Create context
            self.context = sdl.SDL_GL_CreateContext(self._window.window)
    