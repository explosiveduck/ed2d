import sys
import os

def get_path():
    
    path = os.path.realpath(sys.path[0])

    # Later on i am going to need to fix this to check packaged files.
    path = os.sep.join(path.split(os.sep))
    return path

def resolve_path(*location):
    path = get_path()
    location = (path,) + location
    location = os.sep.join(location)
    return location

def read_file(path):
    output = ''
    with open(file, 'r') as f:
        output = f.read()
    return output