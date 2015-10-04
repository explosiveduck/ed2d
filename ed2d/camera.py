import math
from ed2d.glmath import vector
from ed2d.glmath import matrix
from ed2d.glmath import quaternion

class Camera(object):
    def __init__(self):

        # Camera information
        self.yAxis = [0.0, 1.0, 0.0]
        self.position = vector.Vector(3)
        self.rotation = quaternion.Quaternion()
        self.sensitivity = 0.05
        self.aperature = 0

        # Camera modifiers
        self.cameraRotation = matrix.Matrix(4)
        self.cameraPosition = matrix.Matrix(4)
        self.cameraTranslation = matrix.Matrix(4)

        # These are required for rendering
        self.perspectiveProj = matrix.Matrix(4)
        self.orthographicProj = matrix.Matrix(4)
        self.viewMatrix = matrix.Matrix(4)
        self.viewMatrixInverse = matrix.Matrix(4)

        # Camera will rotate around this point
        self.originVisiblity = True
        self.originPosition = [0.0, 0.0, 0.0]

        # Arcball propertise
        self.cur_x = 0
        self.cur_y = 0
        self.arcball_on = False


    def perspectiveProjection(self, fov, aspect, znear, zfar):
        self.perspectiveProj = matrix.perspective(fov, aspect, znear, zfar)

    def orthographicProjection(self, left, right, bottom, top, znear, zfar):
        self.orthographicProj = matrix.orthographic(left, right, bottom, top, znear, zfar)

    def calcViewMatrix(self):
        self.cameraRotation = quaternion.conjugate(self.rotation).toMatrix()
        self.cameraPosition = self.position * -1.0
        self.cameraTranslation.i_translate(self.cameraPosition)

        self.viewMatrix = self.cameraTranslation * self.cameraRotation
        self.viewMatrixInverse = matrix.inverse4(self.viewMatrix)

    def onKeys(self, keys, tick):
        moveAmount = 0.5 * tick

        if 'W' in keys:
            self.move(self.rotation.getForward().vector, -moveAmount)

        if 'S' in keys:
            self.move(self.rotation.getForward().vector, moveAmount)

        if 'A' in keys:
            self.move(self.rotation.getLeft().vector, moveAmount)

        if 'D' in keys:
            self.move(self.rotation.getRight().vector, moveAmount)

        if 'Q' in keys:
            self.move(self.rotation.getForward().vector, math.radians(moveAmount))

        if 'E' in keys:
            self.move(self.rotation.getForward().vector, math.radians(-moveAmount))

        if 'UP' in keys:
            self.move(self.rotation.getUp().vector, moveAmount)

        if 'DOWN' in keys:
            self.movie(self.rotation.getUp().vector, -moveAmount)

        # Mouse buttons
        # if 'MOUSE_LEFT' in keys:
        #     self.arcball_on = True
        # else:
        #     self.arcball_on = False

    def onMouseMove(self, deltaX, deltaY, tick):
        if deltaX != 0:
            self.rotate(self.yAxis, math.radians(deltaX * self.sensitivity * tick))

        if deltaY != 0:
            self.rotate(self.rotation.getRight(), math.radians(-deltaY * self.sensitivity * tick))

        if self.arcball_on:
            self.cur_x = deltaX
            self.cur_y = deltaY
            self.doArcBallRotation(tick)

    def rotate(self, axis, angle):
        self.rotation = self.rotation * quaternion.quat_from_axis_angle(axis, angle)
        self.rotation.i_normalize()

    def move(self, direction, amount):
        self.position = self.position + (direction * amount)

    def setPosition(self, position):
        self.position = position

    def getViewMatrix(self):
        self.calcViewMatrix()
        return self.viewMatrix

    def doArcBallRotation(self, tick):

        last_x = 0
        last_y = 0

        def get_vector(x, y):
            point = vector.Vector(3, data=[1.0 * x / self.screen_width * 2 - 1.0, -(1.0 * y / self.screen_height * 2 - 1.0), 0.0])

            pointSqred = point[0] * point[0] + point[1] * point[1]

            if pointSqred <= 1 * 1:
                point[2] = math.sqrt(1*1 - pointSqred)
            else:
                point.i_normalize()

            return point

        if (self.cur_x is not last_x) or (self.cur_y is not last_y):
            va = get_vector(last_x, last_y)
            vb = get_vector(self.cur_x, self.cur_y)

            angle = math.acos(math.min(1.0, va.dot(vb)))

            axis_in_camera_coord = va.cross(vb)

            self.rotate(axis_in_camera_coord, angle * self.sensitivity * tick)

            last_x = self.cur_x
            last_y = self.cur_y
