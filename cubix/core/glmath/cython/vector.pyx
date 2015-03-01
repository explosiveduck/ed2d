from libc.stdlib cimport malloc, free
import ctypes as ct

cdef float* list_to_array(int size, object pylist):
    cdef float *rtnArr
    cdef int x

    rtnArr = <float*>malloc(size * sizeof(float))

    if rtnArr == NULL:
        raise MemoryError()

    for x from 0 <= x < size by 1:
        rtnArr[x] = pylist[x]

    return rtnArr

cdef float* zero_vector(int size):
    ''' Return a zero filled vector list of the requested size '''
    cdef float *rtnVec
    cdef int x
    rtnVec = <float*>malloc(size * sizeof(float))

    for x from 0 <= x < size by 1:
        rtnVec[x] = 0.0

    return rtnVec

cdef float* one_vector(int size):
    ''' Return a one filled vector list of the requested size '''
    cdef float *rtnVec
    cdef int x
    rtnVec = <float*>malloc(size * sizeof(float))

    for x from 0 <= x < size by 1:
        rtnVec[x] = 1.0

    return rtnVec

cdef class Vector:
    cdef float *vector
    cdef public int size
    cdef public object c_vector
    def __init__(self, size, c_data=None, data=None):

        self.size = size
        if data:
            self.vector = list_to_array(self.size, data)
            self.c_vector = (ct.c_double * size).from_address(<long>self.vector)
        elif c_data:
            self.c_vector = c_data
            self.vector = <float *><long>ct.addressof(self.c_vector)
        else:
            self.vector = zero_vector(self.size)
            self.c_vector =  (ct.c_double * size).from_address(<long>self.vector)

    def __dealloc__(self):
        free(self.vector)