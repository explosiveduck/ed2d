import math

from cubix.core.pycompat import *

def zero_vector(size):
    ''' Return a zero filled vector list of the requested size '''
    return [0.0 for x in range(size)]
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

def vec_add(vecA, vecB):
    size = len(vecA)
    vecOut = zero_vector(size) 
    for i in range(size):
        vecOut[i] = vecA[i] + vecB[i]
    return vecOut

def vec_sub(vecA, vecB):
    size = len(vecA)
    vecOut = zero_vector(size) 
    for i in range(size):
        vecOut[i] = vecA[i] - vecB[i]
    return vecOut

def vec_mul(vecA, scalar):
    size = len(vecA)
    vecOut = zero_vector(size) 
    for i in range(size):
        vecOut[i] = vecA[i] * scalar
    return vecOut

def vec_div(vecA, vecB):
    size = len(vecA)
    vecOut = zero_vector(size) 
    for i in range(size):
        vecOut[i] = vecA[i] / scalar
    return vecOut

def vec_neg(vecA):
    size = len(vecA)
    vecOut = zero_vector(size) 
    for i in range(size):
        vecOut[i] = -vecA[i]
    return vecOut

def dot(vecA, vecB):
    size = len(vecA)
    dp = 0
    for i in range(size):
        dp +=  vecA[i] * vecB[i]
    return dp

def magnitude(vecA):
    size = len(vecA)
    mg = 0
    for i in range(size):
        mg += vecA[i] * vecA[i]
    return math.sqrt(mg)

def normalize(vecA):
    size = len(vecA)
    length = magnitude(vecA)
    temp = zero_vector(size)
    if length != 0:
        for i in range(size):
            temp[i] = vecA[i] / length
    return temp

class Vector(object):
    def __init__(self, size, data=None):
        self.size = size

        if data is None:
            self.vector = zero_vector(self.size)
        else:
            self.vector = data

    def __add__(self, vecB):
        if isinstance(vecB, Vector):
            vecList = vec_add(self.vector, vecB.vector)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __iadd__(self, vecB):
        if isinstance(vecB, Vector):
            self.vector = vec_add(self.vector, vecB.vector)
            return self
        else:
            return NotImplemented

    def __sub__(self, vecB):
        if isinstance(vecB, Vector):
            vecList = vec_sub(self.vector, vecB.vector)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __isub__(self, vecB):
        if isinstance(vecB, Vector):
            self.vector = vec_sub(self.vector, vecB.vector)
            return self
        else:
            return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            vecList = vec_mul(self.vector, scalar)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __imul__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            self.vector = vec_mul(self.vector, scalar)
            return self
        else:
            return NotImplemented

    def __div__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            vecList = vec_div(self.vector, scalar)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __idiv__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            self.vector = vec_div(self.vector, scalar)
            return self
        else:
            return NotImplemented

    def __neg__(self):
        vecList = vec_neg(self.vector)
        return Vector(self.size, data=vecList)

    def magnitude(self):
        return magnitude(self.vector)

    def i_normalize(self):
        self.vector = normalize(self.vector)
        return self

    def normalize(self):
        vecList = normalize(self.vector)
        return Vector(self.size, data=vecList)
        
    def dot(self, vecB):
        if isinstance(vecB, Vector):
            return dot(self.vector, vecB)
        else:
            return NotImplemented
