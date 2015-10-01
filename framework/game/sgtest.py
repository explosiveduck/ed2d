from ed2d import window
from ed2d import context
from ed2d import events
from ed2d import timing
from ed2d.opengl import gl
from ed2d import scenegraph

class GameManager(object):
    def __init__(self):

        self.width = 800
        self.height = 600
        self.fullscreen = False
        self.title = "SceneGraph"
        self.running = False

        self.fpsTimer = timing.FpsCounter()
        self.fpsEstimate = 0

        self.window = window.Window(self.title, self.width,
                self.height, window.WindowedMode)

        self.events = events.Events()
        self.context = context.Context(3, 3, 2)
        self.context.window = self.window
        self.events.add_listener(self.process_event)

        gl.init()
        self.gl_init()

    def gl_init(self):
        '''Init opengl-using objects.'''
        print('MOO')
        self.sg = scenegraph.SceneGraph()
        listNode = self.sg.establish([])
        print(listNode)
        stringNode = self.sg.establish('')
        self.sg.establish({}, parent=stringNode)

        print(self.sg.root.treeChildren)

    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, self.width, self.height)

    def process_event(self, event, data):
        if event == 'quit' or event == 'window_close':
            self.running = False
        elif event == 'resize':
            winID, x, y = data
            self.resize(x, y)

    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.sg.render()

    def update(self):
        pass

    def exit(self):
        pass

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
