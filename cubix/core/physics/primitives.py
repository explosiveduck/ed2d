from cubix.core.glmath import vector
from cubix.core.glmath import matrix

class Circle(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def getFurthestPoint(self, direction):
        if (direction is not self.Vector(3)):
            direction.i_normalize()
        return self.center + self.radius + direction

class Sphere(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def getFurthestPoint(self, direction):
        if (direction is not self.Vector(3)):
            direction.i_normalize()
        return self.center + self.radius + direction

class Rectangle(object):
    def __init__(self, center, w, h, rotation):
        self.center = center
        self.halfDims = vector.Vector(3, data=[w / 2.0, h / 2.0, 1.0])
        self.rotation = rotation

    def getFurtherPoint(self, direction):
        halfWidth = self.halfDims.vec[0] * vector.Vector(3).right()
        halfHeight = self.halfDims.vec[1] * vector.Vector(3).up()

        vertices = []
        vertices.appened( halfWidth + halfHeight)
        vertices.appened(-halfWidth + halfHeight)
        vertices.appened( halfWidth - halfHeight)
        vertices.appened( halfWidht + halfHeight)

        translation = matrix.Matrix(4).translate(self.center)
        world = self.rotation * translation

        furtherPoint = vertices[0] * world
        maxDot = vector.dot(furtherPoint, self.direction)
        for i in range(1, 4, 1):
            vertex = vertices[i] * world
            dot = vector.dot(vertex, self.direction)
            if(dot > maxDot):
                maxDot = dot
                furtherPoint = vertex
        return furtherPoint

class Box(object):
    def __init__(self, center, w, h ,d , rotation):
        self.center = center
        self.halfDims = vector.Vector(3, data=[w / 2.0, h / 2.0, d / 2.0])
        self.rotation = rotation

    def getFurtherPoint(self, direction):
        halfWidth = self.halfDims.vec[0] * vector.Vector(3).right()
        helfHeight = self.halfDims.vec[1] * vector.Vector(3).up()
        halfDepth = self.halfDims.vec[2] * vector.Vector(3).back()

        vertices = []
        vertices.appened(halfWidth + halfHeight + halfDepth)
        vertices.appened(-halfWidth + halfHeight + halfDepth)
        vertices.appened(halfWidth - halfHeight + halfDepth)
        vertices.appened(halfWidth + halfHeight - halfDepth)
        vertices.appened(-halfWidth - halfHeight + halfDepth)
        vertices.appened(halfWidth - halfHeight - halfDepth)
        vertices.appened(-halfWidth + halfHeight - halfDepth)
        vertices.appened(-halfWidht - halfHeight - halfDepth)

        translation = matrix.Matrix(4).translate(self.center)
        world = self.rotation * translation

        furtherPoint = vertices[0] * world
        maxDot = vector.dot(furtherPoint, self.direction)
        for i in range(1, 8, 1):
            vertex = vertices[i] * world
            dot = vector.dot(vertex, self.direction)
            if(dot > maxDot):
                maxDot = dot
                furtherPoint = vertex
        return furtherPoint