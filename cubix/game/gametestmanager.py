import random as rnd
from cubix.core.pycompat import *
from cubix.core import window
from cubix.core import events
from cubix.core import context
from cubix.core import timing
from cubix.core import files
from cubix.core import shaders
from cubix.core.opengl import gl
from cubix.core.opengl import pgl
from cubix.core.opengl import typeutils
from cubix.core import glmath
from cubix.core import texture
from cubix.core import mesh
from cubix.core import text

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

        self.keys = []

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
        self.orthoID = self.program.new_uniform(b'ortho')

        self.vao = pgl.glGenVertexArrays(1)

        # Load character image into new opengl texture
        imagePath = files.resolve_path('data', 'images', 'cubix.png')
        self.texAtlas = texture.Texture(imagePath, self.program)
        
        fontPath = files.resolve_path('data', 'squarishsans.ttf')
        self.font = text.Font(30, fontPath)
        self.text = text.Text(self.program, self.font)

        self.cubixTex = texture.Texture(imagePath, self.program)

        self.meshTest = mesh.Mesh(self.program, self.cubixTex)
        self.meshTest.scale(32)

        self.meshes = []
        
        rowx = 0
        rowy = 0
        numPerRow = int(self.width/37)
        for i in range(numPerRow * int(self.height/37)):
            self.meshes.append(mesh.Mesh(self.program, self.cubixTex))
            self.meshes[i].scale(32)
            if (rowy*32) + (rowy * 5) + 32 >= self.width:
                rowx += 1
                rowy = 0
            self.meshes[i].translate(rowy*32 + rowy * 5, rowx * 37)
            rowy += 1
        print (len(self.meshes))

        self.ortho = glmath.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        self.program.set_uniform_matrix(self.orthoID, self.ortho)
        
        glerr = gl.glGetError()
        if glerr != 0:
            print ('GLError:', glerr)

    def resize_obj(self):
        rowx = 0
        rowy = 0
        numPerRow = int(self.width/37)
        newMesh = []
        for i in range(numPerRow * int(self.height/37)):
            if i > len(self.meshes) - 1:
                newMesh.append(mesh.Mesh(self.program, self.cubixTex))
                newMesh[i].scale(32)
            else:
                newMesh.append(self.meshes[i])
            if (rowy*32) + (rowy * 5) + 32 >= self.width:
                rowx += 1
                rowy = 0
            newMesh[i].translate(rowy*32 + rowy * 5, rowx * 37)
            rowy += 1
        self.meshes = newMesh

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)
        self.ortho = glmath.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.program.set_uniform_matrix(self.orthoID, self.ortho)
        self.resize_obj()

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
            print (self.keys)
        elif event == 'key_up':
            self.keys.remove(data[0])

    def update(self):
        for obj in self.meshes:
            obj.update()

    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBindVertexArray(self.vao)

        #for obj in self.meshes:
         #   obj.render()

        self.text.draw_text('Hello World!, FPS: %.2f' % self.fpsEstimate)
        gl.glBindVertexArray(0)

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
            print ("{:.2f} fps".format(self.fpsEstimate))

    def run(self):
        ''' Called from launcher doesnt exit until the game is quit '''
        self.running = True
        while self.running:
            self.do_run()
        self.exit()
