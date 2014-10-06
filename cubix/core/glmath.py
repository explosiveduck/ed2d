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

def transpose(mat):
    '''Transposes a NxN matrix.'''
    size = len(mat)
    out = [[0.0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            out[i][j]= mat[j][i]
    return out

def scale2(val):
    ''' Scale the matrix by a value.'''
    scale = [[val[0], 0.0],
             [0.0, val[1]]]
    return scale

def scale3(val):
    ''' Scale the matrix by a value.'''
    scale = [[val[0], 0.0, 0.0],
             [0.0, val[1], 0.0],
             [0.0, 0.0, val[2]]]
    return scale

def scale4(val):
    ''' Scale the matrix by a value.'''
    scale = [[val[0], 0.0, 0.0, 0.0],
             [0.0, val[1], 0.0, 0.0],
             [0.0, 0.0, val[2], 0.0],
             [0.0, 0.0, 0.0, 1.0]]
    return scale

def translate2(vector):
    ''' Translate by a vector.'''
    translate = [[1.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [vector.vector[0], vector.vector[1], 1.0]]

def translate4(vector):
    ''' Translate by a vector.'''
    translate = [[1.0, 0.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0, 0.0],
                 [0.0, 0.0, 1.0, 0.0],
                 [vector.vector[0], vector.vector[1], vector.vector[2], 1.0]]
    return translate

def translate3(vector):
    ''' Translate by a vector.'''
    translate = [[1.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [vector.vector[0], vector.vector[1], vector.vector[2]]]
    return translate

def rotate_origin2(theta):
    container = [[math.cos(theta), math.sin(theta), 0.0],
                 [-math.sin(theta), math.cos(theta), 0.0],
                 [0.0, 0.0, 1.0]]
    return container

def rotate2(point, theta):
    c = math.cos(theta)
    s = math.sin(theta)

    x1 = (point[0] - c) * (point[0]) - (-s * point[1])
    y1 = (point[1] - s) * (point[0]) - ( c * point[1])

    container = [[c, s, 0.0],
                 [-s, c, 0.0],
                 [x1, y1, 1.0]]

    return container

def rotate3(axis, theta):
    ''' Rotate around an axis.'''
    c = math.cos(math.radians(theta))
    s = math.sin(math.radians(theta))

    OneMinusCos = (1.0 - c)

    nAxis = axis.normalize()

    x2 = nAxis.vector[0] * nAxis.vector[0]
    y2 = nAxis.vector[1] * nAxis.vector[1]
    z2 = nAxis.vector[2] * nAxis.vector[2]

    container = [[c + x2 * OneMinusCos, ((nAxis.vector[1] * nAxis.vector[0]) * OneMinusCos) + (nAxis.vector[2] * s), ((nAxis.vector[2] * nAxis.vector[0]) * OneMinusCos) - (nAxis.vector[1] * s)],
                [((nAxis.vector[0] * nAxis.vector[1]) * OneMinusCos) - (nAxis.vector[2] * s), c + y2 * OneMinusCos, ((nAxis.vector[2] * nAxis.vector[1]) * OneMinusCos) + (nAxis.vector[0] * s)],
                [((nAxis.vector[0] * nAxis.vector[2]) * OneMinusCos) + (nAxis.vector[1] * s), ((nAxis.vector[1] * nAxis.vector[2]) * OneMinusCos) - (nAxi.vectors[0] * s), c + z2 * OneMinusCos]]
    return container

def rotate4(axis, theta):
    ''' Rotate around an axis.'''
    c = math.cos(theta*(PI/180))
    s = math.sin(theta*(PI/180))

    OneMinusCos = (1.0 - c)

    nAxis = axis.normalize()

    x2 = nAxis.vector[0] * nAxis.vector[0]
    y2 = nAxis.vector[1] * nAxis.vector[1]
    z2 = nAxis.vector[2] * nAxis.vector[2]

    container = [[c + x2 * OneMinusCos, ((nAxis.vector[1] * nAxis.vector[0]) * OneMinusCos) + (nAxis.vector[2] * s), ((nAxis.vector[2] * nAxis.vector[0]) * OneMinusCos) - (nAxis.vector[1] * s), 0.0],
                 [((nAxis.vector[0] * nAxis.vector[1]) * OneMinusCos) - (nAxis.vector[2] * s), c + y2 * OneMinusCos, ((nAxis[2] * nAxis.vector[1]) * OneMinusCos) + (nAxis.vector[0] * s), 0.0],
                 [((nAxis.vector[0] * nAxis.vector[2]) * OneMinusCos) + (nAxis.vector[1] * s), ((nAxis.vector[1] * nAxis.vector[2]) * OneMinusCos) - (nAxis.vector[0] * s), c + z2 * OneMinusCos, 0.0],
                 [0.0, 0.0, 0.0, 1.0]]
    return container

def ortho(left, right, bottom, top, zNear, zFar):
    ''' Orthographic Projection'''
    rtnMat = zero_matrix(4)
    rtnMat[0][0] = 2.0 / (right - left)
    rtnMat[1][1] = 2.0 / (top - bottom)
    rtnMat[2][2] = -2.0 / (zFar - zNear)
    rtnMat[3][0] = -(right + left) / (right - left)
    rtnMat[3][1] = -(top + bottom) / (top - bottom)
    rtnMat[3][2] = - (zFar + zNear) / (zFar - zNear)
    rtnMat[3][3] = 1
    return Matrix(4, data=rtnMat)

def inverse3(mat):
    ''' Inverse of a 3x3 matrix.'''
    det = mat[0][0] * (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2]) - 
          mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0]) +
          mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0])

    invDet = 1 /det;

    temp = Matrix(3)

    temp[0][0] = (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2]) * invDet
    temp[0][1] = (mat[0][2] * mat[2][1] - mat[0][1] * mat[2][2]) * invDet
    temp[0][2] = (mat[0][1] * mat[1][2] - mat[0][2] * mat[1][1]) * invDet
    temp[1][0] = (mat[1][2] * mat[2][0] - mat[1][0] * mat[2][2]) * invDet
    temp[1][1] = (mat[0][0] * mat[2][2] - mat[0][2] * mat[2][0]) * invDet
    temp[1][2] = (mat[1][0] * mat[0][2] - mat[0][0] * mat[1][2]) * invDet
    temp[2][0] = (mat[1][0] * mat[2][1] - mat[2][0] * mat[1][1]) * invDet
    temp[2][1] = (mat[2][0] * mat[0][1] - mat[0][0] * mat[2][1]) * invDet
    temp[2][2] = (mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]) * invDet

    return temp

def inverse4(mat):
    ''' Inverse of a 4x4 matrix.'''
    Coef00 = mat[2][2] * mat[3][3] - mat[3][2] * mat[2][3]
    Coef02 = mat[1][2] * mat[3][3] - mat[3][2] * mat[1][3]
    Coef03 = mat[1][2] * mat[2][3] - mat[2][2] * mat[1][3]

    Coef04 = mat[2][1] * mat[3][3] - mat[3][1] * mat[2][3]
    Coef06 = mat[1][1] * mat[3][3] - mat[3][1] * mat[1][3]
    Coef07 = mat[1][1] * mat[2][3] - mat[2][1] * mat[1][3]

    Coef08 = mat[2][1] * mat[3][2] - mat[3][1] * mat[2][2]
    Coef10 = mat[1][1] * mat[3][2] - mat[3][1] * mat[1][2]
    Coef11 = mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2]

    Coef12 = mat[2][0] * mat[3][3] - mat[3][0] * mat[2][3]
    Coef14 = mat[1][0] * mat[3][3] - mat[3][0] * mat[1][3]
    Coef15 = mat[1][0] * mat[2][3] - mat[2][0] * mat[1][3]

    Coef16 = mat[2][0] * mat[3][2] - mat[3][0] * mat[2][2]
    Coef18 = mat[1][0] * mat[3][2] - mat[3][0] * mat[1][2]
    Coef19 = mat[1][0] * mat[2][2] - mat[2][0] * mat[1][2]

    Coef20 = mat[2][0] * mat[3][1] - mat[3][0] * mat[2][1]
    Coef22 = mat[1][0] * mat[3][1] - mat[3][0] * mat[1][1]
    Coef23 = mat[1][0] * mat[2][1] - mat[2][0] * mat[1][1]

    SignA = [+1, -1, +1, -1]
    SignB = [-1, +1, -1, +1]

    Fac0 = [Coef00, Coef00, Coef02, Coef03]
    Fac1 = [Coef04, Coef04, Coef06, Coef07]
    Fac2 = [Coef08, Coef08, Coef10, Coef11]
    Fac3 = [Coef12, Coef12, Coef14, Coef15]
    Fac4 = [Coef16, Coef16, Coef18, Coef19]
    Fac5 = [Coef20, Coef20, Coef22, Coef23]

    Vec0 = [mat[1][0], mat[0][0], mat[0][0], mat[0][0]]
    Vec1 = [mat[1][1], mat[0][1], mat[0][1], mat[0][1]]
    Vec2 = [mat[1][2], mat[0][2], mat[0][2], mat[0][2]]
    Vec3 = [mat[1][3], mat[0][3], mat[0][3], mat[0][3]]

    Inv0 = mulV4(SignA, add( sub( mulV4( Vec1, Fac0), mulV4( Vec2, Fac1)), mulV4( Vec3, Fac2)))
    Inv1 = mulV4(SignB, add( sub( mulV4( Vec0, Fac0), mulV4( Vec2, Fac3)), mulV4( Vec3, Fac4)))
    Inv2 = mulV4(SignA, add( sub( mulV4( Vec0, Fac1), mulV4( Vec1, Fac3)), mulV4( Vec3, Fac5)))
    Inv3 = mulV4(SignB, add( sub( mulV4( Vec0, Fac2), mulV4( Vec1, Fac4)), mulV4( Vec2, Fac5)))

    Inverse = [Inv0, Inv1, Inv2, Inv3]

    Row0 = [Inverse[0][0], Inverse[1][0], Inverse[2][0], Inverse[3][0]]

    Determinant = dot(mat[0], Row0)

    return m.div(Inverse, Determinant)

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
