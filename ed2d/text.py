import ctypes as ct

import freetype.raw as ft

from ed2d import texture
from ed2d import mesh
from ed2d import typeutils
from ed2d.opengl import gl, pgl
# from ed2d import glmath as cyglmath
from ed2d.glmath import cython as cyglmath


# Hack to verify that freetype is properly destructed after everything
# this code was also commited to freetype-py
class _FT_Library_Wrapper(ft.FT_Library):
    '''Subclass of FT_Library to help with calling FT_Done_FreeType'''
    # for some reason this doesn't get carried over and ctypes complains
    _type_ = ft.FT_Library._type_

    # Store ref to FT_Done_FreeType otherwise it will be deleted before needed.
    _ft_done_freetype = ft.FT_Done_FreeType

    def __del__(self):
        # call FT_Done_FreeType
        self._ft_done_freetype(self)


def init_freetype():
    handle = _FT_Library_Wrapper()

    if ft.FT_Init_FreeType(ct.byref(handle)):
        raise Exception('FreeType failed to initialize.')

    return handle


freetype = init_freetype()

# These are the usable fields of FT_GlyphSlotRec
#   field:            data type:
# library           FT_Library
# face              FT_Face
# next              FT_GlyphSlot
# generic           FT_Generic
# metrics           FT_Glyph_Metrics
# linearHoriAdvance FT_Fixed
# linearVertAdvance FT_Fixed
# advance           FT_Vector
# format            FT_Glyph_Format
# bitmap            FT_Bitmap
# bitmap_left       FT_Int
# bitmap_top        FT_Int
# outline           FT_Outline
# num_subglyphs     FT_UInt
# subglyphs         FT_SubGlyph
# control_data      void*
# control_len       long
# lsb_delta         FT_Pos
# rsb_delta         FT_Pos


class Font(object):
    def __init__(self, size, fontPath):

        self.size = size
        self.path = fontPath

        self.face = ft.FT_Face()

        # here is the general structure of the char data dict.
        #
        # It has
        self.charDataCache = {}

        # load font face
        if ft.FT_New_Face(freetype, typeutils.to_c_str(fontPath), 0,
                          ct.byref(self.face)):
            raise Exception('Error loading font.')

        # For now the device dpi will be hard coded to 72
        # later on if we want to do mobile stuff, or have dpi scaling
        # for high-dpi monitors this will need to be changed.
        if ft.FT_Set_Char_Size(self.face, 0, size * 64, 72, 72):
            raise Exception('Error setting character size.')

    def load_glyph(self, char):
        '''
        Loads glyph, and returns a dictionary containing glyph data.
        '''
        try:
            return self.charDataCache[char]

        except KeyError:
            index = ft.FT_Get_Char_Index(self.face, ord(char))

            if ft.FT_Load_Glyph(self.face, index, ft.FT_LOAD_RENDER):
                raise Exception('Error loading glyph')

            glyphSlot = self.face.contents.glyph

            charData = {}
            bitmapStruct = glyphSlot.contents.bitmap
            texWidth = bitmapStruct.width
            texHeight = bitmapStruct.rows

            pixelData = [0.0 for x in range(texWidth * texHeight)]

            for item in range(texWidth * texHeight):
                pixelData[item] = bitmapStruct.buffer[item]

            if not pixelData:
                pixelData = [0]

            charData['pixelData'] = pixelData
            charData['bitmap_x'] = glyphSlot.contents.bitmap_left
            charData['bitmap_y'] = glyphSlot.contents.bitmap_top
            charData['texWidth'] = texWidth
            charData['texHeight'] = texHeight
            charData['advance'] = glyphSlot.contents.advance.x >> 6

            self.charDataCache[char] = charData

            return charData

    def delete(self):
        '''Delete the freetype face'''
        ft.FT_Done_Face(self.face)


class Text(object):
    def __init__(self, program, font):
        self.program = program
        self.texAtlas = texture.TextureAtlas(self.program, texFormat=gl.GL_RED)

        self.font = font

        self.vertLoc = self.program.get_attribute(b'position')
        self.UVLoc = self.program.get_attribute(b'vertexUV')

        self.data = [[0.0, 1.0], [1.0, 1.0], [0.0, 0.0], [1.0, 0.0], ]

        self.chrMap = {}

        self.basePos = 0.0
        self.lineSpacing = 3

        for texVal in range(32, 128):
            char = chr(texVal)
            fontData = self.font.load_glyph(char)

            # Find the fartherst position from the baseline
            if fontData['bitmap_y'] > self.basePos:
                self.basePos = fontData['bitmap_y']

            self.chrMap[char] = Glyph(self.program, self.texAtlas, fontData,
                                      char, self)
        print(self.basePos)


        self.texAtlas.gen_atlas()

        self.vbo = mesh.buffer_object(self.data, gl.GLfloat)

        for glyph in self.chrMap.values():
            glyph.init_gl()


    def draw_text(self, text, xPos, yPos):

        self.texAtlas.bind()

        # When you can dynamically add textures to an Atlas
        # this is where the glyph objects will be created.
        # Instead of taking a while on init to generate all
        # normal characters.


        textLines = text.split('\n')

        penPosX = xPos
        penPosY = self.basePos + yPos
        for txt in textLines:
            for c in txt:
                char = self.chrMap[c]
                char.render(penPosX, penPosY)
                penPosX += char.advance
            penPosY += self.basePos + self.lineSpacing
            penPosX = xPos

        # gl.glDisableVertexAttribArray(self.UVLoc)

        # gl.glDisableVertexAttribArray(self.vertLoc)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)


class Glyph(object):
    def __init__(self, program, atlas, fontData, char, parent):
        self.atlas = atlas
        self.fontData = fontData
        self.program = program
        self.parent = parent
        self.nverts = 4

        self.vertLoc = self.program.get_attribute(b'position')
        self.modelLoc = self.program.new_uniform(b'model')
        self.UVLoc = self.program.get_attribute(b'vertexUV')

        self.modelMatrix = cyglmath.Matrix(4)

        self.char = char

        self.pixelData = self.fontData['pixelData']

        self.textureWidth = self.fontData['texWidth']
        self.textureHeight = self.fontData['texHeight']

        self.bitX = self.fontData['bitmap_x']
        self.bitY = self.fontData['bitmap_y']

        self.advance = self.fontData['advance']
        self.uniform = self.program.get_uniform(self.modelLoc)

        self.textureID = self.atlas.add_texture(self.textureWidth,
                                                self.textureHeight,
                                                self.pixelData)

    def init_gl(self):
        self.vao = pgl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self._uvCoords = self.atlas.get_uvcoords(self.textureID)
        self.vertexScale = self.atlas.get_vertex_scale(self.textureID)

        vecScale = cyglmath.Vector(
            3,
            data=[self.atlas.maxSubTextureHeight * self.vertexScale[0],
                  self.atlas.maxSubTextureHeight * self.vertexScale[1], 0.0])

        self.scaleMat = cyglmath.Matrix(4).i_scale(vecScale)

        self.uvbo = mesh.buffer_object(self._uvCoords, gl.GLfloat)

        gl.glEnableVertexAttribArray(self.vertLoc)
        gl.glEnableVertexAttribArray(self.UVLoc)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.parent.vbo)
        pgl.glVertexAttribPointer(self.vertLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.uvbo)
        pgl.glVertexAttribPointer(self.UVLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        gl.glBindVertexArray(0)

    def render(self, posX, posY):
        gl.glBindVertexArray(self.vao)

        vecScale = cyglmath.Vector(
            3,
            data=[posX + self.bitX, posY - self.bitY, 0.0])
        self.modelMatrix = self.scaleMat.translate(vecScale)

        self.program.set_uniform_matrix(self.modelLoc, self.modelMatrix,
                                        uniform=self.uniform,
                                        size=4)


        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.nverts)
