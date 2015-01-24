from cubix.core.glmath import vector
from cubix.core.glmath import matrix

class Circle(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def getFurthestPoint(self, direction):
        if (direction is not vector.Vector(3)):
            direction.i_normalize()
        return self.center + direction + self.radius

class Sphere(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def getFurthestPoint(self, direction):
        if (direction is not vector.Vector(3)):
            direction.i_normalize()
        return self.center + direction + self.radius

class Triangle(object):
    def __init__(self, center, b, h, rotation):
        self.center = center
        self.thirdDims = vector.Vector(3, data=[b / 3.0, h / 3.0, 0.0])
        self.rotation = rotation

    def getFurthestPoint(self, direction):
        midBase = vector.Vector(3).right() * self.thirdDims.vector[0]
        midHeight = vector.Vector(3).up() * self.thirdDims.vector[1]

        direction4 = vector.Vector(4, data=[direction.vector[0], direction.vector[1], direction.vector[2], 1.0])

        vertices = []
        vertices.append( self.center.vector[1], midHeight)
        vertices.append( minBase, -midHeight)
        vertices.append(-midBase, -midHeight)

        translation = matrix.Matrix(4).translate(vector.Vector(4, data=[self.center.vector[0], self.center.vector[1], self.center.vector[2], 1.0]))
        world = self.rotation * translation

        furtherPoint = world * vector.Vector(4, data=[vertices[0].vector[0], vertices[0].vector[1], vertices[0].vector[2], 1.0])

        maxDot = furtherPoint.dot(direction4)
        for i in range(1, 3, 1):
            vertex = world * vector.vector(4, data=[vertices[i].vector[0], vertices[i].vector[1], vertices[i].vector[2], 1.0])
            dot = vertex.dot(direction4)
            if(dot > maxDot):
                maxDot = dot
                furtherPoint = vertex
        return vector.Vector(3, data=[furtherPoint.vector[0], furtherPoint.vector[1], furtherPoint.vector[2]])

class Rectangle(object):
    def __init__(self, center, w, h, rotation):
        self.center = center
        self.halfDims = vector.Vector(3, data=[w / 2.0, h / 2.0, 0.0])
        self.rotation = rotation

    def getFurthestPoint(self, direction):
        halfWidth =  vector.Vector(3).right() * self.halfDims.vector[0]
        halfHeight = vector.Vector(3).up() * self.halfDims.vector[1]

        direction4 = vector.Vector(4, data=[direction.vector[0], direction.vector[1], direction.vector[2], 1.0])

        vertices = []
        vertices.append( halfWidth + halfHeight)
        vertices.append(-halfWidth + halfHeight)
        vertices.append(-halfWidth - halfHeight)
        vertices.append( halfWidth - halfHeight)

        translation = matrix.Matrix(4).translate(vector.Vector(4, data=[self.center.vector[0], self.center.vector[1], self.center.vector[2], 1.0]))
        world = self.rotation * translation

        furtherPoint =  world * vector.Vector(4, data=[vertices[0].vector[0], vertices[0].vector[1], vertices[0].vector[2], 1.0])

        maxDot = furtherPoint.dot(direction4)
        for i in range(1, 4, 1):
            vertex = world * vector.Vector(4, data=[vertices[i].vector[0], vertices[i].vector[1], vertices[i].vector[2], 1.0])
            dot = vertex.dot(direction4)
            if(dot > maxDot):
                maxDot = dot
                furtherPoint = vertex
        return vector.Vector(3, data=[furtherPoint.vector[0], furtherPoint.vector[1], furtherPoint.vector[2]])

class Box(object):
    def __init__(self, center, w, h ,d , rotation):
        self.center = center
        self.halfDims = vector.Vector(3, data=[w / 2.0, h / 2.0, d / 2.0])
        self.rotation = rotation

    def getFurthestPoint(self, direction):
        halfWidth = vector.Vector(3).right() * self.halfDims.vector[0] 
        halfHeight = vector.Vector(3).up() * self.halfDims.vector[1]
        halfDepth = vector.Vector(3).back() * self.halfDims.vector[2]

        direction4 = vector.Vector(4, data=[direction.vector[0], direction.vector[1], direction.vector[2], 1.0])

        vertices = []
        vertices.append(halfWidth + halfHeight + halfDepth)
        vertices.append(-halfWidth + halfHeight + halfDepth)
        vertices.append(halfWidth - halfHeight + halfDepth)
        vertices.append(halfWidth + halfHeight - halfDepth)
        vertices.append(-halfWidth - halfHeight + halfDepth)
        vertices.append(halfWidth - halfHeight - halfDepth)
        vertices.append(-halfWidth + halfHeight - halfDepth)
        vertices.append(-halfWidth - halfHeight - halfDepth)

        translation = matrix.Matrix(4).translate(vector.Vector(4, data=[self.center.vector[0], self.center.vector[1], self.center.vector[2], 1.0]))
        world = self.rotation * translation

        furtherPoint = world * vector.Vector(4, data=[vertices[0].vector[0], vertices[0].vector[1], vertices[0].vector[2], 1.0])

        maxDot = furtherPoint.dot(direction4)
        for i in range(1, 8, 1):
            vertex =  world * vector.Vector(4, data=[vertices[i].vector[0], vertices[i].vector[1], vertices[i].vector[2], 1.0])
            dot = vertex.dot(direction4)
            if(dot > maxDot):
                maxDot = dot
                furtherPoint = vertex
        return vector.Vector(3, data=[furtherPoint.vector[0], furtherPoint.vector[1], furtherPoint.vector[2]])