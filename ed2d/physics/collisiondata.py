class CollisionData(object):
	def __init__(self, state, direction, depthPenetration = None):
		self.mState = state
		self.mDirection = direction
		self.mDepthPenetration = depthPenetration

	def getState(self):
		return self.mState

	def getDistance(self):
		return self.mDirection.magnitude()

	def getDirection(self):
		return self.mDirection.normalize()

	def getDepthPenetration(self):
		return self.mDepthPenetration