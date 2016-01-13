# Cook-Torance for diffuseType and Blinn-Phong
# Figure out specular and frensel stuff
# Emission?
# Need to setup so it can send outputs to a shader
# Inputs need to be defined a lot better
class Material(object):
    def __init__(self):
        self.diffuse = None
        self.idiffuse = 0 # Intensity parameter

        self.ambient = None
        self.iambient = 0 # Intensity parameter

        self.specular = None
        self.roughness = None

        self.albedo = None

        self.diffuseType = None
        self.specularType = None

        self.normalMap = None
        self.specularMap = None
        self.displacementMap = None

        # Not sure if this is needed yet
        self.shader = None

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

    # This will replace the texture assignment via Mesh class
    def addTexture(self, texture):
        ''' This sets the diffuse albeo/texture of the material. '''
        self.albedo = texture
