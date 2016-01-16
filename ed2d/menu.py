from ed2d.scenegraph import SceneGraph
from ed2d.mesh import Mesh
from ed2d import view
from ed2d import files
from ed2d import shaders
from gem import matrix
from ed2d.texture import Texture
from ed2d.events import Events
from ed2d.opengl import pgl, gl

class ElementManager(object):
    def __init__(self):
        self.scenegraph = SceneGraph()

        self.elementData = {}
        self.width = 800.0
        self.height = 600.0
        Events.add_listener(self.size_listener)

        self.init_gl()

    def init_gl(self):

        self.vao = pgl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vsPath = files.resolve_path('data', 'shaders', 'main.vs')
        fsPath = files.resolve_path('data', 'shaders', 'main.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)
        self.program = shaders.ShaderProgram(vertex, fragment)


        # A view instance will be used to sync all of the orthographic
        # projections in the various shaders the ui uses.

        # Technically we could use a view instance from the game instead
        # of creating a new one, but that makes things a bit more
        # complex to setup...

        self.view = view.View()
        self.ortho = matrix.orthographic(0.0, self.width, self.height, 0.0, -1.0, 1.0)
        self.view.new_projection('ortho', self.ortho)
        self.view.register_shader('ortho', self.program)

    def size_listener(self, event, data):
        if event == 'window_resized':
            print ('SIZE RECIEVED')
            winID, x, y = data
            self.width = x
            self.height = y
            self.ortho = matrix.orthographic(0.0, self.width, self.height, 0.0, -1.0, 1.0)
            self.view.set_projection('ortho', self.ortho)

    def create_element(self, elmProp):

        imgMesh = Mesh()
        imgMesh.fromData(data=[[0.0, 1.0], [1.0, 1.0], [0.0, 0.0], [1.0, 0.0]])

        for key, value in elmProp.items():
            if key == 'pos':
                x, y = value
                imgMesh.translate(x,y)
            elif key == 'scale':
                imgMesh.scale(value)
            elif key == 'rotation':
                # TODO - not yet implemented in mesh
                # imgMesh.rotate(*value)
                pass
            elif key == 'texture':
                imgMesh.addTexture(value)

        imgMesh.addProgram(self.program)

        eid = self.scenegraph.establish(imgMesh)

        self.elementData[eid] = {}
        self.elementData[eid]['prop'] = elmProp
        self.elementData[eid]['mesh'] = imgMesh

        return eid

    def update_element(self, eid, elmProp):
        imgMesh = self.elementData[eid]['mesh']

        for key, value in elmProp.items():
            self.elementData[eid]['prop'][key] = value
            if key == 'texture':
                imgMesh.addTexture(elmProp['texture'])

    def check_element(self, elmProp):
        '''Check if an object is already managed by the '''
        for eid, info in self.elementData.items():
            if info['prop'] is elmProp:
                return eid

    def render(self):
        self.program.use()
        gl.glBindVertexArray(self.vao)
        self.scenegraph.render()
        gl.glBindVertexArray(0)

_eleman = None

class Tex2D(object):
    def __init__(self, eid, elmProp):
        self.eid = eid
        self.elmProp = elmProp

    def update_scale(self, scale):
        elmProp = {'scale': scale}

        _eleman.update_element(elmProp)

    # TODO - This also should support relative positioning to the previous.
    def update_position(self, x, y):
        elmProp = {'pos': (x, y)}

        _eleman.update_element(elmProp)

    def update_texture(self, texture):
        elmProp = {'texture': texture}

        _eleman.update_element(elmProp)

    def update_rotation(self, rotation):
        elmProp = {'rotation': rotation}

        _eleman.update_element(elmProp)

def init_menusystem():
    global _eleman
    _eleman = ElementManager()

# These functions are wrapper function to help simplify the usage of
# ElementManager, which is basically going to be used like a singleton.
def insert_image(imgPath, x, y, scale=1, rotation=(0, 0, 0)):

    gl.glBindVertexArray(_eleman.vao)
    texture = Texture(imgPath, _eleman.program)
    elmProp = {
        'texture': texture,
        'pos': (x, y),
        'scale': scale,
        'rotation': rotation,
    }
    eid = _eleman.create_element(elmProp)
    gl.glBindVertexArray(0)
    return Tex2D(eid, elmProp)

def insert_text(text, font, x, y, scale=1, rotation=(0, 0, 0)):
    elmProp = {
        'font': font,
        'text': text,
        'pos': (x, y),
        'scale': scale,
        'rotation': rotation,
    }
    eid = _eleman.create_element(elmProp)

def render():
    _eleman.render()
