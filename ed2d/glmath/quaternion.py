import math
from ed2d.glmath import vector
from ed2d.glmath import matrix

def quat_identity():
    ''' Returns the quaternion identity. '''
    return [1.0, 0.0, 0.0, 0.0]

def quat_add(quat, quat1):
    ''' Add two quaternions. '''
    return [quat[0] + quat1[0], quat[1] + quat1[1], quat[2] + quat1[2], quat[3] + quat1[3]]

def quat_sub(quat, quat1):
    ''' Subtract two quaternions. '''
    return [quat[0] - quat1[0], quat[1] - quat1[1], quat[2] - quat1[2], quat[3] - quat1[3]]

def quat_mul_quat(quat, quat1):
    ''' Multiply a quaternion with a quaternion. '''
    w = quat[0] * quat1[0] - quat[1] * quat1[1] - quat[2] * quat1[2] - quat[3] * quat1[3]
    x = quat[0] * quat1[1] + quat[1] * quat1[0] + quat[2] * quat1[3] - quat[3] * quat1[2]
    y = quat[0] * quat1[2] + quat[2] * quat1[0] + quat[3] * quat1[1] - quat[1] * quat1[3]
    z = quat[0] * quat1[3] + quat[3] * quat1[0] + quat[1] * quat1[2] - quat[2] * quat1[1]
    return [w, x, y, z]

def quat_mul_vect(quat, vect):
    ''' Multiply a quaternion with a vector. '''
    w = -quat[1] * vect[0] - quat[2] * vect[1] - quat[3] * vect[2]
    x =  quat[0] * vect[0] + quat[2] * vect[2] - quat[3] * vect[1]
    y =  quat[0] * vect[1] + quat[3] * vect[0] - quat[1] * vect[2]
    z =  quat[0] * vect[2] + quat[1] * vect[1] - quat[2] * vect[0]
    return [w, x, y, z]

def quat_mul_float(quat, scalar):
    ''' Multiply a quaternion with a scalar (float). '''
    return [quat[0] * scalar, quat[1] * scalar, quat[2] * scalar, quat[3] * scalar]

def quat_div_float(quat, scalar):
    ''' Divide a quaternion with a scalar (float). '''
    return [quat[0] / scalar, quat[1] / scalar, quat[2] / scalar, quat[3] / scalar]

def quat_neg(quat):
    ''' Negate the elements of a quaternion. '''
    return [-quat[0], -quat[1], -quat[2], -quat[3]]

def quat_dot(quat1, quat2):
    ''' Dot product between two quaternions. Returns a scalar. '''
    rdp= 0
    for i in range(4):
        rdp += quat1[i] * quat2[i]
    return rdp

def quat_magnitude(quat):
    ''' Compute magnitude of a quaternion. Returns a scalar. '''
    rmg = 0
    for i in range(4):
        rmg += quat[i] * quat[i]
    return math.sqrt(rmg)

def quat_normalize(quat):
    ''' Returns a normalized quaternion. '''
    length = quat_magnitude(quat)
    oquat = quat_identity()
    if length is not 0:
        for i in range(4):
            oquat[i] = quat[i] / length
    return oquat

def quat_conjugate(quat):
    ''' Returns the conjugate of a quaternion. '''
    idquat = quat_identity()
    for i in range(4):
        idquat[i] = -quat[i]
    idquat[0] = -idquat[0]
    return idquat


class Quaternion(object):

    def __init__(self, data=None):

        if data is None:
            self.data = quat_identity()
        else:
            self.data = data

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(quat_add(self.data, other.data))
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Quaternion):
            self.data = quat_add(self.data, other.data)
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(quat_sub(self.data, other.data))
        else:
            return NotImplemented

    def __isub__(self, other):
        if isinstance(other, Quaternion):
            self.data = quat_sub(self.data, other.data)
            return self
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(quat_mul_quat(self.data, other.data))
        elif isinstance(other, vector.Vector):
            return Quaternion(quat_mul_vect(self.data, other.data))
        elif isinstance(other, float):
            return Quaternion(quat_mul_float(self.data, other))
        else:
            return NotImplemented

    def __imul__(self, other):
        if isinstance(other, Quaternion):
            self.data = quat_mul_quat(self.data, other.data)
            return self
        elif isinstance(other, vector.Vector):
            self.data = quat_mul_vect(self.data, other.data)
            return self
        elif isinstance(other, float):
            self.data = quat_mul_float(self.data, other)
            return self
        else:
            return NotImplemented

    def __div__(self, other):
        if isinstance(other, float):
            return Quaternion(quat_div_float(self.data, other))
        else:
            return NotImplemented

    def __idiv__(self, other):
        if isinstance(other, float):
            self.data = quat_div_float(self.data, other)
            return self
        else:
            return NotImplemented

    def i_negate(self):
        self.data = quat_neg(self.data)
        return self

    def negate(self):
        quatList = quat_neg(self.data)
        return Quaternion(quatList)

    def i_identity(self):
        self.data = quat_identity()
        return self

    def identity(self):
        quatList = quat_identity()
        return Quaternion(quatList)

    def magnitude(self):
        return quat_magnitude(self.data)

    def dot(self, quat2):
        if isinstance(quat2, Quaternion):
            return quat_dot(self.data, quat2.data)
        else:
            return NotImplemented

    def i_normalize(self):
        self.data = quat_normalize(self.data)
        return self

    def normalize(self):
        quatList = quat_normalize(self.data)
        return Quaternion(quatList)

    def i_conjugate(self):
        self.data = quat_conjugate(self.data)
        return self

    def conjugate(self):
        quatList = quat_conjugate(self.data)
        return Quaternion(quatList)

