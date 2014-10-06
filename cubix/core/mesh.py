class Mesh(object):

	self.program = 0 #program for rendering
	self.vertexL = 0 #vertex uniform location

	self.data = []	 #vertices

	def __init__(self, glProgram):
		self.program = glProgram

	def rectangle(self):
		pass

	def triangle(self):
		pass