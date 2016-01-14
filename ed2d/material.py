# Cook-Torance for diffuseType and Blinn-Phong
# Figure out specular and frensel stuff
# Emission?
# Need to setup so it can send outputs to a shader
# Inputs need to be defined a lot better
from ed2d import texture.py
from ed2d import files.py

class Material(object):
    def __init__(self, program):
        self.diffuse = None
        self.idiffuse = 0 # Intensity parameter

        self.ambient = None
        self.iambient = 0 # Intensity parameter

        self.specular = None
        self.roughness = None

        # This is the diffuse texture
        self.albedo = None

        self.diffuseType = None
        self.specularType = None

        self.normalMap = None
        self.specularMap = None
        self.displacementMap = None

        # Assign the shader that will render the Material
        self.program = program

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

    def diffuseType(self, shader):
        pass

    def specularType(self, shader):
        pass

    def addTextures(self, textureDict):
        # This will replace the crap underneath this function
        pass

    # This will replace the texture assignment via Mesh class
    def addTexture(self, textureFileName):
        ''' This sets the diffuse albeo/texture of the material. '''
        imagePath = files.resolve_path('data', 'images', textureFileName)
        self.albedo = texture.Texture(imagePath, self.program)

    def addNormalMap(self, textureFileName):
        imagePath = files.resolve_path('data', 'images', textureFileName)
        self.normalMap = texture.Texture(imagePath, self.program)

    def addSpecularMap(self, textureFileName):
        imagePath = files.resolve_path('data', 'images', textureFileName)
        self.specularMap = texture.Texture(imagePath, self.program)

    def addDisplacementMap(self, textureFileName):
        imagePath = files.resolve_path('data', 'images', textureFileName)
        self.displacementMap = texture.Texture(imagePath, self.program)
