import math
from ed2d.glmath import vector
from ed2d.glmath import matrix


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

class Quaternion(object):

    def __init__(self, data=None):

        if data is None:
            self.data = [1.0, 0.0, 0.0, 0.0]
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
