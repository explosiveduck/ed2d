#!python
#cython: cdivision=True, boundscheck=False, wraparound=False

cimport cpython.ref
from libc.stdlib cimport malloc, free
import ctypes as ct

######## Following code is for a reimplementation of the ctypes addressof function
# that way less code gets generated in the execution path when converting to and from
# ctypes objects.
test = 'bob'
cdef extern from "Python.h":
    object PyLong_FromVoidPtr(void *p)


ctypedef tagCDataObject CDataObject

cdef union value:
    char c[16]
    short s
    int i
    long l
    float f
    double d
    long double D

cdef struct tagCDataObject:
    Py_ssize_t ob_refcnt
    cpython.ref.PyTypeObject *ob_type
    char *b_ptr
    int  b_needsfree
    CDataObject *b_base
    Py_ssize_t b_size
    Py_ssize_t b_length
    Py_ssize_t b_index
    cpython.ref.PyObject *b_objects
    value b_value

cdef object addressof(object obj):
    return PyLong_FromVoidPtr((<CDataObject *>obj).b_ptr)

# start of matrix code

cdef float* list_2d_to_array(int sizeX, int sizeY, object pylist):
    cdef float *rtnArr
    cdef int x, y

    rtnArr = <float*>malloc(sizeX * sizeY * sizeof(float))

    if rtnArr == NULL:
        raise MemoryError()

    for x from 0 <= x < sizeX by 1:
        for y from 0 <= y < sizeY by 1:
            rtnArr[y + x * sizeX] = pylist[x][y]

    return rtnArr

cdef float* zero_matrix(int size):
    ''' Return zero filled matrix list of the requested size'''
    cdef float *rtnMat
    cdef int x, y

    rtnMat = <float*>malloc(size * size * sizeof(float))

    if rtnMat == NULL:
        raise MemoryError()
    for x from 0 <= x < size by 1:
        for y from 0 <= y < size by 1:
            rtnMat[y + x * size] = 0.0

    return rtnMat

cdef float* identity(int size):
    ''' Return an identity matrix list of the requested size '''
    cdef float *rtnMat
    cdef int x, y
    rtnMat = <float*>malloc(size * size * sizeof(float))
    if rtnMat == NULL:
        raise MemoryError()

    for x from 0 <= x < size by 1:
        for y from 0 <= y < size by 1:
          rtnMat[y + x * size] = 0.0
            if x==y:
                rtnMat[y + x * size] = 1.0
            else:
                rtnMat[y + x * size] = 0.0

    return rtnMat

cdef float* scale(int size, float *value, int vecSize):
    cdef float *rtnMat
    cdef int x, y

    rtnMat = identity(size)

    for x from 0 <= x < size by 1:
        for y from 0 <= y < size by 1:
            if x == y and x < 3:
                rtnMat[y + x * size] = value[x]
    return rtnMat

cdef float* matrix_multiply(float* matrixA, float* matrixB, int matSize):
    matOut = zero_matrix(matSize)
    cdef int i, j, k

    for i from 0 <= i < matSize by 1:
        for j from 0 <= j < matSize by 1:
            for k from 0 <= k < matSize by 1:
                matOut[j + i * matSize] += matrixA[k + i * matSize] * matrixB[j + k * matSize]
    return matOut


cdef float* translate2(float* vector):
    ''' Translate by a vector.'''
    cdef float* translate
    translate = identity(3)
    translate[4] = vector[0] # element [2][0]
    translate[5] = vector[1] # element [2][1]
    return translate

cdef float* translate3(float* vector):
    ''' Translate by a vector.'''
    cdef float* translate
    translate = identity(3)
    translate[6] = vector[0] # element [2][0]
    translate[7] = vector[1] # element [2][1]
    translate[8] = vector[2] # element [2][2]
    return translate

cdef float* translate4(float* vector):
    ''' Translate by a vector.'''
    cdef float* translate
    translate = identity(4)
    translate[12] = vector[0]  # element [3][0]
    translate[13] = vector[1]  # element [3][1]
    translate[14] = vector[2]  # element [3][2]
    return translate


cdef class Matrix:
    '''
    Matrix class wrapper.
    All operators are implemented in functions, and this class mainly
    acts as data validation/sorting based on input types.
    '''
    cdef float *matrix
    cdef public int size
    cdef public object c_matrix
    def __init__(self, int size, data=None, c_data=None):

        self.size = size
        if data:
            self.matrix = list_2d_to_array(self.size, self.size, data)
            self.c_matrix = (ct.c_float * size * size).from_address(<long>self.matrix)
        elif c_data:
            self.c_matrix = c_data
            self.matrix = <float *><long>addressof(self.c_matrix)
        else:
            self.matrix = identity(self.size)
            self.c_matrix = (ct.c_float * size * size).from_address(<long>self.matrix)

    def __mul__(self, other):
        return self._mul(other)

    def _mul(self, other):
        cdef float *result

        result = matrix_multiply(self.matrix, <float *><long>addressof(other.c_matrix), self.size)
        c_result = (ct.c_float * self.size * self.size).from_address(<long>result)
        return Matrix(self.size, c_data=c_result)

    def __imul__(self, other):
        cdef float *result

        result = matrix_multiply(self.matrix, <float *><long>addressof(other.c_matrix), self.size)
        free(self.matrix)
        self.matrix = result
        self.c_matrix = (ct.c_float * self.size * self.size).from_address(<long>self.matrix)
        return self


    def i_scale(self, value):
        ''' Scale matrix instance in-place by Vector. '''
        cdef float *result
        result = scale(self.size, <float *><long>addressof(value.c_vector), value.size)
        c_result = (ct.c_float * self.size * self.size).from_address(<long>result)
        self *= Matrix(self.size, c_data=c_result)
        return self

    def scale(self, value):
        ''' Scale matrix instance by Vector, and return new matrix. '''
        cdef float *result
        result = scale(self.size, <float *><long>addressof(value.c_vector), value.size)
        c_result = (ct.c_float * self.size * self.size).from_address(<long>result)
        return self * Matrix(self.size, c_data=c_result)

    def i_translate(self, vecA):
        ''' Translate Matrix instance in-place. '''
        cdef float *vector
        cdef float *transMatList

        vector = <float *><long>addressof(self.c_matrix)

        if self.size == 2:
            transMatList = translate2(vector)
        elif self.size == 3:
            transMatList = translate3(vector)
        elif self.size == 4:
            transMatList = translate4(vector)

        c_result = (ct.c_float * self.size * self.size).from_address(<long>transMatList)

        self *= Matrix(self.size, c_data=c_result)
        return self

    def translate(self, vecA):
        ''' Translate Matrix instance and return new Matrix. '''
        cdef float *vector
        cdef float *transMatList

        vector = <float *><long>addressof(vecA.c_vector)

        if self.size == 2:
            transMatList = translate2(vector)
        elif self.size == 3:
            transMatList = translate3(vector)
        elif self.size == 4:
            transMatList = translate4(vector)

        c_result = (ct.c_float * self.size * self.size).from_address(<long>transMatList)

        return self * Matrix(self.size, c_data=c_result)

    def __dealloc__(self):
        free(self.matrix)
