
from ed2d.mesh import MeshBase
from ed2d.assets.mtlloader import MTL
from ed2d import files

class OBJ(object):
    def __init__(self, fileName):
        ''' Wavefront .obj file parser.'''
        fcount = 0
        vcount = 0
        vtcount = 0
        vncount = 0
        gcount = 0

        self.tmvnig = {} # Indices dictionary
        self.fmvnig = {} # Final data dictionary

        __objpath = files.resolve_path('data', 'models', fileName + '.obj')
        __mtlpath = files.resolve_path('data', 'models', fileName + '.mtl')
        __txtpath = files.resolve_path('data', 'models', fileName + '.txt')

        # Load the mtl file
        self.mtlfile = MTL(__mtlpath)

        # Load the obj file
        objfile = open(__objpath, "r")

        lines = objfile.readlines()
        lineslen = len(lines)

        # Do a head count and setup the storage layout using dictionaries
        for i in range(lineslen):
            value = lines[i][:2]
            if value == 'v ':
                vcount += 1
            elif value == 'vt':
                vtcount += 1
            elif value == 'vn':
                vncount += 1
            elif value == 'g ':
                gcount += 1
                # The material used currently
                materialName = None
                if lines[i+1][:6] == 'usemtl':
                    materialName = lines[i+1].split()[1]
                    # Initialize the two dictionaries, indices and final data
                    self.tmvnig[materialName] = [ [], [], [] ]
                    self.fmvnig[materialName] = [ [], [], [] ]

                for j in range(i+2, lineslen, 1):
                    fval = lines[j][:2]

                    if fval == 'f ':
                        fcount += 1
                        # Vertices
                        self.tmvnig[materialName][0].extend(None for _ in range(3))
                        self.fmvnig[materialName][0].extend([None] for _ in range(3))
                        # Normals
                        self.tmvnig[materialName][2].extend(None for _ in range(3))
                        self.fmvnig[materialName][2].extend([None] for _ in range(3))
                        # UV Coordinates (usually these are not always generated)
                        if vtcount != 0:
                            self.tmvnig[materialName][1].extend(None for _ in range(3))
                            self.fmvnig[materialName][1].extend([None] for _ in range(3))
                    elif fval == 'g ':
                        # We need this here for any material that is not the last
                        # Otherwise it will not know when to stop
                        break

        # Close the file
        objfile.close()

        fcount *= 3
        vcount *= 3
        vtcount *= 3
        vncount *= 3

        self.tempVertices = [None] * vcount
        self.tempNormals = [None] * vncount
        self.tempUVs = [None] * fcount

        self.fnumber = 0
        self.vnumber = 0
        self.vtnumber = 0
        self.vnnumber = 0
        self.matnumber = 0

        # Process the data
        self.__process_in_house(__objpath)
        # Finalize
        self.get_final_data()

        # Debug Output
        #self.write(__txtpath)

    def write(self, filename):
        ''' Used for debuging. '''
        objfile = open(filename, "w")
        for j in range(self.matnumber):
            objfile.write('\n')
            matrname = self.tmvnig.keys()[j]
            objfile.write(matrname + '\n')
            objfile.write('VERTICES\n')
            for i in range(len(self.fmvnig[matrname][0]) - 1):
                objfile.write(str(self.tmvnig[matrname][0][i]) + " " + str(self.fmvnig[matrname][0][i]) + '\n')
            objfile.write('NORMALS\n')
            for k in range(len(self.fmvnig[matrname][0]) - 1):
                objfile.write(str(self.tmvnig[matrname][2][k]) + " " + str(self.fmvnig[matrname][2][k]) + '\n')
        objfile.close()

    def __process_in_house(self, filename):
        matname = None
        with open(filename, "r") as objfl:

            for line in objfl:

                value = line.split()
                valueType = value[0]

                # Don't bother unless the following key words exist in the line
                if valueType not in ['f', 'v', 'vt', 'vn', 'usemtl']:
                    continue

                # Start ignoring the first word of the line to grab the values
                value = value[1:]

                # Check first and continue on early because of string splitting
                if valueType == "usemtl":
                    matname = value[0]
                    # Material Vertex UV Normal Indices Group (Vertex, UV, Normal)
                    self.matnumber += 1
                    self.fnumber = 0
                    continue

                if valueType == "f":
                    temp = [item.split("/") for item in value]

                    for i in range(3):
                        # 0 - Vertex
                        # 1 - UV
                        # 2 - Normal
                        # Make sure UV index data exists
                        if temp[i][1] != '':
                            self.tmvnig[matname][1][self.fnumber] = int(temp[i][1])
                        self.tmvnig[matname][0][self.fnumber] = int(temp[i][0])
                        self.tmvnig[matname][2][self.fnumber] = int(temp[i][2])
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


    def get_final_data(self):
        for j in range(self.matnumber):
            matrname = self.tmvnig.keys()[j]
            for i in range(len(self.tmvnig[matrname][0])):
                vertexIndex = int(self.tmvnig[matrname][0][i]) - 1
                vertex = self.tempVertices[vertexIndex]
                self.fmvnig[matrname][0][i] = vertex

                normalIndex = int(self.tmvnig[matrname][2][i]) - 1
                normal = self.tempNormals[normalIndex]
                self.fmvnig[matrname][2][i] = normal

                if self.uvIndices[0] is None and self.vtnumber != 0:
                    uvIndex = int(self.tmvnig[matrname][1][i]) - 1
                    uv = self.tempUVs[uvIndex]
                    self.fmvnig[matrname][1][i] = uv

class ObjMesh(MeshBase):
    def __init__(self, filePath, name, program, vertexLoc, normalLoc):
        super(ObjMesh, self).__init__(filePath, name, program, vertexLoc, normalLoc)
