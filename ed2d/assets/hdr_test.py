import math
import struct
import re
from operator import itemgetter
from ed2d import files

#Flags and constants
RGBE_VALID_PROGRAMTYPE = 0x01
RGBE_VALID_GAMMA = 0x02
RGBE_VALID_EXPOSURE = 0x04

RGBE_RETURN_SUCESS = 0
RGBE_RETURN_FAILURE = 1

RGBE_DATA_RED = 0
RGBE_DATA_GREEN = 1
RGBE_DATA_BLUE = 2
RGBE_DATA_SIZE = 3

class HDRHeader(object):
	def __init__(self):
		self.valid = None
		self.programType = None
		self.gamma = 1.0
		self.exposure = 1.0

def rgbe2float(rgbe):
	f = 0.0
	red = green = blue = 0.0

	if rgbe[3] is not None:
		f = math.ldexp(1.0, rgbe[3] - (128 + 8))
		red = rgbe[0] * f
		green = rgbe[1] * f
		blue = rgbe[2] * f
	else:
		red = green = blue = 0.0

	return red, green, blue

# Return header, width, height
def RGBE_ReadHeader(FILE):
	pass

# Return Data
def RGBE_ReadPixels(FILE, numpixels):
	pass

# Return Data
def RGBE_ReadPixels_RLE(FILE, scanline_width, num_scanlines):
	pass