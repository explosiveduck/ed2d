from ed2d.physics.collisiondata import*
from ed2d.glmath import vector

# Circle Bounding Box
class CBB(object):

    def __init__(self, radius, center):
        '''Creates a circle bounding box object to be used with the physics engine. Takes in a float for the radius and an array for the center.'''
        self.radius = radius
        self.center = vector.Vector(3, data=center)

    def intersectCBB(self, oCBB):
        tempDistance = self.center - oCBB.center
        distanceCenters = tempDistance.magnitude()
        distanceRadii = self.radius + oCBB.radius

        # Collision happens when the distance between the two centers is less than the sum of the radii
        state = distanceCenters < distanceRadii

        # Calculate the depth penetration
        depthPenetration = distanceCenters - (distanceRadii)

        return CollisionData(state, tempDistance, depthPenetration)

    def getCenter(self):
        return self.center

    def getRadius(self):
        return self.radius
