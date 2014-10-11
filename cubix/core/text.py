import ctypes as ct
import sdl2 as sdl
from sdl2 import sdlttf

from cubix.core import texture
from cubix.core import mesh
from cubix.core import shaders
from cubix.core.opengl import gl

def init_text():
    sdlttf.TTF_Init()

class Text(object):
    def __init__(self, size, fontPath):

        vsPath = files.resolve_path('data', 'shaders', 'text.vs')
        fsPath = files.resolve_path('data', 'shaders', 'text.fs')

        vertex = shaders.VertexShader(vsPath)
        fragment = shaders.FragmentShader(fsPath)

        self.program = shaders.ShaderProgram(vertex, fragment)
        self.program.use()

        self.texAtlas = texture.TextureAtlas(self.program)


        self.fontFile = sdlttf.TTF_OpenFont(typeutils.to_c_str(fontPath) , size )

        # Color to render in we want white initialy
        color = sdl.SDL_Color()
        color.r = 255
        color.g = 255
        color.b = 255
        color.a = 255

        for item in range(128):
            glyph = sdlttf.TTF_RenderGlyph_Blended(font, ord('u'), color)

            dataType = (ct.c_ubyte * 4 * (glyph.contents.w * glyph.contents.h))
            dataPython = [[0.0 for sub in range(4)]for x in range(glyph.contents.w * glyph.contents.h)]

            obj = ct.cast(glyph.contents.pixels, ct.POINTER(dataType))
            for item in range(glyph.contents.w * glyph.contents.h):
                for item3 in range(4):
                    dataPython[item][item3] = obj.contents[item][item3]

            self.texAtlas.add_texture(glyph.contents.w, glyph.contents.h, dataPython)

            sdl.SDL_FreeSurface(glyph)


        self.orthoID = self.program.new_uniform(b'ortho')

        self.ortho = glmath.ortho(0.0, self.width, self.height, 0.0, -1.0, 1.0)

        self.program.set_uniform_matrix(self.orthoID, self.ortho)

    def render(self):
        pass