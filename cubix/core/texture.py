
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

class Texture(baseTexture):

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
