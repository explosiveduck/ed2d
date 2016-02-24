import math
from gem import vector
from gem import matrix
from gem import quaternion

# Modes
MODE_ORTHOGRAPHIC = 1
MODE_PERSPECTIVE = 2

class Camera(object):
    def __init__(self, camType):
        
        self.camType = camType
        
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
        self.projection = matrix.Matrix(4)
        self.viewMatrix = matrix.Matrix(4)
        self.viewMatrixInverse = matrix.Matrix(4)

        # Camera will rotate around this point
        self.originVisiblity = True
        self.originPosition = [0.0, 0.0, 0.0]

        # Arcball properties
        self.cur_x = 0
        self.cur_y = 0
        self.arcball_on = False

    def set_view(self, view):
        # Initialize view mode
        self.view = view
        
        # set proper function to setup projection
        if self.camType is MODE_ORTHOGRAPHIC:
            self.set_projection = self._proj_ortho
            if not self.view.if_projection('ortho'):
                self.view.new_projection('ortho', self.projection)
        elif self.camType is MODE_PERSPECTIVE:
            self.set_projection = self._proj_persp
            if not  self.view.if_projection('persp'):
                self.view.new_projection('persp', self.projection)
        else:
            self.set_projection = None

    def _proj_ortho(self, left, right, bottom, top, znear, zfar):
        self.projection = matrix.orthographic(left, right, bottom, top, znear, zfar)

    def _proj_persp(self, fov, aspect, znear, zfar):
        self.projection = matrix.perspective(fov, aspect, znear, zfar)

    def set_program(self, program):
        if self.camType is MODE_ORTHOGRAPHIC:
            self.view.register_shader('ortho', program)
        elif self.camType is MODE_PERSPECTIVE:
            self.view.register_shader('persp', program)
        else:
            return NotImplemented

    def make_current(self):
        if self.camType is MODE_ORTHOGRAPHIC:
            self.view.set_projection('ortho', self.projection)
        elif self.camType is MODE_PERSPECTIVE:
            self.view.set_projection('persp', self.projection)
        else:
            return NotImplemented

    def calcViewMatrix(self):
        self.cameraRotation = self.rotation.conjugate().toMatrix()
        self.cameraPosition = self.position * -1.0
        self.cameraTranslation = matrix.Matrix(4).translate(self.cameraPosition)

        self.viewMatrix = self.cameraTranslation * self.cameraRotation
        self.viewMatrixInverse = self.viewMatrix.inverse()

    @property
    def vec_up(self):
        return self.rotation.getUp()

    @property
    def vec_down(self):
        return self.rotation.getDown()

    @property
    def vec_left(self):
        return self.rotation.getLeft()

    @property
    def vec_right(self):
        return self.rotation.getRight()

    @property
    def vec_forward(self):
        return self.rotation.getForward()

    @property
    def vec_back(self):
        return self.rotation.getBack()

    def rotate(self, axis, angle):
        self.rotation = (quaternion.quat_from_axis_angle(axis, angle) * self.rotation).normalize()

    def move(self, direction, amount):
        self.position = self.position + (direction * amount * self.sensitivity)

    def setPosition(self, position):
        self.position = position

    def getViewMatrix(self):
        self.calcViewMatrix()
        return self.viewMatrix