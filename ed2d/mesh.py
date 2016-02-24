from gem import matrix
from gem import vector
from ed2d.opengl import gl, pgl
from ed2d.assets import objloader


def buffer_object(data, typeM):
    if data or 0:
        vbo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        pgl.glBufferData(gl.GL_ARRAY_BUFFER, data, typeM, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        return vbo
    else:
        return None


def index_buffer_object(data, typeM):
    if data or 0:
        ibo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)
        pgl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, data, typeM,
                         gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        return ibo
    else:
        return None


def bind_object(dataLoc, vbo, size):
    if (dataLoc is not None) and (vbo is not None):
        gl.glEnableVertexAttribArray(dataLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        pgl.glVertexAttribPointer(dataLoc, size, gl.GL_FLOAT, gl.GL_FALSE, 0,
                                  None)
    else:
        pass


def unbind_object(dataLoc):
    if dataLoc is not None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glDisableVertexAttribArray(dataLoc)
    else:
        pass

def calc_face_normal(vertex1, vertex2, vertex3):
    ''' Calculate a face normal from 3 vertices. 3D Vector inputs. '''
    vertex11 = vertex2 - vertex1
    vertex22 = vertex3 - vertex1
    normal = vertex11.cross(vertex22)
    normal.i_normalize()
    return normal

# Conver matrix 4x4 to 3x3
def convertM4to3(mat):
    ''' Convert a 4x4 Matrix to 3x3. '''
    temp = [[0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]]

    for i in range(3):
        for j in range(3):
            temp[i][j] = mat[i][j]

    out = matrix.Matrix(3)
    out.matrix = temp
    return out


class Indexer(object):
    ''' This is needed for CSG.'''
    def __init__(self):
        self.unique = []
        self.indices = []
        self.map = {}

    def add(self, obj):
        key = repr(obj)

        if not (key in self.map):
            self.map[key] = len(self.unique)
            self.unique.append(obj)

        return self.map[key]


class MeshBase(object):
    def __init__(self):
        self.program = None
        self.vertLoc = None
        self.UVLoc = None
        self.colorLoc = None
        self.normLoc = None
        self.modelID = None
        self.texture = None
        self.obj2world = matrix.Matrix(4)
        self.matrix = matrix.Matrix(4) # Model matrix
        self.modelInverseTranspose = matrix.Matrix(4)

        self.vbos = []
        self.cbos = []
        self.nbos = []

    def addProgram(self, program):
        self.program = program
        self.vertLoc = self.program.get_attribute(b'vertexPosition_modelspace')
        self.normLoc = self.program.get_attribute(b'normal_modelspace')
        #self.UVLoc = self.program.get_attribute(b'vertexUV')
        self.colorLoc = self.program.get_attribute(b'vertexColor')
        self.modelID = self.program.new_uniform(b'model_matrix')
        self.invModelLoc = self.program.new_uniform(b'gMdVw')


    def render(self):
        self.program.set_uniform_matrix(self.modelID, self.matrix)
        self.program.set_uniform_matrix(self.invModelLoc, self.modelInverseTranspose)

        i = 0
        for key in self.materials:
            try:
                bind_object(self.vertLoc, self.vbos[i], 3)
                bind_object(self.normLoc, self.nbos[i], 3)
                bind_object(self.colorLoc, self.cbos[i], 3)

                gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.verData[key]))

                unbind_object(self.colorLoc)
                unbind_object(self.normLoc)
                unbind_object(self.vertLoc)
                i += 1
            except KeyError:
                pass

    def buffer_objects(self):
        if self.importedModel:
            for key in self.materials:
                try:
                    self.vbos.append(buffer_object(self.verData[key], gl.GLfloat))
                    self.nbos.append(buffer_object(self.norData[key], gl.GLfloat))
                    self.cbos.append(buffer_object(self.colData[key], gl.GLfloat))
                except KeyError:
                    pass
        else:
            self.vbo = buffer_object(self.vertices, gl.GLfloat)
            self.uvbo = buffer_object(self.texCoord, gl.GLfloat)
            self.ibo = index_buffer_object(self.triangles, gl.GLuint)

class Mesh(MeshBase):
    def __init__(self):
        super(Mesh, self).__init__()

        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.xPosDelta = 0
        self.yPosDelta = 0
        self.zPosDelta = 0

        self._scale = 1
        self.scaleDelta = 0

        self.verData = {}
        self.norData = {}
        self.colData = {}
        self.rect = None
        self.nverts = 0
        self.ntris = 0

        self.vertices = []
        self.texCoord = []
        self.normals = []
        self.colors = []
        self.triangles = []
        self.materials = {}

        self.physObj = None
        self.importedModel = False

    def setColorAll(self, r, g, b):
        '''
        This will populate the colors array with same color for every vertex.
        '''
        if not self.colors:
            for i in range(self.nverts):
                self.colors.append([r, g, b])
        else:
            for i in range(self.nverts):
                self.colors[i] = [r, g, b]

    def addMaterial(self, name, material):
        # Add a material to the mesh
        self.materials[name] = material

    def fromData(self, data, normals=None, texCoord=None):
        '''
        This will take in any set of vertices, uv coordinates and colors arrays
        '''

        if isinstance(data, objloader.OBJ):
            self.importedModel = True
            self.materials = data.mtlfile.data

            for key, value in data.fmvnig.items():
                # Vertices
                self.verData[key] = value[0]
                # Normals
                self.norData[key] = value[2]

            for key, value in self.materials.items():
                try:
                    self.colData[key] = []
                    for i in range(len(self.verData[key])):
                            self.colData[key].append(value.diffuse)
                except KeyError:
                    pass
        else:
            self.importedModel = False
            self.vertices = data
            self.nverts = len(self.vertices)

            if normals is not None:
                self.normals = normals

            if texCoord is not None:
                self.texCoord = texCoord
            else:
                self.texCoord = self.vertices

        self.buffer_objects()

    def fromCSG(self, csg):
        '''
        This will take in a CSG object and convert it to mesh for
        rendering and simulation purposes.
        '''
        indexer = Indexer()
        polygons = csg.toPolygons()

        for i in range(len(polygons)):
            polygon = polygons[i]
            indices = []
            for j in range(len(polygon.vertices)):
                vertex = polygon.vertices[j]
                vertex.color = polygon.shared or [1.0, 1.0, 1.0]
                index = indexer.add(vertex)
                indices.append(index)
            for k in range(2, len(indices), 1):
                self.triangles.append([indices[0], indices[k - 1], indices[k]])

        for i in range(len(indexer.unique)):
            v = indexer.unique[i]
            self.vertices.append(v.pos.vector)
            self.normals.append(v.normal.vector)
            self.colors.append(v.color)

        # print("Indexer Unique Count: ", len(indexer.unique))
        # print("Polygon Count: ", len(polygons))
        # print("Triangles Count: ", len(self.triangles))
        # print("Vertices Count: ", len(self.vertices))

        self.nverts = len(self.vertices)
        self.ntris = len(self.triangles)

        self.buffer_objects()

    def addPhysicsObject(self, physObj):
        '''This will attach a physics object to the mesh.'''
        self.physObj = physObj
        self.rect = physObj.getCollisionModel().getModel()
        self.vertices = self.rect.getVertices()
        self.texCoord = self.rect.getVertices()
        self.matrix = self.rect.getModelMatrix()

    def scale(self, value):
        self.scaleDelta = value / self._scale
        self._scale = value

    def translate(self, x, y, z):
        self.xPosDelta += x - self.xPos
        self.yPosDelta += y - self.yPos
        self.zPosDelta += z - self.zPos
        self.xPos = x
        self.yPos = y
        self.zPos = z

    # TODO - Needs to be checked
    def rotate(self, axis, angle):
        self.rotationMatrix = matrix.Matrix(4).rotate(axis, angle)
        self.matrix *= self.rotationMatrix

    def update(self):

        if self.physObj is None:
            pass
        else:
            self.rect = self.physObj.getCollisionModel().getModel()
            self.matrix = self.rect.getModelMatrix()

        if self.scaleDelta:
            vecScale = vector.Vector(
                3,
                data=[self.scaleDelta, self.scaleDelta, self.scaleDelta])

            self.matrix.i_scale(vecScale)
            self.scaleDelta = 0

        if self.xPosDelta or self.yPosDelta or self.zPosDelta:
            vecTrans = vector.Vector(
                3,
                data=[self.xPosDelta, self.yPosDelta, self.zPosDelta])

            #self.matrix.i_translate(vecTrans)
            self.matrix.i_translate(vecTrans)
            self.xPosDelta = 0
            self.yPosDelta = 0
            self.zPosDelta = 0

        temp4x4 = self.matrix.inverse().transpose()
        self.modelInverseTranspose = convertM4to3(temp4x4.matrix)