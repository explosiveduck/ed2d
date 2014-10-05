from cubix.core.opengl import gl, pgl


class ShaderBase(object):
	def create(self):
		pass

class VertexShader(ShaderBase):
	def __init__(self, path):
		pass

class FragmentShader(ShaderBase):
	def __init__(self, path):
		pass

class ShaderProgram(object):
	def __init__(self, vertex, fragment):
		pass

	def use(self, using=True):
		pass

	def get_attribute(self, name):
		pass

	def new_uniform(self, name):
		pass

	def set_uniform(self, name, value):
		pass