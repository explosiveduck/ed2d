import math

from ed2d.pycompat import *

REFRENCE_VECTOR_2 = [0.0 for x in range(2)]
REFRENCE_VECTOR_3 = [0.0 for x in range(3)]
REFRENCE_VECTOR_4 = [0.0 for x in range(4)]

def zero_vector(size):
    ''' Return a zero filled vector list of the requested size '''
    # Return a copy of the reference vector, this is faster than making a new one
    if size == 2:
        return REFRENCE_VECTOR_2[:]
    if size == 3:
        return REFRENCE_VECTOR_3[:]
    if size == 4:
        return REFRENCE_VECTOR_4[:]
    else:
        return [0.0 for x in range(size)]

IREFRENCE_VECTOR_2 = [1.0 for x in range(2)]
IREFRENCE_VECTOR_3 = [1.0 for x in range(3)]
IREFRENCE_VECTOR_4 = [1.0 for x in range(4)]

def one_vector(size):
    ''' Return a one filled vector list of the requested size '''
    # Return a copy of the reference vector, this is faster than making a new one
    if size == 2:
        return IREFRENCE_VECTOR_2[:]
    if size == 3:
        return IREFRENCE_VECTOR_3[:]
    if size == 4:
        return IREFRENCE_VECTOR_4[:]
    else:
        return [1.0 for x in range(size)]

# Vector Functions
def lerp(vecA, vecB, time):
    '''Linear interpolation between two vectors.'''
    #Note: The commented out part is the precise version of linear interpolation
    #return (vecA * time) + (vecB * (1.0 - time))
    return vecA + ((vecB - vecA) * time)

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

def refract(IOR, incidentVec, Norm):
    ''' Refract a vector. '''
    dotNI = normal.dot(incidentVec)
    k = 1.0 - IOR * IOR * IOR * (1.0 - dotNI * dotNI)

    if k < 0.0:
        return Vector(len(Norm))
    else:
        scalar = IOR * DOTNI + math.sqrt(k)
        return (IOR * incidentVec) - (scalar * normal)

def vec_add(size, vecA, vecB):
    return [(vecA[i] + vecB[i]) for i in range(size)]

def s_vec_add(size, vecA, scalar):
    return [(vecA[i] + scalar) for i in range(size)]

def vec_sub(size, vecA, vecB):
    return [(vecA[i] - vecB[i]) for i in range(size)]

def s_vec_sub(size, vecA, scalar):
    return [(vecA[i] - scalar) for i in range(size)]

def vec_mul(size, vecA, scalar):
    return [(vecA[i] * scalar) for i in range(size)]

def vec_div(size, vecA, scalar):
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

def clamp(size, value, min, max):
    output = value
    for i in range(size):
        # Check to see if greater than max
        output[i] = max[i] if output[i] > max[i] else output[i]
        #output[i] = (output[i] > max[i]) ? max[i] : output[i]
        # Check to see is less than min
        output[i] = min[i] if output[i] < min[i] else output[i]
        #output[i] = (output[i] < min[i]) ? min[i] : output[i]
    return output

def transform(size, position, matrix):
    output = zero_vector(size)
    for i in range(size):
        for j in range(size):
            output[i] += position[j] * matrix[i][j]
        output[i] += matrix[size-1][i]

    return output

class Vector(object):
    def __init__(self, size, data=None):
        self.size = size

        if data is None:
            self.vector = zero_vector(self.size)
        else:
            self.vector = data

    def __rerpr__(self):
        return 'Vector: size:{} , data:{}'.format(self.size, self.vector)

    def __add__(self, other):
        if isinstance(other, Vector):
            vecList = vec_add(self.size, self.vector, other.vector)
            return Vector(self.size, data=vecList)
        elif isinstance(other, int) or isinstance(other, float):
            vecList = s_vec_add(self.size, self.vector, other)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.vector = vec_add(self.size, self.vector, other.vector)
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.vector = s_vec_add(self.size, self.vector, other)
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            vecList = vec_sub(self.size, self.vector, other.vector)
            return Vector(self.size, data=vecList)
        elif isinstance(other, int) or isinstance(other, float):
            vecList = s_vec_sub(self.size, self.vector, other)
            return Vector(self.size, data=vecList)
        else:
            return NotImplemented

    def __isub__(self, vecB):
        if isinstance(other, Vector):
            self.vector = vec_sub(self.size, self.vector, other.vector)
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.vector = s_vec_sub(self.size, self.vector, other)
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

    def clone(self):
        return Vector(self.size, data=self.vector)

    def one(self):
        self.vector = one_vector(self.size)
        return self

    def zero(self):
        self.vector = zero_vector(self.size)
        return self

    def clone(self):
        return Vector(self.size, data=self.vector)

    def negate(self):
        vecList = vec_neg(self.size, self.vector)
        return Vector(self.size, data=vecList)

    def maxV(self, vecB):
        return Vector(self.size, data=maxV(self.size, self.vector, vecB.vector))

    def maxS(self):
        return maxS(self.size, self.vector)

    def minV(self, vecB):
        return Vector(self.size, data=minV(self.size, self.vector, vecB.vector))

    def minS(self):
        return minS(self.size, self.vector)

    def magnitude(self):
        return magnitude(self.size, self.vector)

    def clamp(self, value, min, max):
        ''' Returns a new clamped vector. '''
        return clamp(value, min, max)

    def i_clamp(self, value, min, max):
        ''' Clamp the vector into place. '''
        self.vector = clamp(value, min, max).Vector
        return self

    def i_normalize(self):
        ''' Normalize the vector in place. '''
        self.vector = normalize(self.size, self.vector)
        return self

    def normalize(self):
        ''' Return a new normalized vector. '''
        vecList = normalize(self.size, self.vector)
        return Vector(self.size, data=vecList)
        
    def dot(self, vecB):
        ''' Return the dot product between two vectors. '''
        if isinstance(vecB, Vector):
            return dot(self.size, self.vector, vecB.vector)
        else:
            return NotImplemented

    def isInSameDirection(self, otherVec):
        ''' Return a boolean if the input vector if is in the same direction as the one it's compared against. '''
        if isinstance(otherVec, Vector):
            return self.dot(otherVec) > 0
        else:
            return NotImplemented

    def isInOppositeDirection(self, otherVec):
        ''' Return a boolean if the input vector if is in the opposite direction as the one it's compared against. '''
        if isinstance(otherVec, Vector):
            return self.dot(otherVec) < 0
        else:
            return NotImplemented

    def transform(self, position, matrix):
        ''' Transform the vector via a matrix and returns a new vector. '''
        vecList = transform(self.size, position, matrix)
        return Vector(self.size, data=vecList)

    def i_transform(self, position, matrix):
        ''' Transform the vector via a matrix in place. '''
        self.vector = transform(self.size, position, matrix)
        return self

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
        return Vector(3, data=[ 1.0, 0.0, 0.0, 1.0])

    def left(self):
        return Vector(3, data=[-1.0, 0.0, 0.0, 1.0])

    def front(self):
        return Vector(3, data=[0.0, 0.0, -1.0, 1.0])

    def back(self):
        return Vector(3, data=[ 0.0, 0.0, 1.0, 1.0])

    def up(self):
        return Vector(3, data=[ 0.0, 1.0, 0.0, 1.0])

    def down(self):
        return Vector(3, data=[0.0, -1.0, 0.0, 1.0])
