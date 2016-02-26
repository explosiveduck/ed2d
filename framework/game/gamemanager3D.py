import math

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
from ed2d import view

class Viewport(object):
    '''Basic data container to allow changing the viewport to simpler.'''
    def __init__(self, name, camera):
        self.name = name
        self.camera = camera
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.screenSize = None

    def set_rect(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def make_current(self):
        if self.camera:
            if self.camera.get_mode() == camera.MODE_PERSPECTIVE:
                self.camera.set_projection(75.0, float(self.width) / float(self.height), 1e-6, 1e27)
            else:
                self.camera.set_projection(0.0, self.width, self.height, 0.0, -1.0, 1.0)
            self.camera.make_current()

        gl.glViewport(self.x, self.screenSize[1]-self.y-self.height, self.width, self.height)

class ViewportManager(object):
    '''Viewport Manager is for handling multiple split views '''
    def __init__(self):
        self.view = view.View()
        self.viewports = []
        self.screenSize = (0, 0)
    
    def update_screen(self, width, height):
        self.screenSize = (width, height)
        for vp in self.viewports:
            vp.screenSize = self.screenSize

    def create_viewport(self, name, camera):
        camera.set_view(self.view)
        vp = Viewport(name, camera)
        vp.screenSize = self.screenSize
        self.viewports.append(vp)
        return vp

class GameManager(object):
    ''' Entry point into the game, and manages the game in general '''
    def __init__(self):

        self.width = 1920
        self.height = 1080
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
        self.mouseRelX = 0
        self.mouseRelY = 0
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


        objBox = objloader.OBJ('box')
        self.boxMesh = mesh.Mesh()
        self.boxMesh.fromData(objBox)
        self.boxMesh.addProgram(self.program)
        self.boxMesh.scale(0.25)
        self.boxMeshID = self.scenegraph.establish(self.boxMesh)


        self.loadText()

        self.vpManager = ViewportManager()
        self.vpManager.update_screen(self.width, self.height)

        self.cameraOrtho = camera.Camera(camera.MODE_ORTHOGRAPHIC)
        self.cameraOrtho.set_view(self.vpManager.view)
        self.cameraOrtho.set_program(self.textProgram)
        self.vpFull = Viewport('full', self.cameraOrtho)
        self.vpFull.screenSize = (self.width, self.height)
        
        for i in range(4):
            cam = camera.Camera(camera.MODE_PERSPECTIVE)
            vp = self.vpManager.create_viewport('sceneview{0}'.format(i), cam)

            cam.setPosition(vector.Vector(3, data=[0.5, -2.0, 10.0]))
            cam.set_program( self.program)

        halfWidth = int(self.width /2)
        halfHeight = int(self.height/2)
        
        vps = self.vpManager.viewports
        vps[0].set_rect(0,         0,          halfWidth, halfHeight)
        vps[1].set_rect(0,         halfHeight, halfWidth, halfHeight)
        vps[2].set_rect(halfWidth, halfHeight, halfWidth, halfHeight)
        vps[3].set_rect(halfWidth, 0,          halfWidth, halfHeight)
        self.camera = vps[0].camera

        self.vpFull.set_rect(0, 0, self.width, self.height)

        self.model = matrix.Matrix(4)
        #self.model = matrix.Matrix(4).translate(vector.Vector(3, data=[4.0, -2.0, -8]))


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

    def resize(self, width, height):
        self.width = width
        self.height = height
        
        self.vpManager.update_screen(self.width, self.height)
        self.vpFull.screenSize = (self.width, self.height)

        halfWidth = int(self.width /2)
        halfHeight = int(self.height/2)

        vps = self.vpManager.viewports
        vps[0].set_rect(0,         0,          halfWidth, halfHeight)
        vps[1].set_rect(halfWidth, 0,          halfWidth, halfHeight)
        vps[2].set_rect(halfWidth, halfHeight, halfWidth, halfHeight)
        vps[3].set_rect(0,         halfHeight, halfWidth, halfHeight)
        
        self.vpFull.set_rect(0, 0, self.width, self.height)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'window_resized':
            winID, x, y = data
            self.resize(x, y)
        elif event == 'mouse_move':
            if cursor.is_relative():
                self.mouseRelX, self.mouseRelY = data
            else:
                self.mousePosX, self.mousePosY = data
        elif event == 'key_down':
            if data[0] == 'c':
                cursor.set_relative_mode(True)
            elif data[0] == 'r':
                cursor.set_relative_mode(False)
                cursor.move_cursor(self.mousePosX, self.mousePosY)
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

        moveAmount = 0.5 * self.fpsTimer.tickDelta

        for key in self.keys:
            if key == 'w':
                self.camera.move(self.camera.vec_back, moveAmount)

            elif key == 's':
                self.camera.move(self.camera.vec_forward, moveAmount)

            elif key == 'a':
                self.camera.move(self.camera.vec_left, moveAmount)

            elif key == 'd':
                self.camera.move(self.camera.vec_right, moveAmount)

            elif key == 'q':
                self.camera.move(self.camera.vec_up, moveAmount)

            elif key == 'e':
                self.camera.move(self.camera.vec_down, moveAmount)

            elif key == 'UP':
                self.camera.rotate(self.camera.vec_right, moveAmount * 0.05)

            elif key == 'DOWN':
                self.camera.rotate(self.camera.vec_left, moveAmount * 0.05)

            elif key == 'LEFT':
                self.camera.rotate(self.camera.vec_up, moveAmount * 0.05)

            elif key == 'RIGHT':
                self.camera.rotate(self.camera.vec_down, moveAmount * 0.05)

    def mouseUpdate(self):
        
        if 1 in self.mouseButtons:
            if not cursor.is_relative():
                cursor.set_relative_mode(True)
            tick = self.fpsTimer.tickDelta
            sensitivity = 0.5
            if self.mouseRelX != 0:
                self.camera.rotate(self.camera.yAxis, math.radians(-self.mouseRelX * sensitivity * tick))

            if self.mouseRelY != 0:
                self.camera.rotate(self.camera.vec_right, math.radians(-self.mouseRelY * sensitivity * tick))

            self.mouseRelX, self.mouseRelY = 0, 0
        else:
            if cursor.is_relative():
                cursor.set_relative_mode(False)
                cursor.move_cursor(self.mousePosX, self.mousePosY)

    def update(self):
        posVec = self.camera.position.vector
        self.boxMesh.translate(posVec[0], posVec[1], posVec[2]-2.0)
        if not cursor.is_relative():
            for vp in self.vpManager.viewports:
                w = vp.width
                h = vp.height
                x = vp.x
                y = vp.y
                
                
                if (self.mousePosX >= x and self.mousePosX < x+w and
                    self.mousePosY >= y and self.mousePosY < y+h):
                    self.camera = vp.camera
                    break
                
            
        
        self.mouseUpdate()
        self.keyUpdate()

        self.scenegraph.update()

    def render(self):
        # We need this viewport clear the whole screen (I think) 
        self.vpFull.make_current()
        
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(0.3, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Change view to perspective projection
        gl.glDisable(gl.GL_BLEND)

        for vp in self.vpManager.viewports:

            vp.make_current()
            self.program.use()
            view = vp.camera.getViewMatrix()
            self.program.set_uniform_matrix(self.testID2, view)

            # Draw 3D stuff
            gl.glBindVertexArray(self.vao)

            self.scenegraph.render()

        gl.glBindVertexArray(0)

        gl.glEnable(gl.GL_BLEND)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Change to orthographic projection to draw the text
        self.vpFull.make_current()
        self.textProgram.use()
        self.cameraOrtho.make_current()
        self.text.draw_text(str(self.fpsEstimate) + ' FPS', 0, 10)

        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)


    def do_run(self):
        ''' Process a single loop '''
        self.sysEvents.process()
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
