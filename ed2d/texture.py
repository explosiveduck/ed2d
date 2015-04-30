
from collections import OrderedDict

from PIL import Image
import sdl2 as sdl

from ed2d.pycompat import *
from ed2d.opengl import gl, pgl

def load_image(path):
    img = Image.open(path)

    # Verify that the image is in RGBA format
    if ''.join(img.getbands()) != 'RGBA':
        img = img.convert('RGBA')

    # Get image data as a list
    data = list(img.getdata())

    width, height = img.size
    return width, height, data

class BaseTexture(object):
    ''' Texture manager'''
    # Just for clarity
    # This is basically a static variable
    # It will be for assigning each texture unit id easily.
    # We use the id for calculating GL_TEXTUREi. This value propagates
    # down into the class instances also, even as it is changed. :D
    #
    # edit: decide if this would be better off as an __init__ method that
    # the subclasses call via super. Would be the best thing if we want to
    # have external subclasses of the BaseTexture.

    _textureCount = 0
    def _set_unit_id(self):
        self.texUnitID = self._textureCount
        BaseTexture._textureCount += 1

    def load_gl(self):

        self.texSampID = self.program.new_uniform(b'textureSampler')

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
        self.program.set_uniform(self.texSampID, self.texUnitID)

class Texture(BaseTexture):

    def __init__(self, path, program):

        self.path = path
        self.program = program

        self._set_unit_id()

        self.width, self.height, self.data = load_image(self.path)
        self.load_gl()

class TextureAtlas(BaseTexture):
    def __init__(self, program, maxWidth=1024):

        self.program = program

        self._set_unit_id()

        # Data format will be as follows:
        #    Indexed by textureID
        #    value:
        #        - a second dict with information about that texture
        #            - x, y position in texture, width and height, texture data/uvcoords
        self.textures = []
        self.data = 0
        self.maxWidth = maxWidth

        self.width = 0
        self.height = 0
        self.cursorPosY = 0
        self.cursorPosX = 0
        self.lineHeight = 0
        self.maxSubTextureHeight = 0

    def add_texture(self, width, height, texData):
        textureID = len(self.textures)

        imgWidth = width
        imgHeight = height

        if self.cursorPosX + imgWidth  + 1 >= self.maxWidth:

            self.width = max(self.width, self.cursorPosX)
            self.cursorPosY += self.lineHeight

            self.maxSubTextureHeight = max(self.maxSubTextureHeight, self.lineHeight - 1)

            self.lineHeight = 0
            self.cursorPosX = 0

        x1 = self.cursorPosX
        x2 = self.cursorPosX + imgWidth
        y1 = self.cursorPosY
        y2 = self.cursorPosY + imgHeight

        self.cursorPosX += imgWidth + 1
        self.lineHeight = max(self.lineHeight, imgHeight + 1)

        self.textures.append({
                'x1':x1, 'x2':x2, 'y1':y1, 'y2':y2,
                'width': width, 'height': height,
                'texData': texData, 'uvCoords': None,
        })
        return textureID

    def get_uvcoords(self, texID):

        tex = self.textures[texID]

        x1 = tex['x1'] / float(self.width)
        x2 = tex['x2'] / float(self.width)
        y1 = tex['y1'] / float(self.height)
        y2 = tex['y2'] / float(self.height)

        coord = [[x1, y2],
                 [x2, y2],
                 [x1, y1],
                 [x2, y1]]

        return coord

    def get_vertex_scale(self, texID):
        '''
        Returns calculated vertex scaleing for textures by textureID
        This nomalizes all subtextures to the height of the tallest texture.
        This is done because the vertex data sent to the gpu is the same for
        each 
        '''

        tex = self.textures[texID]

        imgWidth = tex['width']
        imgHeight = tex['height']

        vertScaleY = imgHeight / float(self.maxSubTextureHeight)
        vertScaleX = imgWidth / float(self.maxSubTextureHeight)

        return (vertScaleX, vertScaleY)

    def gen_atlas(self):

        self.cursorPosY += self.lineHeight

        self.width = max(self.width, self.cursorPosX)
        self.height = self.cursorPosY

        self.maxSubTextureHeight = max(self.maxSubTextureHeight, self.lineHeight - 1)

        self.load_gl()

        # add data to blank gl texture with
        # glTexSubImage2D here
        for tex in self.textures:
            x1 = tex['x1']
            y1 = tex['y1']
            width = tex['width']
            height = tex['height']
            texData = tex['texData']

            pgl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, x1, y1, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, texData)
