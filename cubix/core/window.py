
import sdl2 as sdl

class Window(object):
    def __init__(self, title, width, height, fullscreen):
        self.title = title
        self.width = width
        self.height = height
        self.fullscreen = fullscreen

    def make_current(self, context):
        pass

    def flip(self):
        pass

    def destroy(self):
        pass