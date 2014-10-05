''' Helps ease compatibility issues between python 2 and 3 '''
import sys

PYTHON_3 = sys.version_info.major == 3

if PYTHON_3:
    range = range
    unicode = str
else:
    range = xrange

__all__ = ['PYTHON_3', 'range', 'unicode']