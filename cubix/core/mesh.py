class Mesh(object):

	self.program = 0 #program for rendering
	self.vertexL = 0 #vertex uniform location

	self.data = []	 #vertices
	self.nvertes = 0 #number of vertices

	self.modelMatrix = Matrix(4)

	def __init__(self, glProgram, data=None):
		self.program = glProgram
		self.vertexL = self.program.get_attribute(b'm_vertex_position')

		if data is None:
			self.rectangle()
		else:
			self.data = data
			self.nverts = len(data) #assuming is not a multidimensional array

	def setToRectangle(self):
		self.data = [-1.0, 1.0,
					  1.0,-1.0,
					 -1.0,-1.0,
					 -1.0, 1.0,
					  1.0, 1.0,
					  1.0,-1.0]
		self.nvertes = 6

	def setToTriangle(self):
		self.data = [-1.0, 1.0,
					  1.0,-1.0,
					 -1.0,-1.0]
		self.nverts = 3

	def draw(self):
		# Apply model transformations
		self.program.new_uniform(b'model')
		self.program.set_uniform(b'model', self.modelMatrix)

		# Bind Objects
		gl.glBindVertexArray(self.vao)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		pgl.glVertexAttribPointer(self.vertexL, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

		glDrawArrays(GL_TRIANGLES, 0, self.nverts)

		# Clean-up
		glDisableVertexAttribArray(self.vertexL)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

	def buffer_objects(self):
		self.vao = pgl.glGenVertexArrays(1)
		self.vbo = pgl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
		pgl.glBufferData(gl.GL_ARRAY_BUFFER, self.data, gl.GL_STATIC_DRAW)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)