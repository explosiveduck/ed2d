
from PIL import Image

from cubix.core.pycompat import *
from cubix.core.opengl import gl, pgl

class Texture(object):
    ''' Texture manager'''
    # Just for clarity
    # This is basically a static variable
    # It will be for assigning each texture an internal id 
    # We could use glGenTextures however it has no guaratees on
    # the range that it provides. Which means on differant platforms
    # we could get differant results. Which we dont want for what we 
    # use the id for (calculating GL_TEXTUREi) This value propagates
    # down into the class instances also, even as it is changed. :D
    textureCount = 0
    def _set_id(self):
        # increment value in class base
        Texture.textureCount += 1
        self.id = self.textureCount

    def __init__(self, path, program):

        self.path = path
        self.program = program

        self._set_id()

        self.program.new_uniform(b'textureSampler')

        img = Image.open(self.path)

        # Verify that the image is in RGBA format
        if ''.join(img.getbands()) != 'RGBA':
            img = img.convert('RGBA')

        # Get image data as a list
        self.data = list(img.getdata())

        self.width, self.height = img.size

        # Load image into new opengl texture
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        pgl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height,
                         0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.data)

    def bind(self):
        gl.glActiveTexture(gl.GL_TEXTURE0 + (self.id - 1))
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.id)
        self.program.set_uniform(b'textureSampler', (self.id - 1))
