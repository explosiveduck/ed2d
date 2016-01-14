
from ed2d.mesh import MeshBase
from ed2d.assets.mtlloader import MTL

class OBJ(object):
    def __init__(self, fileName):
        ''' Wavefront .obj file parser.'''
        fcount = 0
        vcount = 0
        vtcount = 0
        vncount = 0

        # Load the file
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

        fcount *= 3
        vcount *= 3
        vtcount *= 3
        vncount *= 3

        self.tempVertices = [None] * vcount
        self.tempNormals = [None] * vncount

        self.tempUVs = [None] * fcount

        self.vertexIndices = [None] * fcount
        self.normalIndices = [None] * fcount
        self.uvIndices = [None] * fcount

        self.finalVertices = [None] * fcount
        self.finalNormals = [None] * fcount
        self.finalUVs = [None] * fcount

        self.fnumber = 0
        self.vnumber = 0
        self.vtnumber = 0
        self.vnnumber = 0

        # Process the data
        self.__process_in_house(objfile)
        # Finalize
        self.get_final_data()

        # Close the file
        objfile.close()

    def __process_in_house(self, objfl):
        with open(filename, "r") as objfl:

            for line in objfl:

                value = line.split()
                valueType = value[0]

                if valueType not in ['f', 'v', 'vt', 'vn']:
                    continue

                value = value[1:]

                # Check first and continue on early because of string splitting
                if valueType == "f":
                    temp = [item.split("/") for item in value]

                    for i in range(3):
                        if temp[i][1] != '':
                            self.uvIndices[fnumber] = int(temp[i][1])
                        self.vertexIndices[fnumber] = int(temp[i][0])
                        self.normalIndices[fnumber] = int(temp[i][2])
                        fnumber += 1

                    continue

                value = list(map(float, value))

                if valueType == "v":
                    v = [value[0], value[1], value[2]]
                    self.tempVertices[vnumber] = v
                    self.vnumber += 1

                elif valueType == "vt":
                    vt = [value[0], value[0]]
                    self.tempUVs[vtnumber] = vt
                    self.vtnumber += 1

                elif valueType == "vn":
                    n = [value[0], value[1], value[2]]
                    self.tempNormals[vnnumber] = n
                    self.vnnumber += 1

    def get_final_data(self):
        for i in range(fcount):
            vertexIndex = int(self.vertexIndices[i]) - 1
            vertex = self.tempVertices[vertexIndex]
            self.finalVertices[i] = vertex

            normalIndex = self.normalIndices[i]
            normal = self.tempNormals[int(normalIndex) - 1]
            self.finalNormals[i] = normal

            if self.uvIndices[0] is None and vtcount != 0:
                uvIndex = self.uvIndices[i]
                uv = self.tempUVs[int(uvIndex) - 1]
                self.finalUVs[i] = uv

class ObjMesh(MeshBase):
    def __init__(self, filePath, name, program, vertexLoc, normalLoc):
        super(ObjMesh, self).__init__(filePath, name, program, vertexLoc, normalLoc)
