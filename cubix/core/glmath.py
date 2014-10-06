import math

from cubix.core.pycompat import *

def zero_vector(size):
    ''' Return a zero filled vector list of the requested size '''

def zero_matrix(size):
    ''' Return zero filled matrix list of the requested size'''
    return [[0.0 for y in range(size)] for x in range(size)]

def identity(size):
    ''' Return an identity matrix list of the requested size '''
    return [[1.0 if x==y else 0.0 for y in range(size)] for x in range(size)]

def matrix_multiply(matrixA, matrixB):
    ''' Multiply matrixA with matrixB '''
    sizeA = len(matrixA)
    matOut = zero_matrix(sizeA)
    for i in range(sizeA):
        for j in range(sizeA):
            for k in range(sizeA):
                matOut[i][j] += matrixA[i][k] * matrixB[k][j]
    return matOut

def matrix_vector_multiply(matrix, vector):
    ''' Multiply matrix with vector '''
    matSize = len(matrix)
    vecSize = len(vector)
    vecOut = zero_vector(vecSize)
    for i in range(matSize):
        for j in range(matSize):
            vecOut[i] += vector[j] * matrix[i][j]
    return vecOut

def ortho(left, right, bottom, top, zNear, zFar):
    rtnMat = zero_matrix(4)
    rtnMat[0][0] = 2.0 / (right - left)
    rtnMat[1][1] = 2.0 / (top - bottom)
    rtnMat[2][2] = -2.0 / (zFar - zNear)
    rtnMat[3][0] = -(right + left) / (right - left)
    rtnMat[3][1] = -(top + bottom) / (top - bottom)
    rtnMat[3][2] = - (zFar + zNear) / (zFar - zNear)
    rtnMat[3][3] = 1
    return Matrix(4, data=rtnMat)

class Vector(object):
    def __init__(self, size, data=None):
        self.size = size

        if data is None:
            self.vector = zero_vector(self.size)
        else:
            self.vector = data

class Matrix(object):
    '''
    Matrix class wrapper.
    All operators are implemented in functions, and this class mainly
    acts as data validation/sorting based on input types.
    '''
    def __init__(self, size, data=None):
        self.size = size

        if data is None:
            self.matrix = identity(self.size)
        else:
            self.matrix = data


    def __mul__(self, other):
        if isinstance(other, Vector):
            result = matrix_vector_multiply(self.matrix, other.vector)
            return Vector(len(result), data=result)

        elif isinstance(other, Matrix):
            if other.size != self.size:
                errText = 'size {}, expected {}'.format(other.size, self.size)
                raise ValueError(errText)
            else:
                result = matrix_multiply(self.matrix, self.other.matrix)
                return Matrix(self.size, data=result)


    def __imul__(self, other):
        if isinstance(other, Matrix):
            if other.size != self.size:
                errText = 'size {}, expected {}'.format(other.size, self.size)
                raise ValueError(errText)
            else:
                self.matrix = matrix_multiply(self.matrix, self.other.matrix)
                return self
        else:
            return NotImplemented
