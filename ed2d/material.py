# Cook-Torance for diffuseType and Blinn-Phong
# Figure out specular and frensel stuff
# Emission?
# Need to setup so it can send outputs to a shader
# Inputs need to be defined a lot better
from ed2d import texture
from ed2d import files

class Material(object):
    def __init__(self):
        self.diffuse = None
        self.idiffuse = 0 # Intensity parameter

        self.ambient = None
        self.iambient = 0 # Intensity parameter

        self.specular = None
        self.roughness = None

        # This is the diffuse textures
        self.albedoLayers = {}

        self.diffuseType = None
        self.specularType = None

        self.normalMapLayers = {}
        self.specularMapLayers = {}
        self.displacementMapLayers = {}

        # Assign the shader that will render the Material
        self.program = program

    def addProgram(self, program):
        ''' Adds a program to the Material class. '''
        pass

    def setDiffuseColor(self, r, g, b, intensity):
        ''' Sets the diffuse color of a material. '''
        self.diffuse = [r, g, b]
        self.idiffuse = intensity

    def setAmbientColor(self, r, g, b, intensity):
        ''' Sets the ambient color of a material. '''
        self.ambient = [r, g, b]
        self.iambient = intensity

    def setSpecularColor(self, r, g, b, roughness):
        ''' Sets the specular color and roughness of a material. '''
        self.specular = [r, g, b]
        self.roughness = roughness

    # Leave these like this for now till I figure out the shaders
    def setDiffuseType(self, shader):
        pass

    def setSpecularType(self, shader):
        pass

    def addTextures(self, textureDict):
        ''' Will add textures to the Material. It takes a dictionary as param. '''
        # Format is {A: [albedo0, albedo1, ...], N: [normal1, normal2, ...], S: [specular1, specular2, ...]}
        # This will replace the crap underneath this function
        for key, value in textureDict.iteritems():
            if key is 'A':
                for i in range(len(value)):
                    imagePath = files.resolve_path('data', 'images', value[i])
                    self.albedoLayers['Layer' + i] = texture.Texture(imagePath, self.program)
            if key is 'N':
                for i in range(len(value)):
                    imagePath = files.resolve_path('data', 'images', value[i])
                    self.normalMapLayers['Layer' + i] = texture.Texture(imagePath, self.program)
            if key is 'S':
                for i in range(len(value)):
                    imagePath = files.resolve_path('data', 'images', value[i])
                    self.specularMapLayers['Layer' + i] = texture.Texture(imagePath, self.program)
