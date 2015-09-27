import math

from ed2d.glmath import vector
from ed2d.glmath import matrix

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

        # TO BE IMPLEMENTED
        # Sides of the triangle
        self.A = 0
        self.B = 0
        self.C = 0

    # Reference Real Time Collision Detection by Christer Ericson
    # Calculate the 2D area of a given triangle
    def triArea2D(self, x1, y1, x2, y2, x3, y3):
        return (x1 - x2)*(y2 - y3) - (x2 - x3) * (y1 - y2)

    # Compute barycentric coordinates (u, v, w) for
    # Point P with respect to triangle (a, b, c)
    def barycentric(self, a, b, c, p):
        #Unnormalized triangle normal
        m = (b - a).cross(c - a)

        #Nominators and one-over-denominators for u and v ratios
        nu = 0
        nv = 0
        ood = 0

        # Absolute components for determining projection plane
        x = math.abs(m[0])
        y = math.abs(m[1])
        z = math.abs(m[2])

        if x >= y and x >= z:
            # x is largest, project to the yz plane
            nu = self.triArea2D(p[1], p[2], b[1], b[2], c[1], c[2]) # Area of PBC in yz plane
            nv = self.triArea2D(p[1], p[2], c[1], c[2], a[1], a[2]) # Area of PCA in yz plane
            ood = 1.0 / m[0] # 1 / (2 * area of ABC in yz plane)
        elif y >= x and y >= z:
            # y is largest, project to the xz plane
            nu = self.triArea2D(p[0], p[2], b[0], b[2], c[0], c[2]) # Area of PBC in xz plane
            nv = self.triArea2D(p[0], p[2], c[0], c[2], a[0], a[2]) # Area of PCA in xz plane
            ood = 1.0 / -m[1] # 1 / (2 * area of ABC in xz plane)
        else:
            # z is largest, project to the xy plane
            nu = self.triArea2D(p[0], p[1], b[0], b[1], c[0], c[1]) # Area of PBC in xy plane
            nv = self.triArea2D(p[0], p[1], c[0], c[1], a[0], a[1]) # Area of PCA in xy plane
            ood = 1.0 / m[2]

        # Barycentric coordinates
        u = nu * ood
        v = nv * ood
        w = 1.0 - u - v

        return vector.Vector(3, data=[u, v, w])

    # Test if point p is contained in triangle (a, b, c)
    def testPointTriangle(self, a, b, c, p):
        bV = barycentric(a, b, c, p)
        return (bV[1] >= 0.0) and (bV[2] >= 0.0) and ((bV[1] + bV[2]) <= 1.0)

    def getFurthestPoint(self, direction):
        midBase = vector.Vector(3).right() * self.thirdDims.vector[0]
        midHeight = vector.Vector(3).up() * self.thirdDims.vector[1]

        direction4 = vector.Vector(4, data=[direction.vector[0], direction.vector[1], direction.vector[2], 1.0])

        vertices = []
        vertices.append( self.center.vector[1], midHeight)
        vertices.append( midBase, -midHeight)
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
