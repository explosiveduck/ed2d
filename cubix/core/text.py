import ctypes as ct
import sdl2 as sdl
from sdl2 import sdlttf

from cubix.core import texture
from cubix.core import mesh
from cubix.core import shaders
from cubix.core import files
from cubix.core.opengl import typeutils 
from cubix.core.opengl import gl, pgl
from cubix.core import glmath

def init_text():
    sdlttf.TTF_Init()

class Text(object):
    def __init__(self, _program, size, fontPath):
        self._program = _program

        self.texAtlas = texture.TextureAtlas(self._program)
        self.fontFile = sdlttf.TTF_OpenFont(typeutils.to_c_str(fontPath) , size )

        self.vertLoc = self._program.get_attribute(b'position')

        self.data = [
             [0.0, 1.0],
             [1.0, 1.0],
             [0.0, 0.0],
             [1.0, 0.0],
        ]

        self.chrMap = {}

        for texVal in range(32, 128):
            self.chrMap[chr(texVal)] = Glyph(self.texAtlas, self.fontFile, self._program, texVal, size)
        self.texAtlas.gen_atlas()

        uvcoord = self.texAtlas.get_uvcoords()
        for i, uv in enumerate(uvcoord):
            x1, x2, y1, y2 = uv

            coord = [
                    [x1, y2],
                    [x2, y2],
                    [x1, y1],
                    [x2, y1],
            ]
            self.chrMap[chr(i+32)].uvCoords = coord

        self.vbo = mesh.buffer_object(self.data)

    def draw_text(self, text):

        self.texAtlas.bind()

        gl.glEnableVertexAttribArray(self.vertLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        pgl.glVertexAttribPointer(self.vertLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        for i, c in enumerate(text):
            self.chrMap[c].render(i)

        gl.glDisableVertexAttribArray(self.vertLoc)

        gl.glBindVertexArray(0)

class Glyph(object):
    def __init__(self, _atlas, _font, _program, glyphOrd, size):
        self._atlas = _atlas
        self._font = _font
        self._program = _program
        self._nverts = 4


        self.modelLoc = self._program.new_uniform(b'model')
        self.UVLoc = self._program.get_attribute(b'vertexUV')

        self.modelMatrix = glmath.Matrix(4)

        # Variables that will be used from this class elsewhere
        self.ord = glyphOrd
        self.textureID = None
        self.textureWidth = None
        self.textureHeight = None
        self.pixelData = None
        self._uvCoords = None

        # Color to render in we want white initialy
        color = sdl.SDL_Color()
        color.r = 255
        color.g = 255
        color.b = 255
        color.a = 255

        glyph = sdlttf.TTF_RenderGlyph_Blended(self._font, self.ord, color)

        self.textureWidth = glyph.contents.w
        self.textureHeight = glyph.contents.h

        dataType = (ct.c_ubyte * 4 * (self.textureWidth * self.textureHeight))
        pixObj = ct.cast(glyph.contents.pixels, ct.POINTER(dataType)).contents

        pixelData = [[0.0 for sub in range(4)] for x in range(self.textureWidth * self.textureHeight)]

        for item in range(self.textureWidth * self.textureHeight):
            pixelData[item] = list(pixObj[item])

        del pixObj
        sdl.SDL_FreeSurface(glyph)

        self.textureID = self._atlas.add_texture(self.textureWidth, self.textureHeight, pixelData)

    @property
    def uvCoords(self):
        return self._uvCoords
    @uvCoords.setter
    def uvCoords(self, value):
        self._uvCoords = value
        self.uvbo = mesh.buffer_object(self._uvCoords)
    
    def render(self, pos):
        self.modelMatrix = glmath.Matrix(4)
        vecScale = glmath.Vector(3, data=[30.0, 30.0, 0.0])
        self.modelMatrix.i_scale(vecScale)
        vecScale = glmath.Vector(3, data=[pos*32, 0.0, 0.0])
        self.modelMatrix.i_translate(vecScale)

        self._program.set_uniform_matrix(self.modelLoc, self.modelMatrix)

        gl.glEnableVertexAttribArray(self.UVLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.uvbo)
        pgl.glVertexAttribPointer(self.UVLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self._nverts)

        gl.glDisableVertexAttribArray(self.UVLoc)

