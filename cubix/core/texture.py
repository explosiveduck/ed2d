
from collections import OrderedDict

from PIL import Image
import sdl2 as sdl

from cubix.core.pycompat import *
from cubix.core.opengl import gl, pgl

class BaseTexture(object):
    ''' Texture manager'''
    # Just for clarity
    # This is basically a static variable
    # It will be for assigning each texture unit id easily.
    # We use the id for calculating GL_TEXTUREi. This value propagates
    # down into the class instances also, even as it is changed. :D
    textureCount = 0
    def _set_unit_id(self):
        self.texUnitID = self.textureCount
        Texture.textureCount += 1

    def load_gl(self):

        self.program.new_uniform(b'textureSampler')

        # Load image into new opengl texture
        self.texID = pgl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texID)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        pgl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height,
                         0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.data)

    def bind(self):
        gl.glActiveTexture(gl.GL_TEXTURE0 + self.texUnitID)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texID)
        self.program.set_uniform(b'textureSampler', self.texUnitID)

class Texture(BaseTexture):

    def __init__(self, path, program, type=''):

        self.path = path
        self.program = program

        self._set_unit_id()

        self.load_image()
        self.load_gl()


    def load_image(self):
        img = Image.open(self.path)

        # Verify that the image is in RGBA format
        if ''.join(img.getbands()) != 'RGBA':
            img = img.convert('RGBA')

        # Get image data as a list
        self.data = list(img.getdata())

        self.width, self.height = img.size

class TextureAtlas(BaseTexture):
    def __init__(self, program):

        self.program = program

        self._set_unit_id()

        # Data format will be as follows:
        #    Indexed by textureID
        #    value:
        #        - a second dict with information about that texture
        #            - x, y position in texture, width and height, texture data/uvcoords
        self.textures = []
        self.data = 0

    def add_texture(self, width, height, texData):
        textureID = len(self.textures)

        self.textures.append({
                'xpos':None, 'ypos':None,       # Calculated by calc_image
                'width': width, 'height': height,
                'texData': textData, 'uvCoords': None, # uvCords Calculated by calc_image
        })
        return textureID

    def get_uvcoords():
        cordData = []
        # This will return a list of all of the uvcoords indexed by textureID

        return coordData


    def calc_image(self):
        self.width = 0
        self.height = 0

        # For loop to go through all registered textures
        # and calculate the total image size for the atlas
        # for i in range():


    def gen_atlas(self):

        self.calc_image()
        self.load_gl()

        # add data to blank gl texture with
        # glTexSubImage2D here