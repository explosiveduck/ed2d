
from ed2d.core.pycompat import *
from ed2d.core import glmath
from ed2d.core.opengl import gl, pgl

def buffer_object(data, type):
    if data or 0:
        vbo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        pgl.glBufferData(gl.GL_ARRAY_BUFFER, data, type, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        return vbo
    else:
        return None

def index_buffer_object(data, type):
    if data or 0:
        ibo = pgl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)
        pgl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, data, type, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        return ibo
    else:
        return None

def bind_object(dataLoc, vbo, size):
    if (dataLoc is not None) and (vbo is not None):
        gl.glEnableVertexAttribArray(dataLoc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        pgl.glVertexAttribPointer(dataLoc, size, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
    else:
        pass

def unbind_object(dataLoc):
    if dataLoc is not None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glDisableVertexAttribArray(dataLoc)
    else:
        pass

class Indexer(object):

    def __init__(self):
        self.unique = []
        self.indices = []
        self.map = {}

    def add(self, obj):
        key = obj.__dict__

        value1 = key['pos']
        value2 = key['normal']

        key['pos'] = value1
        key['normal'] = value2

        key = str(key)

        if not(key in self.map):
            self.map[key] = len(self.unique)
            self.unique.append(obj)

        return self.map[key]

class MeshBase(object):

    def __init__(self):
        self.program = None
        self.vertLoc = None
        self.UVLoc = None
        self.colorLoc = None
        self.modelID = None

    def addProgram(self, program):
        self.program = program
        self.vertLoc = self.program.get_attribute(b'position')
        self.UVLoc = self.program.get_attribute(b'vertexUV')
        self.colorLoc = self.program.get_attribute(b'color')
        self.modelID = self.program.new_uniform(b'model')

    def addTexture(self, texture):
        self.texture = texture

    def render(self):
        
        self.program.set_uniform_matrix(self.modelID, self.modelMatrix)

        if self.texture is not None:
            self.texture.bind()
        else:
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        self.cbo = buffer_object(self.colors, gl.GLfloat)

        bind_object(self.vertLoc, self.vbo, 3)
        bind_object(self.UVLoc, self.uvbo, 3)
        bind_object(self.colorLoc, self.cbo, 3)

        if self.ibo:
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

            gl.glDrawElements(gl.GL_TRIANGLES, self.ntris * 3, gl.GL_UNSIGNED_INT, 0)

            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        else:
            gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.nverts)

        unbind_object(self.colorLoc)
        unbind_object(self.UVLoc)
        unbind_object(self.vertLoc)

    def buffer_objects(self):
        self.vbo = buffer_object(self.data, gl.GLfloat)
        self.uvbo = buffer_object(self.texCoord, gl.GLfloat)
        self.ibo = index_buffer_object(self.triangles, gl.GLuint)

class Mesh(MeshBase):
    def __init__(self):
        super(Mesh, self).__init__()

        self.xPos = 0
        self.yPos = 0
        self.xPosDelta = 0
        self.yPosDelta = 0

        self._scale = 1
        self.scaleDelta = 0

        self.modelMatrix = glmath.Matrix(4)

        self.rect = None
        self.nverts = 0
        self.ntris = 0
        self.data = []
        self.texCoord = []

        self.normals = []
        self.colors = []
        self.triangles = []
        

    def setColorAll(self, r, g, b):
        '''This will populate the colors array with same color for every vertex.'''
        if not self.colors:
            for i in range(self.nverts):
                self.colors.append([r,g,b])
        else:
            for i in range(self.nverts):
                self.colors[i] = [r, g, b]

    def fromData(self, **kwargs):
        ''' This will take in any set of vertices, uv coordinates and colors arrays. '''
        if kwargs is not None:
            for key, value in kwargs.items():
                if key is 'data':
                    self.data = value
                    self.nverts = len(self.data)

                if key is 'texCoord':
                    self.texCoord = value
                else:
                    self.texCoord = self.data

                if key is 'colors':
                    self.colors = value
                else:
                    self.colors = []
        

    def fromCSG(self, csg):
        '''This will take in a CSG object and convert it to mesh for rendering and simulation purposes.'''
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
            self.data.append(v.pos.vector)
            self.normals.append(v.normal.vector)
            self.colors.append(v.color)

        #print("Indexer Unique Count: ", len(indexer.unique))
        #print("Polygon Count: ", len(polygons))
        #print("Triangles Count: ", len(self.triangles))
        #print("Vertices Count: ", len(self.data))

        self.nverts = len(self.data)
        self.ntris = len(self.triangles)

    def setBuffers(self):
        self.buffer_objects()

    def addPhysicsObject(self, physObj):
        '''This will attach a physics object to the mesh.'''
        self.rect = physObj.getCollisionModel().getModel()
        self.data = self.rect.getVertices()
        self.texCoord = self.rect.getVertices()
        self.modelMatrix = self.rect.getModelMatrix()


    def scale(self, value):
        self.scaleDelta = value / self._scale
        self._scale = value

    def translate(self, x, y):
        self.xPosDelta += x - self.xPos
        self.yPosDelta += y - self.yPos
        self.xPos = x
        self.yPos = y

    def update(self, physicsObject=None):

        if physicsObject is None:
            pass
        else:
            self.rect = physicsObject.getCollisionModel().getModel()
            self.modelMatrix = self.rect.getModelMatrix()

        if self.scaleDelta:
            vecScale = glmath.Vector(3, data=[self.scaleDelta, self.scaleDelta, 0.0])

            self.modelMatrix.i_scale(vecScale)
            self.scaleDelta = 0

        if self.xPosDelta or self.yPosDelta:
            vecTrans = glmath.Vector(3, data=[self.xPosDelta, self.yPosDelta, 0.0])
            
            self.modelMatrix.i_translate(vecTrans)
            self.xPosDelta = 0
            self.yPosDelta = 0
        


