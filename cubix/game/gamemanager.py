import ctypes as ct
import sdl2 as sdl

from cubix.core.pycompat import *
from cubix.core import window
from cubix.core import events
from cubix.core import context
from cubix.core import timing
from cubix.core import files
from cubix.core import shaders
from cubix.core.opengl import gl
from cubix.core.opengl import pgl
from cubix.core import glmath


class GameManager(object):
    ''' Entry point into the game, and manages the game in general '''
    def __init__(self):

        self.width = 800
        self.height = 600
        self.title = "Cubix"
        self.running = False

        window.init_video()

        self.fpsTimer = timing.FpsCounter()
        self.fpsEstimate = 0

        self.events = events.Events()
        self.window = window.Window(self.title, self.width, self.height, False)
        self.context = context.Context(3, 3, 2)
        self.context.window = self.window

        self.events.add_listener(self.process_event)

        gl.init()
        major = pgl.glGetInteger(gl.GL_MAJOR_VERSION)
        minor = pgl.glGetInteger(gl.GL_MINOR_VERSION)
        print ('OpenGL Version: {}.{}'.format(major, minor))

        gl.glViewport(0, 0, self.width, self.height)

        vsPath = files.resolve_path('data', 'shaders', 'main.vs')
        fsPath = files.resolve_path('data', 'shaders', 'main.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)

        self.program = shaders.ShaderProgram(vertex, fragment)

        self.program.use()

        self.vertLoc = self.program.get_attribute(b'position')
        self.program.new_uniform(b'ortho')
        #self.program.new_uniform('model')

        self.data = [
            -0.5,  0.5,
             0.5, -0.5,
            -0.5, -0.5,
            -0.5,  0.5,
             0.5,  0.5,
             0.5, -0.5
        ]

        self.ortho = glmath.ortho(0.0, self.width/8, self.height/8, 0.0, -1.0, 1.0)
        self.model = glmath.Matrix(4)

        self.program.set_uniform(b'ortho', self.ortho)
        #self.program.set_uniform('model', self.model)

        self.vbo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        pgl.glBufferData(gl.GL_ARRAY_BUFFER, self.data, gl.GL_STATIC_DRAW)

        self.vao = pgl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        gl.glEnableVertexAttribArray(self.vertLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        pgl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        glerr = gl.glGetError()
        if glerr != 0:
            print ('GLError:', glerr)

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)
        self.ortho = glmath.ortho(0.0, self.width/8, self.height/8, 0.0, -1.0, 1.0)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'window_resized':
            winID, x, y = data
            self.resize(x, y)


    def update(self):
        pass

    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)

    def do_run(self):
        ''' Process a single loop '''
        self.events.process()
        self.update()
        self.render()
        self.window.flip()
        self.fpsTimer.tick()
        if self.fpsTimer.fpsTime >= 2000:
            self.fpsEstimate = self.fpsTimer.get_fps()
            print ("{:.2f} fps".format(self.fpsEstimate))

    def run(self):
        ''' Called from launcher doesnt exit until the game is quit '''
        self.running = True
        while self.running:
            self.do_run()