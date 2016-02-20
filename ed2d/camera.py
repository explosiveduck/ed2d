import math
from gem import vector
from gem import matrix
from gem import quaternion
from ed2d import view

class Camera(object):
    def __init__(self):

        # Camera information
        self.yAxis = vector.Vector(3, data=[0.0, 1.0, 0.0])
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

        # Initialize view mode
        self.view = view.View()

        # Modes
        self.MODE_ORTHOGRAPHIC = 1
        self.MODE_PERSPECTIVE = 2
        self.currentMode = 0


    def perspectiveProjection(self, fov, aspect, znear, zfar):
        self.perspectiveProj = matrix.perspective(fov, aspect, znear, zfar)
        self.view.new_projection('persp', self.perspectiveProj)

    def orthographicProjection(self, left, right, bottom, top, znear, zfar):
        self.orthographicProj = matrix.orthographic(left, right, bottom, top, znear, zfar)
        self.view.new_projection('ortho', self.orthographicProj)

    def set_program(self, mtype, program):
        if mtype is 1:
            self.currentMode = self.MODE_ORTHOGRAPHIC
            self.view.register_shader('ortho', program)
        elif mtype is 2:
            self.currentMode = self.MODE_PERSPECTIVE
            self.view.register_shader('persp', program)
        else:
            self.currentMode = 0
            return NotImplemented

    def set_mode(self, mtype):
        if mtype is 1:
            self.currentMode = self.MODE_ORTHOGRAPHIC
            self.view.set_projection('ortho', self.orthographicProj)
        elif mtype is 2:
            self.currentMode = self.MODE_PERSPECTIVE
            self.view.set_projection('persp', self.perspectiveProj)
        else:
            self.currentMode = 0
            return NotImplemented

    def calcViewMatrix(self):
        self.cameraRotation = self.rotation.conjugate().toMatrix()
        self.cameraPosition = self.position * -1.0
        self.cameraTranslation = matrix.Matrix(4).translate(self.cameraPosition)

        self.viewMatrix = self.cameraTranslation * self.cameraRotation
        self.viewMatrixInverse = self.viewMatrix.inverse()


    def onKeys(self, keys, tick):
        moveAmount = 0.5 * tick

        if 'w' in keys:
            self.move(self.rotation.getForward(), -moveAmount)

        if 's' in keys:
            self.move(self.rotation.getForward(), moveAmount)

        if 'a' in keys:
            self.move(self.rotation.getLeft(), moveAmount)

        if 'd' in keys:
            self.move(self.rotation.getRight(), moveAmount)

        if 'q' in keys:
            self.move(self.rotation.getUp(), moveAmount)

        if 'e' in keys:
            self.move(self.rotation.getUp(), -moveAmount)

        if 'UP' in keys:
            self.rotate(self.rotation.getRight(), moveAmount * 0.05)

        if 'DOWN' in keys:
            self.rotate(self.rotation.getRight(), -moveAmount * 0.05)

        if 'LEFT' in keys:
            self.rotate(self.rotation.getUp(), moveAmount * 0.05)

        if 'RIGHT' in keys:
            self.rotate(self.rotation.getUp(), -moveAmount * 0.05)

    def onMouseMove(self, deltaX, deltaY, tick):
        sensitivity = 0.5
        if deltaX != 0:
            self.rotate(self.yAxis, math.radians(deltaX * sensitivity * tick))

        if deltaY != 0:
            self.rotate(self.rotation.getRight(), math.radians(deltaY * sensitivity * tick))

    def rotate(self, axis, angle):
        self.rotation = (quaternion.quat_from_axis_angle(axis, angle) * self.rotation).normalize()

    def move(self, direction, amount):
        self.position = self.position + (direction * amount * self.sensitivity)

    def setPosition(self, position):
        self.position = position

    def getViewMatrix(self):
        self.calcViewMatrix()
        return self.viewMatrix
