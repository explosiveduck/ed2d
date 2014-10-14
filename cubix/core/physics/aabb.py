from cubix.core.physics.collisiondata import*

class AABB(object):

    def __init__(self, min_edge2D, max_edge2D):
        self.minEdge2D = min_edge2D
        self.maxEdge2D = max_edge2D

    def IntersectAABB(self, oAABB):
        distance1 = oAABB.getMinEdges() - self.maxEdge2D
        distance2 = self.minEdge2D - oAABB.getMaxEdges()

        distance3 = distance1.maxV(distance2)

        maxDistance = distance3.maxS()

        return CollisionData(maxDistance <= 0, distance3)

    def getMinEdges(self):
        return self.minEdge2D

    def getMaxEdges(self):
        return self.maxEdge2D