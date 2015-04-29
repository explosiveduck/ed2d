class cModel(object):

    def __init__(self, object):
        # The following need to be "overwritten" by 
        # by the object class.. ie. rectangle or circle in case of 2D
        self.object = object
        self.type = object.getType()
        self.cmodel = object.getCollisionData()

    def intersect(self, cother):
        '''Check interesection between two colliders'''
        if self.type == "AABB" and cother.getType() == "AABB":
            # The following interesection test is for a AABBB
            # The AABB has only 4 edges to check against
            # This intersection function will be called by physics engine via physics object
            # It returns a collisiondata object
            # It will contains, direction, distance and state
            for i in range(4):
                for j in range(4):
                    ctemp = self.cmodel[i].IntersectAABB(cother.getCModel()[j])
                    if ctemp.getState():
                        print('Collision:', 'Dist:', ctemp.getDistance(), 'Dir:', ctemp.getDirection().vector)
        else:
            return NotImplemented

    def translate(self, translation):
        # This function is best called before interesction is used
        # For now it takes in a vector of any size but it will only use X and Y
        # If there is not translation then it doesn't make any sense to even update the matrix
        if (translation.vector[0] != 0.0 and translation.vector[1] != 0.0):
            self.object.translate(translation.vector[0], translation.vector[1])
            self.object.update()

        self.cmodel = self.object.getCollisionData()

    def getCenter(self):
        return self.object.getCenter()

    def getModel(self):
        return self.object

    def getCModel(self):
        return self.cmodel

    def getType(self):
        return self.type