from ed2d.assets.mtlloader import MTL
from ed2d import files

def merge_dicts(dicts):
    dictKeys = set()
    for dic in dicts:
        dictKeys.update(dic.keys())
    
    finalDictionary = {}

    for key in dictKeys:
        # Vertices
        finalDictionary[key] = [ [], [], [] ]
     
    for dic in dicts:
        for key in dictKeys:
            try:
                # Vertices
                for i, data in enumerate(dic[key]):
                    finalDictionary[key][i].extend(data)
            except KeyError:
                pass
            
    return finalDictionary


class OBJObject(object):
    ''' Storage for each object inside a .obj file.'''
    def __init__(self, data):
        # Store the lines that represent one object from obj file.
        self.object = data
        # Size of the object
        self.objectlen = len(self.object)
        # Store number of faces/indices
        self.fcount = 0
        # Store number of vertices
        self.vcount = 0
        # Store numver of uv indices
        self.vtcount = 0
        # Store number of normals
        self.vncount = 0
        # Store number of materials used
        self.gcount = 0

        # Indices dict
        self.tmvnig = {}
        # Final parsed data dict
        self.fmvnig = {}

        # Material list
        self.matList = []

        # Do a head count and setup the storage layout using dictionaries
        for i in range(self.objectlen):
            value = self.object[i][:2]
            if value == 'v ':
                self.vcount += 1
            elif value == 'vt':
                self.vtcount += 1
            elif value == 'vn':
                self.vncount += 1
            elif value == 'g ':
                self.gcount += 1
                # The material used currently
                materialName = None
                if self.object[i+1][:6] == 'usemtl':
                    materialName = self.object[i+1].split()[1]
                    self.matList.append(materialName)
                    # Initialize the two dictionaries, indices and final data
                    self.tmvnig[materialName] = [ [], [], [] ]
                    self.fmvnig[materialName] = [ [], [], [] ]


                for j in range(i+2, self.objectlen, 1):
                    fval = self.object[j][:2]

                    if fval == 'f ':
                        self.fcount += 1
                        # Vertices
                        self.tmvnig[materialName][0].extend(None for _ in range(3))
                        self.fmvnig[materialName][0].extend([None] for _ in range(3))
                        # Normals
                        self.tmvnig[materialName][2].extend(None for _ in range(3))
                        self.fmvnig[materialName][2].extend([None] for _ in range(3))
                        # UV Coordinates (usually these are not always generated)
                        if self.vtcount != 0:
                            self.tmvnig[materialName][1].extend(None for _ in range(3))
                            self.fmvnig[materialName][1].extend([None] for _ in range(3))
                    elif fval == 'g ':
                        # We need this here for any material that is not the last
                        # Otherwise it will not know when to stop
                        break

        # Faces, Vertices, UVs, Normals each store 3 values per line
        self.fcount *= 3
        self.vcount *= 3
        self.vtcount *= 3
        self.vncount *= 3

        # Create temporary storage
        self.tempVertices = [None] * self.vcount
        self.tempNormals = [None] * self.vncount
        self.tempUVs = [None] * self.fcount

        # Store the final counts
        self.fnumber = 0
        self.vnumber = 0
        self.vtnumber = 0
        self.vnnumber = 0
        self.matnumber = 0



class OBJ(object):
    def __init__(self, fileName):
        ''' Wavefront .obj file parser.'''
        ocount = 0

        __objpath = files.resolve_path('data', 'models', fileName + '.obj')
        __mtlpath = files.resolve_path('data', 'models', fileName + '.mtl')
        __txtpath = files.resolve_path('data', 'models', fileName + '.txt')

        # Load the mtl file
        self.mtlfile = MTL(__mtlpath)

        # Load the obj file
        with open(__objpath, 'r') as objfile:
            lines = objfile.readlines()
            lineslen = len(lines)

            self.objects = []
            self.fmvnig = {}
            
            start = []
            end = []
            # Do an object count in the file
            for i in range(lineslen):
                value = lines[i][:2]
                value1 = lines[i - 1][:2]
                # Look for 'o ' at the begining of the line and count them
                if value1 == 'o ':
                    # Create a layout of where all the lines starting with o start
                    ocount +=1
                    start.append((i - 1))
                if (value1 == 'f ' or value1 == 'l ') and value == 'o ':
                    end.append((i + 1))
            end.append(lineslen)

            for i in range(len(end)):
                self.objects.append(OBJObject(lines[start[i]:end[i]]))

        vertNumberOffset = 0
        normNumberOffset = 0
        vtNumberOffset = 0
        for i in range(len(self.objects)):
            self.__process_in_house(self.objects[i], vertNumberOffset, normNumberOffset, vtNumberOffset)
            vertNumberOffset += (self.objects[i].vcount / 3)
            normNumberOffset += (self.objects[i].vncount / 3)
            vtNumberOffset += (self.objects[i].vtcount / 3)

        for i in range(len(self.objects)):
            self.get_final_data(self.objects[i])

        self.combine_data()

        # Debug Output
        #self.write(__txtpath)

    def write(self, filename):
        ''' Used for debuging. '''
        objfile = open(filename, "w")
        for j in range(self.matnumber):
            objfile.write('\n')
            matrname = list(self.tmvnig.keys())[j]
            objfile.write(matrname + '\n')
            objfile.write('VERTICES\n')
            for i in range(len(self.fmvnig[matrname][0]) - 1):
                objfile.write(str(self.tmvnig[matrname][0][i]) + " " + str(self.fmvnig[matrname][0][i]) + '\n')
            objfile.write('NORMALS\n')
            for k in range(len(self.fmvnig[matrname][0]) - 1):
                objfile.write(str(self.tmvnig[matrname][2][k]) + " " + str(self.fmvnig[matrname][2][k]) + '\n')
        objfile.close()

    def __process_in_house(self, obj, voffset, noffset, vtoffset):
        matname = None

        for line in obj.object:

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
                obj.matnumber += 1
                obj.fnumber = 0
                continue

            if valueType == "f":
                temp = [item.split("/") for item in value]
                for i in range(3):
                    # 0 - Vertex
                    # 1 - UV
                    # 2 - Normal
                    # Make sure UV index data exists
                    if temp[i][1] != '':
                        obj.tmvnig[matname][1][obj.fnumber] = abs(int(temp[i][1]) - vtoffset)
                    obj.tmvnig[matname][0][obj.fnumber] = abs(int(temp[i][0]) - voffset)
                    obj.tmvnig[matname][2][obj.fnumber] = abs(int(temp[i][2]) - noffset)
                    obj.fnumber += 1
                continue

            # Map the values after the keyword to floats
            value = list(map(float, value))

            if valueType == "v":
                v = [value[0], value[1], value[2]]
                obj.tempVertices[obj.vnumber] = v
                obj.vnumber += 1

            elif valueType == "vt":
                vt = [value[0], value[0]]
                obj.tempUVs[obj.vtnumber] = vt
                obj.vtnumber += 1

            elif valueType == "vn":
                n = [value[0], value[1], value[2]]
                obj.tempNormals[obj.vnnumber] = n
                obj.vnnumber += 1


    def get_final_data(self, obj):
        for j in range(obj.matnumber):
            matrname = list(obj.tmvnig.keys())[j]
            for i in range(len(obj.tmvnig[matrname][0])):
                vertexIndex = int(obj.tmvnig[matrname][0][i]) - 1
                vertex = obj.tempVertices[vertexIndex]
                obj.fmvnig[matrname][0][i] = vertex

                normalIndex = int(obj.tmvnig[matrname][2][i]) - 1
                normal = obj.tempNormals[normalIndex]
                obj.fmvnig[matrname][2][i] = normal

                if obj.tmvnig[matrname][1] is None and obj.vtnumber != 0:
                    uvIndex = int(obj.tmvnig[matrname][1][i]) - 1
                    uv = obj.tempUVs[uvIndex]
                    obj.fmvnig[matrname][1][i] = uv

    def combine_data(self):
        obj = [obj.fmvnig for obj in self.objects]
        self.fmvnig = merge_dicts(obj)
