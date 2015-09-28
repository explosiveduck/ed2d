import random as rnd
from ed2d import window
from ed2d import events
from ed2d import context
from ed2d import timing
from ed2d import files
from ed2d import shaders
from ed2d.opengl import gl
from ed2d.opengl import pgl
from ed2d import typeutils
from ed2d import glmath
from ed2d import texture
from ed2d import mesh
from ed2d.physics import rectangle
from ed2d.physics import cmodel
from ed2d.physics import physobj
from ed2d.physics import physengine

class GameManager(object):
    ''' Entry point into the game, and manages the game in general '''
    def __init__(self):

        self.width = 800
        self.height = 600
        self.title = "Edge Engine - Texture Filtering Demo"
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
        print ('OpenGL Version: {}.{}'.format(major, minor))

        gl.glViewport(0, 0, self.width, self.height)

        # Shaders setup
        vsPath = files.resolve_path('data', 'shaders', 'main.vs')
        fsPath = files.resolve_path('data', 'shaders', 'texturefiltering.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)
        self.program = shaders.ShaderProgram(vertex, fragment)
        self.program.use()
        self.orthoID = self.program.new_uniform(b'ortho')
        self.viewPortID = self.program.new_uniform(b'viewPortResolution')

        self.vao = pgl.glGenVertexArrays(1)

        # Load character image into new opengl texture
        imagePath = files.resolve_path('data', 'images', 'cubix.png')
        self.texAtlas = texture.Texture(imagePath, self.program)

        '''Physics Scene'''
        # Create a physics engine
        self.physicsEngineTest = physengine.PhysEngine()

        '''Player physical model'''
        # Create a rectangle the long way, this will be the player
        self.cModelTestRect = rectangle.Rectangle(0.0, 0.0, width=800, height=600)
        self.cModelTestRect.update()

        # Creating a object steps:
        # Create a collision model object
        # Create a physics object to simulate
        # Create a mesh object to render
        self.cModelTest = cmodel.cModel(self.cModelTestRect)
        self.physicsObjectTest = physobj.PhysObj(self.cModelTest, glmath.Vector(3, data=[0.0, 0.0, 1.0]))
        self.physicsEngineTest.addObject(self.physicsObjectTest)
        self.meshObjectTest = mesh.Mesh()

        self.meshObjectTest.fromData(data=[
             [0.0, 1.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0]])

        self.meshObjectTest.setBuffers()
        self.meshObjectTest.addProgram(self.program)
        self.meshObjectTest.addTexture(self.texAtlas)
        self.meshObjectTest.addPhysicsObject(self.physicsObjectTest)
        '''End Player'''

        # Setup projection
        self.ortho = glmath.orthographic(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        # Update the uniforms in the shaders
        self.program.set_uniform_matrix(self.orthoID, self.ortho)
        self.program.set_uniform_array(self.viewPortID, [float(self.width), float(self.height)])

        glerr = gl.glGetError()
        if glerr != 0:
            print ('GLError:', glerr)

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)
        self.ortho = glmath.orthographic(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.program.set_uniform_matrix(self.orthoID, self.ortho)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'window_resized':
            winID, x, y = data
            self.resize(x, y)
        elif event == 'mouse_move':
            x, y = data
            # Translate and then update it, this can be handled better but for now, this will do
            #self.physicsObjectTest.translate(x,y)
            #self.meshObjectTest.update(self.physicsObjectTest)
        elif event == 'key_down':
            self.keys.append(data[0])
            print (self.keys)
        elif event == 'key_up':
            self.keys.remove(data[0])

    def update(self):
        pass
        #Disabled because it can get really annoying, really fast >:[
        #self.physicsEngineTest.simulate(self.fpsTimer.tick())

    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBindVertexArray(self.vao)

        self.meshObjectTest.render()

        gl.glBindVertexArray(0)

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
