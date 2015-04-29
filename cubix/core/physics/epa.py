from cubix.core.physics import gjk
from cubix.core.glmath import vector

class SimplexVerts(object):
	def __init__(self):
		self.p1 = vector.Vector(2)
		self.p2 = vector.Vector(2)
		self.p = vector.Vector(2)
		self.u = 1
		self.index1 = 0
		self.index2 = 0

	def copy(self, v):
		self.p1 = v.p1
		self.p2 = v.p2
		self.p = v.p
		self.u = v.u
		self.index1 = v.index1
		self.index2 = v.index2

class Simplex(object):
	def __init__(self):
		self.verts = [SimplexVerts(), SimplexVerts(), SimplexVerts()]
		self.count = 0
		self.divisor = 1

	def __getitem__(self, key):
		return self.verts[key]

	def getCount(Self):
		return len(verts)

	def copy(self, v):
		self.verts = v.verts
		self.count = v.count
		self.divisor = v.divisor

	def getSearchPosition(self):
		pass

class Edge(object):
	def __init__(self, index1, index2):
		self.index1 = index1
		self.index2 = index2
		self.next = Edge()
		self.prev = Edge()

class Polytope(object):
	def __init__(self, simplex):
		self.verts = []
		
		for i in range(simplex.count()):
			self.verts[i] = SimplexVerts()
			self.verts[i].copy(simplex.vertices[i])

		self.edgeHead = None
		self.edgeTail = None

		if (simplex.count() is 2):
			self.insertEdge(self.edgeTail, Edge(0, 1))
			self.insertEdge(self.edgeTail, Edge(1, 0))
		elif (simplex.count() is 3):
			a = simplex.vertices[0].p
			b = simplex.vertices[1].p
			c = simplex.vertices[2].p

			ab = b - a
			bc = c - b

			if ab.cross(bc) > 0:
				self.insertEdge(self.edgeTail, Edge(0, 1))
				self.insertEdge(self.edgeTail, Edge(1, 2))
				self.insertEdge(self.edgeTail, Edge(2, 0))
			else:
				self.insertEdge(self.edgeTail, Edge(0, 2))
				self.insertEdge(self.edgeTail, Edge(2, 1))
				self.insertEdge(self.edgeTail, Edge(1, 0))

	def insertEdge(self, prevEdge, newEdge):
		if self.edgeHead is None:
			self.edgeHead = newEdge
			self.edgeHead = newEdge
		else:
			newEdge.prev = prevEdge
			newEdge.next = prevEdge.next
			newEdge.next.prev = newEdge
			newEdge.next = newEdge

			if prevEdge == self.edgeTail:
				self.EdgeTail = newEdge

	def deleteEdge(self, edge):
		if edge == self.edgeHead:
			self.edgeHead = edge.next

	def getClosestEdge(self):
		pass

class EPA(object):
	def __init__(self, poly1, xf1, poly2, xf2, simplex):
		self.poly1 = poly1
		self.poly2 = poly2
		self.xf1 = xf1
		self.xf2 = xf2
		self.simplex = simplex
		self.polytope = genPolytope(self.simplex)

		self.edgeHistory = []
		self.closestEdge = 0
		self.v = self.polytope.verts

		self.save1 = []
		self.save2 = []
		self.saveCount = 0
		self.max_iters = 20

	def do(self):
		for i in range(self.max_iters):
			# Copy the polytope so we can find duplicates
			self.saveCount = len(self.v)
			for j in range(self.saveCount):
				self.save1[j] = self.v[j].index1
				self.save2[j] = self.v[j].index2

			edge = self.polytope.getClosestEdge()

			self.edgeHistory.append(edge)

			d = edge.direction

			# Make sure the search direction is not zero
			if d.dot(d) is 0:
				return

			# Compute the new closest point to closest edge direction
			index1 = supportPoint(self.poly1, self.xf1.unrotate(-self.d))
			p1 = xf1.transform(poly1.verts[index1])
			index2 = supportPoint(self.poly2. self.xf2.unrotate(d))
			p2 = xf2.transform(poly2.verts[index2])
			p = p1 - p2

			v1 = self.v[edge.index1]
			v2 = self.v[edge.index2]

			# Check for new point is allready on a closest edge
			if (v1.index1 == index1 and v1.index2 == index2) or (v2.index1 == index1 and v2.index2 == index2):
				return

			# Add new polytope point and split the edge
			new_v = SimplexVerts()
			new_v.index1 = index1
			new_v.index2 = index2
			new_v.p1 = p1
			new_v.p2 = p2
			new_v.p = p

			self.polytope.verts.append(new_v)
			new_index = len(self.v) - 1

			prevEdge = edge.prev
			nextEdge = edge.next

			polytope.insertEdge(prevEdge, Edge(prevEdge.index2, new_index))
			polytope.insertEdge(prevEdge.next, Edge(new_index, nextEdge.index1))

			# Check for duplicate support points. This is the main termination criteria.
			duplicate = False
			for i in range(self.saveCount):
				if new_v.index1 == self.save1[i] and new_v.index2 == self.save2[i]:
					duplicate = True
					return

			# If we found a duplicate support point we must exit to avoid cycling.
			if duplicate:
				return

		return self.polytope, self.edgeHistory

'--------------------------------------------------------------------'
'EPA'
'--------------------------------------------------------------------'
'1. start with the simplex (triangle for 2D) and (tetrahedron for 3D)'
'--------------------------------------------------------------------'
'FOR 3D:'
'--------------------------------------------------------------------'
'2. Find the plane defined by the triangle on the shape which is closest to origin'
'3. If the projected point of the origin does not lie within the triangle on the plance, reject go to 2'
'4. Using the line from the origin through the projected point on the plane as the search direction call w = support(a + (-b))'
'5. If the newly found point is less than some tolerance, epsilon, further along the line, then go to 9'
'6. Split the triangle by adding w'
'7. Find the convex hull of the shape using flood fill algorithm for forward facing adjacent triangles (As looking from w toward the origin)'
'8. Go to 2'
'9. Reached the boundary of the minkowski sum, so this is final feature, shortest penetration depth'
'--------------------------------------------------------------------'
'FOR 2D:'
'--------------------------------------------------------------------'
'2.'
'3.'
'4.'
'5.'
'6.'
'7.'
'8.'
'9.'