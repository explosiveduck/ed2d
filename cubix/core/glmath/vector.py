import math

from cubix.core.pycompat import *

# Vector Functions
def lerp(vecA, vecB, time):
    '''Linear interpolation between two vectors.'''
    return (vecA * time) + (vecB * (1.0 - time))

def cross(vecA, vecB):
    ''' Cross product between two 3D vectors, returns a vector.'''
    vecC = Vector(3)
    vecC.vector[0] = vecA.vector[1] * vecB.vector[2] - vecA.vector[2] * vecB.vector[1]
    vecC.vector[1] = vecA.vector[2] * vecB.vector[0] - vecA.vector[0] * vecB.vector[2]
    vecC.vector[2] = vecA.vector[0] * vecB.vector[1] - vecA.vector[1] * vecB.vector[0]
    return vecC

def reflect(incidentVec, norm):
    '''Reflect a vector'''
    return incidentVec - (norm * (2.0 * incidentVec.dot(norm)))

class Vector(object):
    def __init__(self, size, data=None):
        self.size = size

        if data is None:
            self.vector = zero_vector(self.size)
        else:
            self.vector = data

    def __add__(self, vecB):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] + vecB.vector[i]
        return out

    def __iadd__(self, vecB):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] + vecB.vector[i]
        return out

    def __sub__(self, vecB):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] - vecB.vector[i]
        return out

    def __isub__(self, vecB):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] - vecB.vector[i]
        return out

    def __mul__(self, scalar):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] * scalar
        return out

    def __imul__(self, scalar):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] * scalar
        return out

    def __div__(self, scalar):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] / scalar
        return out

    def __idiv__(self, scalar):
        out = Vector(size)
        for i in range(size):
            out[i] = self.vector[i] * scalar
        return out

    def __neg__(self):
        out = Vector(size)
        for i in range(size):
            out[i] = -self.vector[i]
        return out

    def magnitude(self):
        temp = 0
        for i in range(size):
            temp += self.vector[i] * self.vector[i]
        return math.sqrt(temp)

    def normalize(self):
        length = self.magnitude()
        temp = Vector(size)
        if length != 0:
            for i in range(size):
                temp.vector[i] = self.vector[i] / length
        return temp

    def dot(self, vecB):
        temp = 0
        for i in range(size):
            temp +=  self.vector[i] * vecB.vector[i]
        return temp
