from PIL import Image

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
        self.UVLoc = self.program.get_attribute(b'vertexUV')
        self.program.new_uniform(b'ortho')
        self.program.new_uniform(b'model')
        self.program.new_uniform(b'textureSampler')

        self.vao = pgl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        # Load character image into new opengl texture
        imagePath = files.resolve_path('data', 'images', 'cubix.png')
        pilImage = Image.open(imagePath)

        # Verify that the image is in RGBA format
        if ''.join(pilImage.getbands()) != 'RGBA':
            pilImage = pilImage.convert('RGBA')

        # Get image data as a list
        self.cubixData = list(pilImage.getdata())
        self.cubixWidth, self.cubixHeight = pilImage.size

        # Create new texture
        self.texID = pgl.glGenTextures(1)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texID)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        pgl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.cubixWidth, self.cubixHeight, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.cubixData)

        self.data = [
             [0.0, 32.0],
             [32.0, 32.0],
             [0.0, 0.0],
             [32.0, 0.0],
        ]

        self.uvCoord =  [
             [0.0, 1.0],
             [1.0, 1.0],
             [0.0, 0.0],
             [1.0, 0.0],
        ]

        self.ortho = glmath.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.model = glmath.Matrix(4).i_translate(glmath.Vector(3, data=(100.0,100.0,0.0)))

        self.program.set_uniform(b'ortho', self.ortho)
        self.program.set_uniform(b'model', self.model)

        self.vbo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        pgl.glBufferData(gl.GL_ARRAY_BUFFER, self.data, gl.GL_STATIC_DRAW)

        self.uvbo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.uvbo)
        pgl.glBufferData(gl.GL_ARRAY_BUFFER, self.uvCoord, gl.GL_STATIC_DRAW)

        #self.uvCoord = [0.0, 0.0,  1.0, 0.0,  1.0, 1.0,  0.0, 1.0]

        glerr = gl.glGetError()
        if glerr != 0:
            print ('GLError:', glerr)

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)
        self.ortho = glmath.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.program.set_uniform(b'ortho', self.ortho)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'window_resized':
            winID, x, y = data
            self.resize(x, y)
        elif event == 'mouse_move':
            x, y = data
            self.model = glmath.Matrix(4).i_translate(glmath.Vector(3, data=(x,y,0.0)))
            self.program.set_uniform(b'model', self.model)


    def update(self):
        pass

    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texID)
        self.program.set_uniform(b'textureSampler', 0)

        gl.glEnableVertexAttribArray(self.vertLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        pgl.glVertexAttribPointer(self.vertLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        
        gl.glEnableVertexAttribArray(self.UVLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.uvbo)
        pgl.glVertexAttribPointer(self.UVLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
        #print ('test')

        gl.glDisableVertexAttribArray(self.UVLoc)
        gl.glDisableVertexAttribArray(self.vertLoc)

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