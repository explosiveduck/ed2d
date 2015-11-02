from gem import vector

class PhysObj(object):

    def __init__(self, collisionModel, velocity):
        self.collisionModel = collisionModel
        self.currentPosition = collisionModel.getCenter()
        self.oldPosition = collisionModel.getCenter()
        self.velocity = velocity

    def update(self, delta):
        self.currentPosition += self.velocity * delta

    def getCollisionModel(self):
        translation = vector.Vector(3, data=self.currentPosition) - vector.Vector(3, data=self.oldPosition)
        self.oldPosition = self.currentPosition
        self.collisionModel.translate(translation)
        return self.collisionModel

    def translate(self, x, y):
        self.collisionModel.translate(vector.Vector(3, data=[x, y, 1.0]))

    def getPosition(self):
        return self.currentPosition

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, velocity):
        self.velocity = velocity

    def getX(self):
        return self.collisionModel.getModel().getX()

    def getY(self):
        return self.collisionModel.getModel().getY()

    def getWidth(self):
        return self.collisionModel.getModel().getWidth()

    def getHeight(self):
        return self.collisionModel.getModel().getHeight()