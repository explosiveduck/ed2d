
from collections import OrderedDict

from PIL import Image
import sdl2 as sdl

from cubix.core.pycompat import *
from cubix.core.opengl import gl, pgl

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

    def __init__(self, path, program, type=''):

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

    def add_texture(self, width, height, texData):
        textureID = len(self.textures)

        self.textures.append({
                'x1':0, 'x2':0, 'y1':0, 'y2':0,      # Calculated by calc_image
                'width': width, 'height': height,
                'texData': texData, 'uvCoords': None,
        })
        return textureID

    def get_uvcoords(self):
        coordData = []
        # This will return a list of all of the uvcoords indexed by textureID
        for tex in self.textures:
            x1 = tex['x1'] / float(self.width)
            x2 = tex['x2'] / float(self.width)
            y1 = tex['y1'] / float(self.height)
            y2 = tex['y2'] / float(self.height)
            coordData.append((x1, x2, y1, y2))

        return coordData

    def get_coords(self):
        coordData = []
        # This will return a list of all of the coord data indexed by textureID
        for tex in self.textures:
            x1 = tex['x1']
            x2 = tex['x2']
            y1 = tex['y1']
            y2 = tex['y2']

            coordData.append((x1, x2, y1, y2)) 

        return coordData

    def get_vertex_scale(self):
        ''' Returns calculated vertex scaleing for textures by textureID '''
        coordData = []
        # This will return a list of all of the coord data indexed by textureID

        vertScale = []

        # This assumes that your vertex coords are:
        #[0,1]
        #[1,1]
        #[0,0]
        #[1,0]

        for tex in self.textures:
            imgWidth = tex['width']
            imgHeight = tex['height']

            vertScaleX = imgHeight / float(self.maxSubTextureHeight)
            vertScaleY = imgWidth / float(self.maxSubTextureHeight)

            vertScale.append([vertScaleX, vertScaleY])

        return coordData

    def calc_image(self):

        # Go through all registered textures and calculate the total
        # image size for the atlas plus the coords for image location.

        self.width = 0
        self.height = 0
        cursorPosY = 0
        cursorPosX = 0
        lineHeight = 0
        self.maxSubTextureHeight = 0

        for tex in self.textures:
            imgWidth = tex['width']
            imgHeight = tex['height']

            if cursorPosX + imgWidth  + 1 >= self.maxWidth:

                self.width = max(self.width, cursorPosX)
                cursorPosY += lineHeight

                self.maxSubTextureHeight = max(self.maxSubTextureHeight, lineHeight - 1)

                lineHeight = 0
                cursorPosX = 0

            tex['x1'] = cursorPosX
            tex['x2'] = cursorPosX + imgWidth
            tex['y1'] = cursorPosY
            tex['y2'] = cursorPosY + imgHeight

            cursorPosX += imgWidth + 1
            lineHeight = max(lineHeight, imgHeight + 1)

        cursorPosY += lineHeight
        self.width = max(self.width, cursorPosX)
        self.height = cursorPosY

        self.maxSubTextureHeight = max(self.maxSubTextureHeight, lineHeight - 1)

    def gen_atlas(self):

        self.calc_image()
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
