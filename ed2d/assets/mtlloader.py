from ed2d import material

class MTL(object):
    def __init__(self, filename):
        self.data = {}
        self.material = material.Material()
        self.__load(filename)

    def __load(self, filename):
        materialName = None
        value = None
        valueType = None

        for line in open(filename, "r"):
            # Avoid lines starting with "#"
            if line.startswith('#'):
                continue
            else:
                value = line.split()
                # Make sure the line is no empty
                if not value:
                    continue
                else:
                    valueType = value[0]

            # Check for material
            if valueType == 'newmtl':
                self.material = self.data[value[1]] = material.Material()
                materialName = value[1]
                continue
            elif self.material is None:
                print("Error, material member is None.")
                break

            # Generate a list of floats using the numbers
            value = list(map(float, value[1:]))

            if valueType == 'Ns':
                # Material Specular Exponent which is multipled by texture value
                self.data[materialName].ispecular = value[0]
            elif valueType == 'Ka':
                # Ambient color
                self.data[materialName].ambient = [value[0], value[1], value[2]]
            elif valueType == 'Kd':
                # Diffuse color
                self.data[materialName].diffuse = [value[0], value[1], value[2]]
            elif valueType == 'Ks':
                # Specular color
                self.data[materialName].specular = [value[0], value[1], value[2]]
            elif valueType == 'Ke':
                # Emission color
                self.data[materialName].emission = [value[0], value[1], value[2]]
            elif valueType == 'Ni':
                # Optical Denisty or Index of Refraction
                self.data[materialName].IOR = value[0]
            elif valueType == 'map_Kd':
                # Diffuse texture is multiplied by the Kd
                self.data[materialName].albedoLayers['test'] = value[0]
                # Do texture stuff here
            elif valueType == 'map_Ks':
                # Specular texture is multiplied by the Ks
                self.data[materialName].specularMapLayers['test'] = value[0]
            elif valueType == 'map_Ns':
                # Texture linked to the specular exponent and is multiplied by Ns
                pass

# NOTE:
'''
During rendering, the Ka, Kd, and Ks values and the map_Ka, map_Kd, and map_Ks values are blended according to the following formula:

result_color=tex_color(tv)*decal(tv)+mtl_color*(1.0-decal(tv))

where tv is the texture vertex.

"result_color" is the blended Ka, Kd, and Ks values.
'''
