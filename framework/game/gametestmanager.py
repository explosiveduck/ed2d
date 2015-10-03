from ed2d import window
from ed2d import events
from ed2d import context
from ed2d import timing
from ed2d import files
from ed2d import shaders
from ed2d.opengl import gl
from ed2d.opengl import pgl
from ed2d import glmath
from ed2d import text

class GameManager(object):
    ''' Entry point into the game, and manages the game in general '''
    def __init__(self):

        self.width = 800
        self.height = 600
        self.title = "Cubix"
        self.running = False

        self.fpsTimer = timing.FpsCounter()
        self.fpsEstimate = 0

        self.events = events.Events()
        self.window = window.Window(self.title, self.width, self.height, window.WindowedMode)
        self.context = context.Context(3, 3, 2)
        self.context.window = self.window

        self.events.add_listener(self.process_event)

        self.keys = []

        gl.init()
        major = pgl.glGetInteger(gl.GL_MAJOR_VERSION)
        minor = pgl.glGetInteger(gl.GL_MINOR_VERSION)
        print('OpenGL Version: ', major, '.', minor)

        gl.glViewport(0, 0, self.width, self.height)

        vsPath = files.resolve_path('data', 'shaders', 'font.vs')
        fsPath = files.resolve_path('data', 'shaders', 'font.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)
        self.program = shaders.ShaderProgram(vertex, fragment)
        self.program.use()
        self.orthoID = self.program.new_uniform(b'ortho')


        fontPath = files.resolve_path('data', 'SourceCodePro-Regular.ttf')
        self.font = text.Font(12, fontPath)
        self.text = text.Text(self.program, self.font)
        self.textScroll = 0
        self.meshes = []

        self.ortho = glmath.orthographic(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        self.program.set_uniform_matrix(self.orthoID, self.ortho)

        with open("./game/gametestmanager.py", "r") as myfile:
            self.data=myfile.read()

        glerr = gl.glGetError()
        if glerr != 0:
            print('GLError:', glerr)

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)
        self.ortho = glmath.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.program.set_uniform_matrix(self.orthoID, self.ortho)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'window_resized':
            winID, x, y = data
            self.resize(x, y)
        elif event == 'mouse_move':
            x, y = data
        elif event == 'key_down':
            self.keys.append(data[0])
            print(self.keys)
        elif event == 'key_up':
            self.keys.remove(data[0])

    def update(self):
        if 'DOWN' in self.keys:
            self.textScroll -= 6
        elif 'UP' in self.keys:
            self.textScroll += 6


    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.text.draw_text(self.data, 0, 10 + self.textScroll)

    def exit(self):
        '''Commands to run before exit.'''
        self.font.delete()

    def do_run(self):
        ''' Process a single loop '''
        self.events.process()
        self.update()
        self.render()
        self.window.flip()
        self.fpsTimer.tick()
        if self.fpsTimer.fpsTime >= 2000:
            self.fpsEstimate = self.fpsTimer.get_fps()
            print("{:.2f} fps".format(self.fpsEstimate))

    def run(self):
        ''' Called from launcher doesnt exit until the game is quit '''
        self.running = True
        while self.running:
            self.do_run()
        self.exit()
