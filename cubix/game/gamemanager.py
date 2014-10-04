import sdl2 as sdl
from cubix.core.opengl import gl
from cubix.core import window
from cubix.core import events
from cubix.core import context

class GameManager(object):
    def __init__(self):

        self.width = 800
        self.height = 600
        self.title = "Cubix"
        self.running = False

        self.events = events.Events()
        self.window = window.Window(self.title, self.width, self.height, False)
        self.context = context.Context(3, 3, 2)
        self.context.window = self.window

    def update(self):
        pass

    def render(self):
        pass

    def do_run(self):
        self.update()
        self.render()
        self.window.flip()

    def run(self):
        self.running = True
        while self.running:
            self.do_run()