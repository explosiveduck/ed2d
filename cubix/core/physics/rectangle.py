from cubix.core import glmath
from cubix.core.physics import aabb

class Rectangle(object):
    def __init__(self, x, y, width=None, height=None, flag=None, data=None):
        # Object information
        self.width = width
        self.height = height

        # Scale data
        self.scaleDeltaX = 0
        self.scaleDeltaY = 0
        self._scaleX = 1
        self._scaleY = 1

        # Positon data
        self.xPosDelta = 0
        self.yPosDelta = 0
        self.xPos = 0
        self.yPos = 0

        # Containers
        self.data = [None, None, None, None]
        self.collisionData = []

        # Type of collision model, used by the physics engine
        self.type = "AABB"

        self.modelMatrix = glmath.Matrix(4)

        # Params processing
        if width == None and height == None:
            self.findDim()

        if flag == None and data == None:
            self.generateVertices()
        elif flag == 'QT' and data == None:
            self.fgenerateVertices()
        else:
            self.data = data
            self.__findDim()

        self.translate(x, y)


    def make_aabb(self):
        '''Generate an AABB for this object'''
        # The collision data should be used by the collider to run an intersection test
        aabbData10 = (self.modelMatrix.transpose() * glmath.Vector(4, data=[self.data[0][0], self.data[0][1], 0.0, 1.0])).xy()
        aabbData11 = (self.modelMatrix.transpose() * glmath.Vector(4, data=[self.data[1][0], self.data[1][1], 0.0, 1.0])).xy()
        aabbData12 = (self.modelMatrix.transpose() * glmath.Vector(4, data=[self.data[2][0], self.data[2][1], 0.0, 1.0])).xy()
        aabbData13 = (self.modelMatrix.transpose() * glmath.Vector(4, data=[self.data[3][0], self.data[3][1], 0.0, 1.0])).xy()

        box11 = aabb.AABB(glmath.Vector(2, aabbData10), glmath.Vector(2, aabbData11))
        box12 = aabb.AABB(glmath.Vector(2, aabbData11), glmath.Vector(2, aabbData12))
        box13 = aabb.AABB(glmath.Vector(2, aabbData12), glmath.Vector(2, aabbData13))
        box14 = aabb.AABB(glmath.Vector(2, aabbData13), glmath.Vector(2, aabbData11))

        self.collisionData = [box11, box12, box13, box14]

    def fgenerateVertices(self):
        '''Generate a box based on width and height'''
        # This is here to be used with the quadtree
        # Is definetly temporary, it might be better to init a unit sized rectangle and then scale it
        self.data = [0.0, self.height,
                     self.width, self.height,
                     0.0, 0.0,
                     self.width, 0.0]

    def generateVertices(self):
        '''Generate a unit box.'''
        self.data = [[0.0, 1.0],
                     [1.0, 1.0],
                     [0.0, 0.0],
                     [1.0, 0.0]]

    def scale(self, valueX, valueY):
        '''Scale the object by X and Y'''
        self.scaleDeltaX = valueX / self._scaleX
        self.scaleDeltaY = valueY / self._scaleY
        self._scaleX = valueX
        self._scaleY = valueY
        self.width = self.scaleDeltaX
        self.height = self.scaleDeltaY

    def translate(self, x, y):
        '''Translate the object by X and Y'''
        self.xPosDelta += x - self.xPos
        self.yPosDelta += y - self.yPos
        self.xPos = x
        self.yPos = y

    def update(self):
        '''Update all the vertices'''
        if self.scaleDeltaX or self.scaleDeltaY:
            vecScale = glmath.Vector(3, data=[self.scaleDeltaX, self.scaleDeltaY, 0.0])
            self.modelMatrix.i_scale(vecScale)
            self.scaleDeltaX = 0
            self.scaleDeltaY = 0
        if self.xPosDelta or self.yPosDelta:
            vecTrans = glmath.Vector(3, data=[self.xPosDelta, self.yPosDelta, 0.0])
            self.modelMatrix.i_translate(vecTrans)
            self.xPosDelta = 0
            self.yPosDelta = 0
        self.make_aabb()

    def __findDim(self):
        '''Calculate the width and height based on the inputed data'''
        self.width = glmath.Vector(2, [self.data[0] - self.data[2], self.data[1] - self.data[3]]).magnitude()
        self.height = glmath.Vector(2, [self.data[2] - self.data[4], self.data[3] - self.data[5]]).magnitude()


    # Getters
    def getVertices(self):
        return self.data

    def getType(self):
        return self.type

    def getCollisionData(self):
        return self.collisionData

    def getModelMatrix(self):
        return self.modelMatrix

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getCenter(self):
        return [self.xPos + self.width / 2.0, self.yPos + self.height / 2.0, 1.0]