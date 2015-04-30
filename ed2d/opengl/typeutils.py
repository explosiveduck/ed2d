from ed2d.pycompat import *
import ctypes as ct

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def cast_ptr(obj, ptrType):
    return ct.cast(obj, ct.POINTER(ptrType))

def to_c_str(text, hackRef=[], extList=False):
    ''' Convert python strings to null terminated c strings. '''
    # We only want to keep the cString data around for 1 call
    # This is a pretty terrible hack but oh well :(
    if not extList and len(hackRef) != 0:
        hackRef.remove(hackRef[0])
    cStr = ct.create_string_buffer(text.encode(encoding='UTF-8'))
    hackRef.append(cStr)
    return ct.cast(ct.pointer(cStr), ct.POINTER(ct.c_char))

def conv_list(listIn, cType):
    ''' Convert a python list into a ctypes array '''
    return (cType * len(listIn))(*listIn)

def conv_list_2d(listIn, cType):
    ''' Convert a python 2d list into a ctypes 2d array '''
    xlength = len(listIn)
    ylength = len(listIn[0])

    arrayOut = (cType * ylength * xlength)()

    for x in range(xlength):
        for y in range(ylength):
            arrayOut[x][y] = listIn[x][y]

    return arrayOut