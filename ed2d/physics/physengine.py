from ed2d.core.physics import rectangle
from ed2d.core.physics import quadtree

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
        for item in self.pObjects:
            self.quadTree.insert(item)

        # Pass this for a while, this basically add velocity to objects
        # But is kinda of a stupid way to do
        '''
        for i in range(len(self.pObjects)):
            self.pObjects[i].update(delta)
        '''

        # Run collision check
        self.collisions()

    def collisions(self):
        objects = []
        self.quadTree.retriveAll(objects)
        for x in range(len(objects)):
            obj = []
            self.quadTree.findObjects(obj, objects[x])
            for y in range(len(obj)):
                objects[x].getCollisionModel().intersect(obj[y].getCollisionModel())
            del obj[:]
        del objects[:]

    def addObject(self, p_object):
        self.quadTree.insert(p_object)
        self.pObjects.append(p_object)

    def getObject(self, index):
        return self.pObjects[index]

    def getLength(self):
        return len(self.pObjects)