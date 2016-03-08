from ed2d.assets.mtlloader import MTL
from ed2d import files

class OBJ(object):
    def __init__(self, fileName):
        ''' Wavefront .obj file parser.'''
        objPath = files.resolve_path('data', 'models', fileName + '.obj')

        self.fmvnig = {}

        # Shared temporary storage of data
        self.tempVertices = []
        self.tempNormals = []
        self.tempUVs = []

        # Load the obj file
        with open(objPath, 'r') as objfile:
            self.lines = objfile.readlines()

        self.parse()


    def parse(self):
        ''' Perform the parsing of the obj format  '''

        matname = None
        valueType = None

        for line in self.lines:
            valueType, value = line.strip().split(' ', 1)

            # Don't bother unless the following key words exist in the line
            if valueType not in ['o', 'g', 'f', 'v', 'vt', 'vn', 'usemtl', 'mtllib']:
                continue

            value = value.split(' ')

            # Check first and continue on early because of string splitting
            if valueType == "usemtl":
                matname = value[0]
                continue

            if valueType in ['g', 'o']:
                # These objects reset state basically
                matname = None
                continue

            if valueType == 'mtllib':
                mtlpath = files.resolve_path('data', 'models', value[0])

                # Load the mtl file
                self.mtlfile = MTL(mtlpath)
                for material in self.mtlfile.data.keys():
                    self.fmvnig[material] = [ [], [], [] ]

                continue

            if valueType == "f":
                face = [item.split("/") for item in value]
                for typeGroup in face:
                    for typeIndex in range(len(typeGroup)):
                        if typeIndex == 0: # Vertex
                            typeSource = self.tempVertices
                        elif typeIndex == 1: # UV
                            typeSource = self.tempUVs
                        elif typeIndex == 2: # Normal
                            typeSource = self.tempNormals

                        index = typeGroup[typeIndex]

                        # Make sure data exists
                        if index != '':
                            index = int(index)
                            typeData = typeSource[index - 1]

                            self.fmvnig[matname][typeIndex].append(typeData)
                continue

            # Map the values after the keyword to floats
            value = list(map(float, value))

            if valueType == "v":
                self.tempVertices.append(value)

            elif valueType == "vt":
                self.tempUVs.append(value * 2)

            elif valueType == "vn":
                self.tempNormals.append(value)
