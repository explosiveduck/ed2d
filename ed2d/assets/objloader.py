
from ed2d.mesh import MeshBase
from ed2d.assets.mtlloader import MTL

class OBJ(object):
    def __init__(self, fileName):
        ''' Wavefront .obj file parser.'''
        fcount = 0
        vcount = 0
        vtcount = 0
        vncount = 0
        matcount = 0

        __objpath = files.resolve_path('data', 'models', 'fileName' + '.obj')
        __mtlpath = files.resolve_path('data', 'models', 'fileName' + '.mtl')

        # Load the mtl file
        self.mtlfile = MTL(__mtlpath)

        # Load the obj file
        objfile = open(fileName, "r")

        # Do a head count
        for line in objfile:
            value = line[:2]
            if value == 'f ':
                fcount += 1
            elif value == 'v ':
                vcount += 1
            elif value == 'vt':
                vtcount += 1
            elif value == 'vn':
                vncount += 1
            elif value == 'g ':
                matcount += 1

        # Close the file
        objfile.close()

        fcount *= 3
        vcount *= 3
        vtcount *= 3
        vncount *= 3

        self.tempVertices = [None] * vcount
        self.tempNormals = [None] * vncount
        self.tempUVs = [None] * fcount
        self.tempMaterials = [None] * matcount

        self.vertexIndices = [None] * fcount
        self.normalIndices = [None] * fcount
        self.uvIndices = [None] * fcount

        self.finalVertices = [None] * fcount
        self.finalNormals = [None] * fcount
        self.finalUVs = [None] * fcount
        self.usedMaterials = [None] * matcount

        self.fnumber = 0
        self.vnumber = 0
        self.vtnumber = 0
        self.vnnumber = 0
        self.matnumber = 0

        # Process the data
        self.__process_in_house(__objpath)
        # Finalize
        self.get_final_data()

    def __process_in_house(self, filename):
        with open(filename, "r") as objfl:

            for line in objfl:

                value = line.split()
                valueType = value[0]

                # Don't bother unless the following key words exist in the line
                if valueType not in ['f', 'v', 'vt', 'vn', 'g', 'usemtl']:
                    continue

                # Start ignoring the first word of the line to grab the values
                value = value[1:]

                # Check first and continue on early because of string splitting
                if valueType == "f":
                    temp = [item.split("/") for item in value]

                    for i in range(3):
                        # Make sure UV index exists
                        if temp[i][1] != '':
                            self.uvIndices[self.fnumber] = int(temp[i][1])
                        self.vertexIndices[self.fnumber] = int(temp[i][0])
                        self.normalIndices[self.fnumber] = int(temp[i][2])
                        self.fnumber += 1

                    continue

                # Map the values after the keyword to floats
                value = list(map(float, value))

                if valueType == "v":
                    v = [value[0], value[1], value[2]]
                    self.tempVertices[self.vnumber] = v
                    self.vnumber += 1

                elif valueType == "vt":
                    vt = [value[0], value[0]]
                    self.tempUVs[self.vtnumber] = vt
                    self.vtnumber += 1

                elif valueType == "vn":
                    n = [value[0], value[1], value[2]]
                    self.tempNormals[self.vnnumber] = n
                    self.vnnumber += 1

                elif valueType == "g":
                    g = value[0]
                    self.tempMaterials[self.matnumber] = g
                    self.matnumber += 1
                elif valueType == "usemtl":
                    gs = value[0]
                    # Need a way to generate which material per what face
                    # In a specific order
                    self.usedMaterials[sef.matnumber] = gs

    def get_final_data(self):
        for i in range(self.fcount):
            vertexIndex = int(self.vertexIndices[i]) - 1
            vertex = self.tempVertices[vertexIndex]
            self.finalVertices[i] = vertex

            normalIndex = self.normalIndices[i]
            normal = self.tempNormals[int(normalIndex) - 1]
            self.finalNormals[i] = normal

            if self.uvIndices[0] is None and self.vtcount != 0:
                uvIndex = self.uvIndices[i]
                uv = self.tempUVs[int(uvIndex) - 1]
                self.finalUVs[i] = uv

class ObjMesh(MeshBase):
    def __init__(self, filePath, name, program, vertexLoc, normalLoc):
        super(ObjMesh, self).__init__(filePath, name, program, vertexLoc, normalLoc)
