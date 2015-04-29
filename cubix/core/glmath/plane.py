from cubix.core.glmath import vector

class Plane(object):

    def __init__(self):
        self.normal = vector.Vector(3, data=[0.0, 0.0, 0.0])
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

    def clone(self):
        '''Create a new Plane with similar propertise'''
        newPlane = Plane()
        newPlane.normal = self.normal.clone()
        newPlane.a = self.a
        newPlane.b = self.b
        newPlane.c = self.c
        newPlane.d = self.d
        return newPlane

    def flip(self):
        '''Flip the plane.'''
        self.normal = -self.normal
        self.a = -self.a
        self.b = -self.b
        self.c = -self.c
        self.d = -self.d

    def fromCoeffs(self, a, b, c, d):
        '''Create the plane from A,B,C,D.'''
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.normal = vector.cross(b - a, c - a).normalize()

    def fromPoints(self, a, b, c):
        '''Calculate the plane from A,B,C.'''
        self.a = a
        self.b = b
        self.c = c
        self.normal = vector.cross(b - a, c - a).normalize()
        self.d = self.normal.dot(self.a)

    def dot(self, vector):
        return self.a * vector.vector[0] + self.b * vector.vector[1] + self.c * vector.vector[2] + self.d * vector.vector[3]

    def i_normalize(self):
        ''' Return the normalized plane in-place.'''
        vectorData = [self.a, self.b, self.c]
        vectorNorm = vector.Vector(3, data=vectorData).i_normalize()
        vectorLeng = vectorNorm.magnitude()

        if vectorLeng is not 0:
            self.a = vectorNorm.vector[0]
            self.b = vectorNorm.vector[1]
            self.c = vectorNorm.vector[2]
            self.d = self.d / vectorLeng

    def normalize(self):
        ''' Return a new normalized plane.'''
        vectorData = [self.a, self.b, self.c]
        vectorNorm = vector.Vector(3, data=vectorData).i_normalize()
        vectorLeng = vectorNorm.magnitude()

        if vectorLeng is not 0:
            return Plane().fromCoeffs(vectorNorm.vector[0], vectorNorm.vector[1], vectorNorm.vector[2], self.d/vectorLeng)

    def bestFitNormal(self, normalList):
        output = vector.Vector(3).zero()

        for i in range(len(output.size)):
            output.vector[0] += (normalList[i].vector[2] + normalList[i + 1].vector[2]) * (normalList[i].vector[1] - normalList[i + 1].vector[1])
            output.vector[1] += (normalList[i].vector[0] + normalList[i + 1].vector[0]) * (normalList[i].vector[2] - normalList[i + 1].vector[2])
            output.vector[2] += (normalList[i].vector[1] + normalList[i + 1].vector[1]) * (normalList[i].vector[0] - normalList[i + 1].vector[0])

        return output.i_normalize()

    def bestFitD(self, vectorList, bestFitNormal):
        val = 0.0
        for vec in vectorList:
            val += vec.dot(bestFitNormal)
        return val / len(vectorList)

    def point_location(self, point):
        ''' Returns the location of the point. '''
        # If s > 0 then the point is on the same side as the normal. (front)
        # If s < 0 then the point is on the opposide side of the normal. (back)
        # If s = 0 then the point lies on the plane.
        s = self.a * point[0] + self.b * point[1] + self.c * point[2] + self.d

        if s > 0:
            return 1
        elif s < 0:
            return -1
        else:
            return 0