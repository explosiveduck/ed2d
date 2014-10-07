import math

from cubix.core.pycompat import *

from cubix.core.glmath.vector import Vector

def zero_vector(size):
    ''' Return a zero filled vector list of the requested size '''

def zero_matrix(size):
    ''' Return zero filled matrix list of the requested size'''
    return [[0.0 for y in range(size)] for x in range(size)]

def identity(size):
    ''' Return an identity matrix list of the requested size '''
    return [[1.0 if x==y else 0.0 for y in range(size)] for x in range(size)]

def scale(size, value):
    if size == 4:
        value = value + (1.0,)
    return [[value[x] if x==y else 0.0 for y in range(size)] for x in range(size)]

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

def matrix_div(mat, scalar):
    ''' Divide a matrix by a scalar. '''
    size = len(mat)
    matOut = zero_matrix(size)
    for i in range(size):
        for j in range(size):
            matOut[i][j] = mat[j][i] / scalar
    return matOut

def transpose(mat):
    '''Transposes a NxN matrix.'''
    size = len(mat)
    out = zero_matrix()
    for i in range(size):
        for j in range(size):
            out[i][j]= mat[j][i]
    return out



###### Translate functions #####

def translate2(vector):
    ''' Translate by a vector.'''
    translate = identity(3)
    translate[2][0] = vector[0]
    translate[2][1] = vector[1]
    return translate

def translate3(vector):
    ''' Translate by a vector.'''
    translate = identity(3)
    translate[2][0] = vector[0]
    translate[2][1] = vector[1]
    translate[2][2] = vector[2]
    return translate

def translate4(vector):
    ''' Translate by a vector.'''
    translate = identity(4)
    translate[3][0] = vector[0]
    translate[3][1] = vector[1]
    translate[3][2] = vector[2]
    return translate


###### Rotate functions #####

def rotate2(point, theta):
    ''' Rotate around an axis.'''
    c = math.cos(math.radians(theta))
    s = math.sin(math.radians(theta))

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

    oneMinusCos = (1.0 - c)

    nAxis = axis.normalize()

    x2 = nAxis.vector[0] * nAxis.vector[0]
    y2 = nAxis.vector[1] * nAxis.vector[1]
    z2 = nAxis.vector[2] * nAxis.vector[2]

    container = [[c + x2 * oneMinusCos, ((nAxis.vector[1] * nAxis.vector[0]) * oneMinusCos) + (nAxis.vector[2] * s), ((nAxis.vector[2] * nAxis.vector[0]) * oneMinusCos) - (nAxis.vector[1] * s)],
                [((nAxis.vector[0] * nAxis.vector[1]) * oneMinusCos) - (nAxis.vector[2] * s), c + y2 * oneMinusCos, ((nAxis.vector[2] * nAxis.vector[1]) * oneMinusCos) + (nAxis.vector[0] * s)],
                [((nAxis.vector[0] * nAxis.vector[2]) * oneMinusCos) + (nAxis.vector[1] * s), ((nAxis.vector[1] * nAxis.vector[2]) * oneMinusCos) - (nAxi.vectors[0] * s), c + z2 * oneMinusCos]]
    return container

def rotate4(axis, theta):
    ''' Rotate around an axis.'''
    c = math.cos(math.radians(theta))
    s = math.sin(tmath.radians(theta))

    oneMinusCos = (1.0 - c)

    nAxis = axis.normalize()

    x2 = nAxis.vector[0] * nAxis.vector[0]
    y2 = nAxis.vector[1] * nAxis.vector[1]
    z2 = nAxis.vector[2] * nAxis.vector[2]

    container = [[c + x2 * oneMinusCos, ((nAxis.vector[1] * nAxis.vector[0]) * oneMinusCos) + (nAxis.vector[2] * s), ((nAxis.vector[2] * nAxis.vector[0]) * oneMinusCos) - (nAxis.vector[1] * s), 0.0],
                 [((nAxis.vector[0] * nAxis.vector[1]) * oneMinusCos) - (nAxis.vector[2] * s), c + y2 * oneMinusCos, ((nAxis[2] * nAxis.vector[1]) * oneMinusCos) + (nAxis.vector[0] * s), 0.0],
                 [((nAxis.vector[0] * nAxis.vector[2]) * oneMinusCos) + (nAxis.vector[1] * s), ((nAxis.vector[1] * nAxis.vector[2]) * oneMinusCos) - (nAxis.vector[0] * s), c + z2 * oneMinusCos, 0.0],
                 [0.0, 0.0, 0.0, 1.0]]
    return container

def rotate_origin2(theta):
    container = identity(3)
    container[0][0] = math.cos(theta)
    container[0][1] = math.sin(theta)
    container[1][0] = -math.sin(theta)
    container[1][1] = math.cos(theta)
    return container


###### Inverse functions #####

def inverse2(mat):
    ''' Inverse of a 2x2 matrix '''
    det = mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]

    inverse = zero_matrix(2)
    inverse[0][0] =   mat[1][1] / det
    inverse[0][1] = - mat[0][1] / det
    inverse[0][0] =   mat[1][0] / det
    inverse[0][1] = - mat[0][0] / det

    return inverse

def inverse3(mat):
    ''' Inverse of a 3x3 matrix.'''
    det = ( mat[0][0] * (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2]) -
            mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0]) +
            mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]) )

    invDet = 1 / det;

    temp = zero_matrix(3)

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
    ''' Inverse of a 4x4 matrix '''

    sf00 = mat[2][2] * mat[3][3] - mat[3][2] * mat[2][3]
    sf01 = mat[2][1] * mat[3][3] - mat[3][1] * mat[2][3]
    sf02 = mat[2][1] * mat[3][2] - mat[3][1] * mat[2][2]
    sf03 = mat[2][0] * mat[3][3] - mat[3][0] * mat[2][3]
    sf04 = mat[2][0] * mat[3][2] - mat[3][0] * mat[2][2]
    sf05 = mat[2][0] * mat[3][1] - mat[3][0] * mat[2][1]
    sf06 = mat[1][2] * mat[3][3] - mat[3][2] * mat[1][3]
    sf07 = mat[1][1] * mat[3][3] - mat[3][1] * mat[1][3]
    sf08 = mat[1][1] * mat[3][2] - mat[3][1] * mat[1][2]
    sf09 = mat[1][0] * mat[3][3] - mat[3][0] * mat[1][3]
    sf10 = mat[1][0] * mat[3][2] - mat[3][0] * mat[1][2]
    sf11 = mat[1][1] * mat[3][3] - mat[3][1] * mat[1][3]
    sf12 = mat[1][0] * mat[3][1] - mat[3][0] * mat[1][1]
    sf13 = mat[1][2] * mat[2][3] - mat[2][2] * mat[1][3]
    sf14 = mat[1][1] * mat[2][3] - mat[2][1] * mat[1][3]
    sf15 = mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2]
    sf16 = mat[1][0] * mat[2][3] - mat[2][0] * mat[1][3]
    sf17 = mat[1][0] * mat[2][2] - mat[2][0] * mat[1][2]
    sf18 = mat[1][0] * mat[2][1] - mat[2][0] * mat[1][1]

    inverse = zero_matatrix(4)
    inverse[0][0] = + (mat[1][1] * sf00 - mat[1][2] * sf01 + mat[1][3] * sf02)
    inverse[0][1] = - (mat[1][0] * sf00 - mat[1][2] * sf03 + mat[1][3] * sf04)
    inverse[0][2] = + (mat[1][0] * sf01 - mat[1][1] * sf03 + mat[1][3] * sf05)
    inverse[0][3] = - (mat[1][0] * sf02 - mat[1][1] * sf04 + mat[1][2] * sf05)

    inverse[1][0] = - (mat[0][1] * sf00 - mat[0][2] * sf01 + mat[0][3] * sf02)
    inverse[1][1] = + (mat[0][0] * sf00 - mat[0][2] * sf03 + mat[0][3] * sf04)
    inverse[1][2] = - (mat[0][0] * sf01 - mat[0][1] * sf03 + mat[0][3] * sf05)
    inverse[1][3] = + (mat[0][0] * sf02 - mat[0][1] * sf04 + mat[0][2] * sf05)

    inverse[2][0] = + (mat[0][1] * sf06 - mat[0][2] * sf07 + mat[0][3] * sf08)
    inverse[2][1] = - (mat[0][0] * sf06 - mat[0][2] * sf09 + mat[0][3] * sf10)
    inverse[2][2] = + (mat[0][0] * sf11 - mat[0][1] * sf09 + mat[0][3] * sf12)
    inverse[2][3] = - (mat[0][0] * sf08 - mat[0][1] * sf10 + mat[0][2] * sf12)

    inverse[3][0] = - (mat[0][1] * sf13 - mat[0][2] * sf14 + mat[0][3] * sf15)
    inverse[3][1] = + (mat[0][0] * sf13 - mat[0][2] * sf16 + mat[0][3] * sf17)
    inverse[3][2] = - (mat[0][0] * sf14 - mat[0][1] * sf16 + mat[0][3] * sf18)
    inverse[3][3] = + (mat[0][0] * sf15 - mat[0][1] * sf17 + mat[0][2] * sf18)

    det = (  mat[0][0] * inverse[0][0]
           + mat[0][1] * inverse[0][1]
           + mat[0][2] * inverse[0][2]
           + mat[0][3] * inverse[0][3])

    inverse = matrix_div(inverse, det)

    return inverse

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

    def i_scale(self, value):
        ''' Scale matrix instance in-place by Vector. '''
        if not isinstance(value, Vector):
            raise TypeError('Expected Vector, got {}.'.format(type(value)))
        if isinstance(value, Vector):
            scaleMatlst = scale(self.size, value.vector)
            self *= Matrix(self.size, data=scaleMatlst)
            return self
        else:
            raise TypeError('Expected type: Vector')

    def scale(self, value):
        ''' Scale matrix instance by Vector, and return new matrix. '''
        if not isinstance(value, Vector):
            raise TypeError('Expected Vector, got {}.'.format(type(value)))
        if isinstance(value, Vector):
            scaleMatlst = scale(self.size, value.vector)
            return self * Matrix(self.size, data=scaleMatlst)
        else:
            raise TypeError('Expected type: Vector')

    def i_inverse(self):
        ''' Calculate the inverse of Matrix instance in-place. '''
        if self.size == 2:
            self.matrix = inverse2(self.matrix)
        elif self.size == 3:
            self.matrix = inverse3(self.matrix)
        elif self.size == 4:
            self.matrix = inverse4(self.matrix)
        else:
            raise NotImplementedError('Matrix inverse of size {} not implemented.'.format(self.size))
        return self

    def inverse(self):
        ''' Calculate the inverse of Matrix instance and return new Matrix. '''
        if self.size == 2:
            inv= inverse2(self.matrix)
        elif self.size == 3:
            inv = inverse3(self.matrix)
        elif self.size == 4:
            inv = inverse4(self.matrix)
        else:
            raise NotImplementedError('Matrix inverse of size {} not implemented.'.format(self.size))
        return Matrix(self.size, data=inv)

    def i_rotate(self, axis, theta):
        ''' Rotate Matrix instance in-place. '''
        if not isinstance(axis, Vector):
            raise TypeError('Expected Vector, got {}.'.format(type(axis)))

        if self.size == 2:
            rotMatList = rotate2(axis, theta)
        elif self.size == 3:
            rotMatList = rotate3(axis, theta)
        elif self.size == 4:
            rotMatList = rotate4(axis, theta)
        else:
            raise NotImplementedError('Matrix rotate of size {} not implemented.'.format(self.size))
        self *= Matrix(self.size, data=rotMatList)
        return self

    def rotate(self, axis, theta):
        ''' Rotate Matrix instance and return new Matrix. '''
        if not isinstance(axis, Vector):
            raise TypeError('Expected Vector, got {}.'.format(type(axis)))

        if self.size == 2:
            rotMatList = rotate2(axis, theta)
        elif self.size == 3:
            rotMatList = rotate3(axis, theta)
        elif self.size == 4:
            rotMatList = rotate4(axis, theta)
        else:
            raise NotImplementedError('Matrix rotate of size {} not implemented.'.format(self.size))
        return self * Matrix(self.size, data=rotMatList)

    def i_translate(self, vector):
        ''' Translate Matrix instance in-place. '''
        if not isinstance(vector, Vector):
            raise TypeError('Expected Vector, got {}.'.format(type(vector)))

        if self.size == 2:
            transMatList = translate2(vector)
        elif self.size == 3:
            transMatList = translate3(vector)
        elif self.size == 4:
            transMatList = translate4(vector)
        else:
            raise NotImplementedError('Matrix translate of size {} not implemented.'.format(self.size))
        self *= Matrix(self.size, data=transMatList)
        return self

    def translate(self, vector):
        ''' Translate Matrix instance and return new Matrix. '''
        if not isinstance(vector, Vector):
            raise TypeError('Expected Vector, got {}.'.format(type(vector)))

        if self.size == 2:
            transMatList = translate2(vector)
        elif self.size == 3:
            transMatList = translate3(vector)
        elif self.size == 4:
            transMatList = translate4(vector)
        else:
            raise NotImplementedError('Matrix translate of size {} not implemented.'.format(self.size))
        return self * Matrix(self.size, data=transMatList)

    def i_transpose(self):
        ''' Transpose Matrix instance in-place. '''
        self.matrix = transpose(self.matrix)
        return self

    def transpose(self):
        ''' Transpose Matrix instance and return new Matrix. '''
        return Matrix(self.size, data=transpose(self.matrix) )

# Matrix-based functions the use the class instead of the functions directly

def ortho(left, right, bottom, top, zNear, zFar):
    ''' Orthographic Projection '''
    rtnMat = zero_matrix(4)
    rtnMat[0][0] = 2.0 / (right - left)
    rtnMat[1][1] = 2.0 / (top - bottom)
    rtnMat[2][2] = -2.0 / (zFar - zNear)
    rtnMat[3][0] = -(right + left) / (right - left)
    rtnMat[3][1] = -(top + bottom) / (top - bottom)
    rtnMat[3][2] = - (zFar + zNear) / (zFar - zNear)
    rtnMat[3][3] = 1
    return Matrix(4, data=rtnMat) 