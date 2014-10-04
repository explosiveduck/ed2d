import sdl2 as sdl

class Context(object):
    def __init__(self, major, minor, msaa):
        self.major = major
        self.minor = minor
        self.msaa = msaa

        self.context = None
        self._window = None

    def destroy(self):
        pass

    @property
    def window(self):
        return self._window
    @window.setter
    def window(self, window):
        self._window = window
        if self.context == None:
            # SDL Context creation here
            pass
    