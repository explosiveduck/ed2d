from cubix.core.physics import rectangle
from cubix.core.physics import quadtree

class PhysEngine(object):

    def __init__(self):
        # I would love to have width and height as global constants
        self.quadTree = quadtree.QuadTree(0, rectangle.Rectangle(0.0, 0.0, width=800, height=600, flag='QT'))
        self.quadTree.clear()
        self.pObjects = []
        self.returnObjects = []

    def simulate(self, delta):
        '''Update all the objects'''
        # Update the quad tree
        self.quadTree.clear()
        for item in self.pObject:
            self.quadTree.insert(item)

        # Pass this for a while, this basically add velocity to objects
        # But is kinda of a stupid way to do
        '''
        for i in range(len(self.pObjects)):
            self.pObjects[i].update(delta)
        '''

    def collisions(self, object):
        self.returnObjects = self.quadTree.retrive(object)
        for item in self.returnObjects:
            object.getCollisionModel().intersect(item.getCollisionModel())
        del self.returnObjects[:]

    def addObject(self, p_object):
        self.quadTree.insert(p_object)
        self.pObjects.append(p_object)

    def getObject(self, index):
        return self.pObjects[index]

    def getLength(self):
        return len(self.pObjects)