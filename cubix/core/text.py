import ctypes as ct

import sdl2 as sdl
import freetype.raw as ft

from cubix.core import texture
from cubix.core import mesh
from cubix.core import shaders
from cubix.core import files
from cubix.core.opengl import typeutils 
from cubix.core.opengl import gl, pgl
from cubix.core import glmath

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
        if ft.FT_New_Face(freetype, typeutils.to_c_str(fontPath), 0, ct.byref(self.face)):
            raise Exception('Error loading font.')

        # For now the device dpi will be hard coded to 72
        # later on if we want to do mobile stuff, or have dpi scaling
        # for high-dpi monitors this will need to be changed.
        if ft.FT_Set_Char_Size(self.face, 0, size*64, 72, 72):
            raise Exception('Error setting character size.')

    def load_glyph(self, char):
        '''
        Loads glyph, and returns a dictionary containing glyph data.
        
        '''
        try:
            return self.charDataCache[char]

        except:
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
                pixelData[item] = [255, 255, 255, bitmapStruct.buffer[item]]

            if not pixelData:
                pixelData = [0]

            charData['pixelData'] = pixelData
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
        self.texAtlas = texture.TextureAtlas(self.program)

        self.font = font

        self.vertLoc = self.program.get_attribute(b'position')

        self.data = [
             [0.0, 1.0],
             [1.0, 1.0],
             [0.0, 0.0],
             [1.0, 0.0],
        ]

        self.chrMap = {}

        for texVal in range(32, 128):
            char = chr(texVal) 
            fontData = self.font.load_glyph(char)
            self.chrMap[char] = Glyph(self.program, self.texAtlas,
                    fontData, char)

        self.texAtlas.gen_atlas()

        for glyph in self.chrMap.values():
            glyph.init_gl()

        self.vbo = mesh.buffer_object(self.data)

    def draw_text(self, text):

        self.texAtlas.bind()

        # When you can dynamically add textures to an Atlas
        # this is where the glyph objects will be created.
        # Instead of taking a while on init to generate all
        # normal characters.

        gl.glEnableVertexAttribArray(self.vertLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        pgl.glVertexAttribPointer(self.vertLoc, 2, gl.GL_FLOAT,
                gl.GL_FALSE,0, None)

        penPosX = 0
        for i, c in enumerate(text):
            char = self.chrMap[c]
            char.render(penPosX)
            penPosX += char.advance

        gl.glDisableVertexAttribArray(self.vertLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)


class Glyph(object):
    def __init__(self, program, atlas, fontData, char):
        self.atlas = atlas
        self.fontData = fontData
        self.program = program
        self.nverts = 4

        self.modelLoc = self.program.new_uniform(b'model')
        self.UVLoc = self.program.get_attribute(b'vertexUV')

        self.modelMatrix = glmath.Matrix(4)

        self.char = char
        

        self.pixelData = self.fontData['pixelData']

        self.textureWidth = self.fontData['texWidth']
        self.textureHeight = self.fontData['texHeight']

        self.advance = self.fontData['advance']

        self.textureID = self.atlas.add_texture(self.textureWidth,
                self.textureHeight, self.pixelData)

    def init_gl(self):
        self._uvCoords = self.atlas.get_uvcoords(self.textureID)
        self.vertexScale = self.atlas.get_vertex_scale(self.textureID)

        self.uvbo = mesh.buffer_object(self._uvCoords)
    
    def render(self, pos):
        self.modelMatrix = glmath.Matrix(4)

        vecScale = glmath.Vector(3, data=[self.atlas.maxSubTextureHeight, self.atlas.maxSubTextureHeight, 0.0])
        self.modelMatrix.i_scale(vecScale)

        vecScale = glmath.Vector(3, data=[self.vertexScale[0], self.vertexScale[1], 0.0])
        self.modelMatrix.i_scale(vecScale)



        vecScale = glmath.Vector(3, data=[pos, 0.0, 0.0])
        self.modelMatrix.i_translate(vecScale)

        self.program.set_uniform_matrix(self.modelLoc, self.modelMatrix)

        gl.glEnableVertexAttribArray(self.UVLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.uvbo)
        pgl.glVertexAttribPointer(self.UVLoc, 2, gl.GL_FLOAT,
                gl.GL_FALSE, 0, None)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.nverts)

        gl.glDisableVertexAttribArray(self.UVLoc)

