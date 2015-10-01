from ed2d.physics.rectangle import Rectangle

class QuadTree(object):
	def __init__(self, lvl, bounds):
		self.level = lvl
		self.bounds = bounds
		self.max_objects = 1
		self.max_levels = 5
		self.objects = []
		self.nodes = []

	def clear(self):
		self.objects = []
		for i in range(len(self.nodes)):
			self.nodes[i].clear()
		self.nodes = []

	# Splits the node into 4 subnodes
	def split(self):
		subWidth = int(self.bounds.getWidth() / 2)
		subHeight = int(self.bounds.getHeight() / 2)

		x = int(self.bounds.getX())
		y = int(self.bounds.getY())

		# Top Right Node
		self.nodes.append(QuadTree(self.level + 1, Rectangle(x + subWidth, y, subWidth, subHeight)))

		# Top Left Node
		self.nodes.append(QuadTree(self.level + 1, Rectangle(x, y, subWidth, subHeight)))

		# Bottom Left Node
		self.nodes.append(QuadTree(self.level + 1, Rectangle(x, y + subHeight, subWidth, subHeight)))

		# Bottom Right Node
		self.nodes.append(QuadTree(self.level + 1, Rectangle(x + subWidth, y + subHeight, subWidth, subHeight)))

	# Determine which node the objects belongs to.
	# -1 means object cannot completely fit within
	# A child node and is part of the parent node
	def getIndex(self, obj):
		index = -1
		verticalMidPoint = self.bounds.getX() + (self.bounds.getWidth() / 2)
		horizontalMidPoint = self.bounds.getY() + (self.bounds.getHeight() / 2)

		# Object can completely fit whitin the top quadrants
		topQuadrant = (obj.getY() < horizontalMidPoint) and ((obj.getY() + obj.getHeight()) < horizontalMidPoint)
		# Object can completely fit whitin the bottom quadrants
		bottomQuadrant = (obj.getY() > horizontalMidPoint)

		# Object can completely fit within left quadrants
		if ((obj.getX() < verticalMidPoint) and ((obj.getX() + obj.getWidth()) < verticalMidPoint)):
			if topQuadrant:
				index = 1
			elif bottomQuadrant:
				index = 2
		# Object can completely fit within right quadrants
		elif (obj.getX() > verticalMidPoint):
			if topQuadrant:
				index = 0
			elif bottomQuadrant:
				index = 3
		return index

	# Insert the object into the quadtree.
	# If the node exdees the capacity, it will split and add all
	# objects to their corresponding nodes.
	def insert(self, obj):
		if obj is None:
			return

		if isinstance(obj, list):
			for i in range(len(obj)):
				self.insert(obj[i])
			return

		if len(self.nodes):
			index = self.getIndex(obj)
			if index is not -1:
				self.nodes[index].insert(obj)
				return

		self.objects.append(obj)

		if (len(self.objects) > self.max_objects) and (self.level < self.max_levels):
			if len(self.nodes) is 0:
				self.split()
			i = 0
			while (i < len(self.objects)):
				index = self.getIndex(self.objects[i])
				if index is not -1:
					self.nodes[index].insert(self.objects.pop(i))
				else:
					i += 1

	def retriveAll(self, returnObjects):
		for i in range(len(self.nodes)):
			self.nodes[i].retriveAll(returnObjects)

		for i in range(len(self.objects)):
			returnObjects.append(self.objects[i])
		return returnObjects

	def findObjects(self, returnedObjects, obj):
		index = self.getIndex(obj)
		if index is not -1 and len(self.nodes):
			self.nodes[index].findObjects(returnedObjects, obj)
		for i in range(len(self.objects)):
			returnedObjects.append(self.objects[i])
		return returnedObjects
