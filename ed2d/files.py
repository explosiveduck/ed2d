import sys
import os


def get_path():
    ''' get the current path '''
    path0 = os.path.realpath(sys.path[0])
    path1 = os.path.realpath(sys.path[1])

    pathtest = os.sep.join(path0.split(os.sep)[:-1])

    if pathtest == path1:
        return path1
    else:
        return path0

_originPath = get_path()

def resolve_path(*location):
    '''Resolve path relative to current path.'''
    return os.sep.join((_originPath,) + location)


def read_file(path):
    '''Read file and return string'''
    output = ''
    with open(path, 'r') as f:
        output = f.read()
    return output
