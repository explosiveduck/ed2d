class CollisionData(object):
	def __init__(self, state, direction):
		self.mState = state
		self.mDirection = direction

	def getState(self):
		return self.mState

	def getDistance(self):
		return self.mDirection.magnitude()

	def getDirection(self):
		return self.mDirection.normalize()