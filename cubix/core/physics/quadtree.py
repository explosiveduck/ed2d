from cubix.core.physics.rectangle import*

class QuadTree(object):
	def __init__(self, lvl, bounds):
		self.level = lvl
		self.bounds = bounds
		self.max_objects = 7
		self.max_levels = 4
		self.objects = []
		self.nodes = [None, None, None, None]

	def clear(self):
		del self.objects[:]
		for i in range(len(self.nodes)):
			if self.nodes[i] is not None:
				self.nodes[i].clear()
				self.nodes[i] = None

	# Splits the node into 4 subnodes
	def split(self):
		subWidth = int(self.bounds.getWidth() / 2)
		subHeight = int(self.bounds.getHeight() / 2)

		x = int(self.bounds.getX())
		y = int(self.bounds.getY())

		# Top Right Node
		self.nodes[0] = QuadTree(self.level + 1, Rectangle(x + subWidth, y, subWidth, subHeight))

		# Top Left Node
		self.nodes[1] = QuadTree(self.level + 1, Rectangle(x, y, subWidth, subHeight))

		# Bottom Left Node
		self.nodes[2] = QuadTree(self.level + 1, Rectangle(x, y + subHeight, subWidth, subHeight))

		# Bottom Right Node
		self.nodes[3] = QuadTree(self.level + 1, Rectangle(x + subWidth, y + subHeight, subWidth, subHeight))

	# Determine which node the objects belongs to.
	# -1 means object cannot completely fit within
	# A child node and is part of the parent node
	def getIndex(self, object):
		index = -1
		verticalMidPoint = self.bounds.getX() + (self.bounds.getWidth() / 2)
		horizontalMidPoint = self.bounds.getY() + (self.bounds.getHeight() / 2)

		# Object can completely fit whitin the top quadrants
		topQuadrant = (object.getY() < horizontalMidPoint) and ((object.getY() + object.getHeight()) < horizontalMidPoint)
		# Object can completely fit whitin the bottom quadrants
		bottomQuadrant = (object.getY() > horizontalMidPoint)

		# Object can completely fit within left quadrants
		if ((object.getX() < verticalMidPoint) and ((object.getX() + object.getWidth()) < verticalMidPoint)):
			if topQuadrant:
				index = 1
			elif bottomQuadrant:
				index = 2
		# Object can completely fit within right quadrants
		elif (object.getX() > verticalMidPoint):
			if topQuadrant:
				index = 0
			elif bottomQuadrant:
				index = 3
		return index

	# Insert the object into the quadtree.
	# If the node exdees the capacity, it will split and add all
	# objects to their corresponding nodes.
	def insert(self, object):
		index = 0
		if self.nodes[0] is not None:
			index = self.getIndex(object)
			if (index is not -1):
				self.nodes[index].insert(object)

		self.objects.append(object)

		if (len(self.objects) > self.max_objects) and (self.level < self.max_levels):
			if self.nodes[0] is None:
				self.split()
				count = 0
				while (count < len(self.objects)):
					index = self.getIndex(self.objects[count])
					if index != -1:
						self.nodes[index].insert(self.objects[count])
						del self.objects[count]
					else:
						count += 1

	# Return all objects that could collide with the given object
	def retrive(self, object):
		returnObjects = self.objects
		index = self.getIndex(object)
		if self.nodes[0] is not None:
			if index is not -1:
				returnObjects.extend(self.nodes[index].retrive(object))
			else:
				for i in range(len(self.nodes)):
					returnObjects.extend(self.nodes[index].retrive(object))

		return returnObjects
