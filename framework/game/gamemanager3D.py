from ed2d import window
from ed2d import sysevents
from ed2d.events import Events
from ed2d import context
from ed2d import timing
from ed2d import files
from ed2d import shaders
from ed2d.opengl import gl
from ed2d.opengl import pgl
from gem import vector
from gem import matrix
from ed2d import mesh
from ed2d import text
from ed2d import camera
from ed2d.scenegraph import SceneGraph
from ed2d.assets import objloader
from ed2d import cursor

class GameManager(object):
    ''' Entry point into the game, and manages the game in general '''
    def __init__(self):

        self.width = 800
        self.height = 600
        self.title = "ed2d"
        self.running = False

        self.fpsTimer = timing.FpsCounter()
        self.fpsEstimate = 0

        self.sysEvents = sysevents.SystemEvents()
        self.window = window.Window(self.title, self.width, self.height, window.WindowedMode)
        self.context = context.Context(3, 3, 2)
        self.context.window = self.window

        Events.add_listener(self.process_event)

        self.keys = []

        # Mouse Information
        self.mousePos = [0.0, 0.0]
        self.mouseButtons = []
        self.oldMouseX = 0
        self.oldMouseY = 0
        self.mousePosX = 0
        self.mousePosY = 0
        cursor.set_relative_mode(False)
        cursor.show_cursor()

        gl.init()
        major = pgl.glGetInteger(gl.GL_MAJOR_VERSION)
        minor = pgl.glGetInteger(gl.GL_MINOR_VERSION)
        print('OpenGL Version: {}.{}'.format(major, minor))

        gl.glViewport(0, 0, self.width, self.height)

        # For CSG to work properly
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_MULTISAMPLE)

        gl.glClearColor(0.0, 0.0, 0.4, 0.0)

        vsPath = files.resolve_path('data', 'shaders', 'main2.vs')
        fsPath = files.resolve_path('data', 'shaders', 'main2.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)
        self.program = shaders.ShaderProgram(vertex, fragment)
        self.program.use()

        #self.testID1 = self.program.new_uniform(b'perp')
        self.testID2 = self.program.new_uniform(b'view')

        self.vao = pgl.glGenVertexArrays(1)

        self.scenegraph = SceneGraph()

        # Creating a object steps:
        # Create a mesh object to render
        objFL = objloader.OBJ('buildings')
        self.meshTest = mesh.Mesh()
        self.meshTest.fromData(objFL)
        self.meshTest.addProgram(self.program)
        self.meshTestID = self.scenegraph.establish(self.meshTest)
        self.meshTest.translate(0.0, 0.0, 0.0)

        self.camera = camera.Camera()
        self.camera.orthographicProjection(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.camera.perspectiveProjection(75.0, float(self.width) / float(self.height), 0.1, 10000.0)
        self.camera.setPosition(vector.Vector(3, data=[0.5, -2.0, 10.0]))
        self.camera.set_program(2, self.program)
        self.model = matrix.Matrix(4)
        #self.model = matrix.Matrix(4).translate(vector.Vector(3, data=[4.0, -2.0, -8]))
        self.loadText()

        glerr = gl.glGetError()
        if glerr != 0:
            print('GLError:', glerr)

    def loadText(self):
        vsPath = files.resolve_path('data', 'shaders', 'font.vs')
        fsPath = files.resolve_path('data', 'shaders', 'font.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)
        self.textProgram = shaders.ShaderProgram(vertex, fragment)

        fontPath = files.resolve_path('data', 'SourceCodePro-Regular.ttf')
        self.font = text.Font(12, fontPath)
        self.text = text.Text(self.textProgram, self.font)

        self.camera.set_program(1, self.textProgram)

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)
        self.camera.perspectiveProjection(75.0, float(self.width) / float(self.height), 0.1, 10000.0)
        self.camera.orthographicProjection(0.0, self.width, self.height, 0.0, -1.0, 1.0)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'window_resized':
            winID, x, y = data
            self.resize(x, y)
        elif event == 'mouse_move':
            if cursor.is_relative():
                xrel, yrel = data
                self.mousePosX += xrel
                self.mousePosY += yrel
            else:
                self.mousePosX, self.mousePosY = data
        elif event == 'key_down':
            if data[0] == 'c':
                cursor.set_relative_mode(True)
            elif data[0] == 'r':
                cursor.set_relative_mode(False)
            self.keys.append(data[0])
            print(self.keys)
        elif event == 'key_up':
            self.keys.remove(data[0])
        elif event == 'mouse_button_down':
            self.mouseButtons.append(data[0])
            print(self.mouseButtons)
        elif event == 'mouse_button_up':
            self.mouseButtons.remove(data[0])

    def keyUpdate(self):
        self.camera.onKeys(self.keys, self.fpsTimer.tickDelta)

    def mouseUpdate(self):
        if cursor.is_relative():
            if 1 in self.mouseButtons:
                self.camera.onMouseMove(self.oldMouseX - self.mousePosX, self.oldMouseY - self.mousePosY, self.fpsTimer.tickDelta)

        self.oldMouseX = self.mousePosX
        self.oldMouseY = self.mousePosY

    def update(self):
        self.scenegraph.update()

    def render(self):
        gl.glClearColor(0.3, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Change view to perspective projection
        gl.glDisable(gl.GL_BLEND)

        self.program.use()
        self.camera.set_mode(2)
        view = self.camera.getViewMatrix()
        self.program.set_uniform_matrix(self.testID2, view)

        # Draw 3D stuff
        gl.glBindVertexArray(self.vao)

        self.scenegraph.render()

        gl.glBindVertexArray(0)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Change to orthographic projection to draw the text
        self.textProgram.use()
        self.camera.set_mode(1)
        self.text.draw_text(str(self.fpsEstimate) + ' FPS', 0, 10)

        gl.glDisable(gl.GL_BLEND)


    def do_run(self):
        ''' Process a single loop '''
        self.sysEvents.process()
        self.mouseUpdate()
        self.keyUpdate()
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
