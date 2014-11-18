import math

from cubix.core.pycompat import *

REFRENCE_VECTOR_2 = [0.0 for x in range(2)]
REFRENCE_VECTOR_3 = [0.0 for x in range(3)]
REFRENCE_VECTOR_4 = [0.0 for x in range(4)]
def zero_vector(size):
    ''' Return a zero filled vector list of the requested size '''
<<<<<<< HEAD
    return [0.0 for x in range(size)]

def one_vector(size):
    ''' Return a one filled vector list of the requested size '''
    return [1.0 for x in range(size)]
=======
    # Return a copy of the reference vector, this is faster than making a new one
    if size == 2:
        return REFRENCE_VECTOR_2[:]
    if size == 3:
        return REFRENCE_VECTOR_3[:]
    if size == 4:
        return REFRENCE_VECTOR_4[:]
>>>>>>> origin/master

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

<<<<<<< HEAD
def refract(IOR, incidentVec, Norm):
    ''' Refract a vector. '''
    dotNI = normal.dot(incidentVec)
    k = 1.0 - IOR * IOR * IOR * (1.0 - dotNI * dotNI)

    if k < 0.0:
        return Vector(len(Norm))
    else:
        scalar = IOR * DOTNI + math.sqrt(k)
        return (IOR * incidentVec) - (scalar * normal)

def vec_add(vecA, vecB):
    size = len(vecA)
    vecOut = zero_vector(size) 
    for i in range(size):
        vecOut[i] = vecA[i] + vecB[i]
    return vecOut
=======
def vec_add(size, vecA, vecB):
    return [(vecA[i] + vecB[i]) for i in range(size)]
>>>>>>> origin/master

def vec_sub(size, vecA, vecB):
    return [(vecA[i] - vecB[i]) for i in range(size)]

def vec_mul(size, vecA, scalar):
    return [(vecA[i] * scalar) for i in range(size)]

def vec_div(size, vecA, vecB):
    return [(vecA[i] / scalar) for i in range(size)]

def vec_neg(size, vecA):
    return [(-vecA[i]) for i in range(size)]

def dot(size, vecA, vecB):
    dp = 0
    for i in range(size):
        dp +=  vecA[i] * vecB[i]
    return dp

def magnitude(size, vecA):
    mg = 0
    for i in range(size):
        mg += vecA[i] * vecA[i]
    return math.sqrt(mg)

def normalize(size, vecA):
    length = magnitude(size, vecA)
    temp = zero_vector(size)
    if length != 0:
        for i in range(size):
            temp[i] = vecA[i] / length
    return temp

def maxV(size, vecA, vecB):
    return [vecA[i] if vecA[i] > vecB[i] else vecB[i] for i in range(size)]

def minV(size, vecA, vecB):
    return [vecA[i] if vecA[i] < vecB[i] else vecB[i] for i in range(size)]

def maxS(size, vecA):
    mScalar = vecA[0]
    for i in range(size):
        if vecA[i] > mScalar:
            mScalar = vecA[i]
    return mScalar

def minS(size, vecA):
    mScalar = vecA[0]
    for i in range(size):
        if vecA[i] < mScalar:
            mScalar = vecA[i]
    return mScalar

class Vector(object):
    def __init__(self, size, data=None):
        self.size = size

        if data is None:
            self.vector = zero_vector(self.size)
        else:
            self.vector = data

    def __add__(self, vecB):
        if isinstance(vecB, Vector):
            vecList = vec_add(self.size, self.vector, vecB.vector)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __iadd__(self, vecB):
        if isinstance(vecB, Vector):
            self.vector = vec_add(self.size, self.vector, vecB.vector)
            return self
        else:
            return NotImplemented

    def __sub__(self, vecB):
        if isinstance(vecB, Vector):
            vecList = vec_sub(self.size, self.vector, vecB.vector)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __isub__(self, vecB):
        if isinstance(vecB, Vector):
            self.vector = vec_sub(self.size, self.vector, vecB.vector)
            return self
        else:
            return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            vecList = vec_mul(self.size, self.vector, scalar)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __imul__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            self.vector = vec_mul(self.size, self.vector, scalar)
            return self
        else:
            return NotImplemented

    def __div__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            vecList = vec_div(self.size, self.vector, scalar)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __idiv__(self, scalar):
        if isinstance(scalar, int) or isinstance(scalar, float):
            self.vector = vec_div(self.size, self.vector, scalar)
            return self
        else:
            return NotImplemented

    def __eq__(self, vecB):
        if isinstance(vecB, Vector):
            tempBool = False
            for i in range(self.size):
                if self.vector[i] == vecB.vector[i]:
                    tempBool = True
                else:
                    tempBool = False
            return tempBool
        else:
            return NotImplemented

    def __neg__(self):
        vecList = vec_neg(self.size, self.vector)
        return Vector(self.size, data=vecList)

    def maxV(self, vecB):
<<<<<<< HEAD
        ''' Return the biggest vector of the two. '''
        if isinstance(vecB, Vector):
            return maxV(self.vector, vecB.vector)
        else:
            return NotImplemented

    def minV(self, vecB):
        ''' Return the smallest vector of the two. '''
        if isinstance(vecB, Vector):
            return maxV(self.vector, vecB.vector)

    def minS(self):
        ''' Return the smallest numeric value of the component of the vector. '''
        return maxS(self.vector)

    def maxS(self):
        ''' Return the biggest numeric value of the component of the vector. '''
        return maxS(self.vector)

    def magnitude(self):
        ''' Return the magnitude of the vector. '''
        return magnitude(self.vector)
=======
        return Vector(self.size, data=maxV(self.size, self.vector, vecB.vector))

    def maxS(self):
        return maxS(self.size, self.vector)

    def minV(self, vecB):
        return Vector(self.size, data=maxV(self.size, self.vector, vecB.vector))

    def minS(self):
        return maxS(self.size, self.vector)

    def magnitude(self):
        return magnitude(self.size, self.vector)
>>>>>>> origin/master

    def i_normalize(self):
        ''' Normalize the vector in place. '''
        self.vector = normalize(self.vector)
        return self

    def normalize(self):
<<<<<<< HEAD
        ''' Return a new normalized vector. '''
        vecList = normalize(self.vector)
=======
        vecList = normalize(self.size, self.vector)
>>>>>>> origin/master
        return Vector(self.size, data=vecList)
        
    def dot(self, vecB):
        ''' Return the dot product between two vectors. '''
        if isinstance(vecB, Vector):
            return dot(self.size, self.vector, vecB)
        else:
            return NotImplemented

    def isInSameDirection(self, otherVec):
        ''' Return a boolean if the input vector if is in the same direction as the one it's compared against. '''
        if isinstance(otherVec, Vector):
            return self.vector.dot(otherVec) > 0
        else:
            return NotImplemented

    def isInOppositeDirection(self, otherVec):
        ''' Return a boolean if the input vector if is in the opposite direction as the one it's compared against. '''
        if isinstance(otherVec, Vector):
            return self.vector.dot(otherVec) < 0
        else:
            return NotImplemented

    # Return common components of the vector as a group
    def xy(self):
        return [self.vector[0], self.vector[1]]

    def yz(self):
        return [self.vector[1], self.vector[2]]

    def xz(self):
        return [self.vector[0], self.vector[2]]

    def xw(self):
        return [self.vector[0], self.vector[3]]

    def yw(self):
        return [self.vector[1], self.vector[3]]

    def zw(self):
        return [self.vector[2], self.vector[3]]

    def xyw(self):
        return [self.vector[0], self.vector[1], self.vector[3]]

    def yzw(self):
        return [self.vector[1], self.vector[2], self.vector[3]]

    def xzw(self):
        return [self.vector[0], self.vector[2], self.vector[3]]

    def xyz(self):
        return [self.vector[0], self.vector[1], self.vector[2]]

    # 3D vector identities
    def right(self):
        return [ 1.0, 0.0, 0.0]

    def left(self):
        return [-1.0, 0.0, 0.0]

    def front(self):
        return [0.0, 0.0, -1.0]

    def back(self):
        return [ 0.0, 0.0, 1.0]

    def up(self):
        return [ 0.0, 1.0, 0.0]

    def down(self):
        return [0.0, -1.0, 0.0]
