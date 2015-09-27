import ctypes as ct

# list to keep refrences to c strings around
_stringRef = []


def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def cast_ptr(obj, ptrType):
    return ct.cast(obj, ct.POINTER(ptrType))


def to_c_str(text, extList=False):
    ''' Convert python strings to null terminated c strings. '''
    global _stringRef
    # We only want to keep the cString data around for 1 call
    if not extList and len(_stringRef) != 0:
        _stringRef.remove(_stringRef[0])
    cStr = ct.create_string_buffer(text.encode(encoding='UTF-8'))
    _stringRef.append(cStr)
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


def list_2d_to_1d(inlist):
    ''' Convert a python 2D list to python 1D list. '''
    sizeX = len(inlist[0])
    sizeY = len(inlist)

    rtnList = [None for x in range(sizeY*sizeX)]

    for x in range(sizeY):
        for y in range(sizeX):
            rtnList[y + x * sizeX] = inlist[x][y]

    return rtnList
