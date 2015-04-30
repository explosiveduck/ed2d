import math
from ed2d.glmath import vector
from ed2d.glmath import plane

class CSG(object):
    def __init__(self):
        self.polygons = []

    def clone(self):
        newCSG = CSG()
        for i in range(len(self.polygons)):
            newCSG.polygons.append(self.polygons[i].clone())
        return newCSG

    def fromPolygons(self, polygons):
        newCSG = CSG()
        newCSG.polygons = polygons
        return newCSG

    def toPolygons(self):
        return self.polygons

    def setColor(self, r, g, b):
        for i in range(len(self.polygons)):
            self.polygons[i].shared = [r, g, b]

    def union(self, otherCSG):
        csgA = csgNode(self.clone().polygons)
        csgB = csgNode(otherCSG.clone().polygons)
        csgA.clipTo(csgB)
        csgB.clipTo(csgA)
        csgB.invert()
        csgB.clipTo(csgA)
        csgB.invert()
        csgA.build(csgB.allPolygons())

        return self.fromPolygons(csgA.allPolygons())

    def subtract(self, otherCSG):
        csgA = csgNode(self.clone().polygons)
        csgB = csgNode(otherCSG.clone().polygons)

        csgA.invert()
        csgA.clipTo(csgB)
        csgB.clipTo(csgA)
        csgB.invert()
        csgB.clipTo(csgA)
        csgB.invert()
        csgA.build(csgB.allPolygons())
        csgA.invert()
        return self.fromPolygons(csgA.allPolygons())

    def intersect(self, otherCSG):
        csgA = csgNode(self.clone().polygons)
        csgB = csgNode(otherCSG.clone().polygons)

        csgA.invert()
        csgB.clipTo(csgA)
        csgB.invert()
        csgA.clipTo(csgB)
        csgB.clipTo(csgA)
        csgA.build(csgB.allPolygons())
        csgA.invert()


        return self.fromPolygons(csgA.allPolygons())

    def inverse(self):
        newCSG = self.clone()
        for i in range(len(self.polygons)):
            newCSG.polygons[i] = self.polygons[i].flip()
        return newCSG

    def cube(self, center, radius):
        c = center
        r = radius

        indices = [[0, 4, 6, 2],
                   [1, 3, 7, 5],
                   [0, 1, 5, 4],
                   [2, 6, 7, 3],
                   [0, 2, 3, 1],
                   [4, 5, 7, 6]]

        normals = [[-1, 0, 0],
                   [ 1, 0, 0],
                   [ 0,-1, 0],
                   [ 0, 1, 0],
                   [ 0, 0,-1],
                   [ 0, 0, 1]]

        finalPolygons = []
        invidiualPolygonVertices = []

        for i in range(6):
            invidiualPolygonVertices = []
            for j in range(4):
                pos = vector.Vector(3, 
                                    data = [c[0] + r[0] * (2 *  int(bool(indices[i][j] & 1)) - 1),
                                            c[1] + r[1] * (2 *  int(bool(indices[i][j] & 2)) - 1),
                                            c[2] + r[2] * (2 *  int(bool(indices[i][j] & 4)) - 1)])

                invidiualPolygonVertices.append(csgVertex(pos, vector.Vector(3, normals[i])))
            finalPolygons.append(csgPolygon(invidiualPolygonVertices, [1, 1, 1]))

        return self.fromPolygons(finalPolygons)

    def sphere(self, center, radius, slices, stacks):
        c = vector.Vector(3, data=center)
        r = radius
        sl = slices
        st = stacks

        polygons = []
        vertices = []

        #vertex = lambda theta, phi: vertices.append(csgVertex(c + (vector.Vector(3, data=[math.cos(theta) * math.sin(phi), math.cos(phi), math.sin(theta) * math.sin(phi)]) * r), vector.Vector(3, data=[math.cos(theta) * math.sin(phi), math.cos(phi), math.sin(theta) * math.sin(phi)])))
        def vertex(theta, phi):
            t = theta * math.pi * 2
            p = phi * math.pi
            cosT = math.cos(t)
            cosP = math.cos(p)
            sinT = math.sin(t)
            sinP = math.sin(p)

            direction = vector.Vector(3, data=[cosT * sinP, cosP, sinT * sinP])

            vertices.append(csgVertex(c + (direction * r), direction))

        for i in range(sl):
            for j in range(st):
                vertices = []

                vertex(i / sl, j / st)

                if j > 0:
                    vertex((i + 1) / sl, j / st)

                if j < (stacks - 1):
                    vertex((i + 1) / sl, (j + 1) / st)

                vertex(i / sl, (j + 1) / st)

                polygons.append(csgPolygon(vertices, [1, 1, 1]))

        return self.fromPolygons(polygons)

    def cylinder(self, start, end, radius, slices):
        s = vector.Vector(3, data=start)
        e = vector.Vector(3, data=end)
        r = radius
        slices = slices

        ray = e - s

        axisZ = ray.normalize()
        isY = abs(axisZ.vector[1]) > 0.5
        axisX = vector.cross(vector.Vector(3, data=[isY, int(not isY), 0.0]), axisZ).normalize()
        axisY = vector.cross(axisX, axisZ).normalize()

        start = csgVertex(s, -axisZ)
        end = csgVertex(e, axisZ.normalize())

        polygons = []

        def point(stack, slice, normalBlend):
            angle = slice * math.pi * 2
            out = axisX * math.cos(angle) + axisY * math.sin(angle)
            pos = s + ray * stack + out * r
            normal = out * (1 - abs(normalBlend)) + axisZ * normalBlend
            return csgVertex(pos, normal)

        for i in range(slices):
            t0 = i / slices
            t1 = (i + 1) / slices

            polygons.append(csgPolygon([start, point(0, t0, -1), point(0, t1, -1)], [1, 1, 1]))
            polygons.append(csgPolygon([point(0, t1, 0), point(0, t0, 0), point(1, t0, 0), point(1, t1, 0)], [1, 1, 1]))
            polygons.append(csgPolygon([end, point(1, t1, 1), point(1, t0, 1)], [1, 1, 1]))

        return self.fromPolygons(polygons)


class csgVertex(object):
    def __init__(self, pos, normal):
        self.pos = pos
        self.normal = normal
        self.color = [1, 0, 0]

    def __repr__(self):
        return 'csgVertex: pos:{} , normal:{}, color:{}'.format(self.pos, self.normal, self.color)

    def clone(self):
        return csgVertex(self.pos.clone(), self.normal.clone())

    def flip(self):
        self.normal = -self.normal

    def interpolate(self, vert, t):
        pos = vector.lerp(self.pos, vert.pos, t)
        normal = vector.lerp(self.normal, vert.normal, t)
        return csgVertex(pos, normal)

class csgPlane(plane.Plane):
    def __init__(self, normal, d):
        super(csgPlane, self).__init__()
        self.normal = normal
        self.d = d
        self.epsilon = 1e-5

    def __repr__(self):
        return 'csgPlane: normal:{} , d:{}'.format(self.normal, self.d)

    def clone(self):
        return csgPlane(self.normal.clone(), self.d)

    def splitPolygon(self, polygon, cFront, cBack, f1, b1):
        coplanarFront = cFront
        coplanarBack = cBack
        front = f1
        back = b1

        COPLANAR = 0
        FRONT = 1
        BACK = 2
        SPANNING = 3

        polygonType = 0
        types = []

        for i in range(len(polygon.vertices)):
            t = self.normal.dot(polygon.vertices[i].pos) - self.d
            typeP = 0
            if t < -self.epsilon:
                typeP = BACK
            if t > self.epsilon:
                typeP = FRONT
            if t > -self.epsilon and t < self.epsilon:
                typeP = COPLANAR

            polygonType |= typeP
            types.append(typeP)


        if polygonType == COPLANAR:
            if self.normal.dot(polygon.plane.normal) > 0:
                coplanarFront.append(polygon)
            else:
                coplanarBack.append(polygon)
        if polygonType == FRONT:
            front.append(polygon)
        if polygonType == BACK:
            back.append(polygon)
        if polygonType == SPANNING:
            f = []
            b = []

            for i in range(len(polygon.vertices)):
                j = (i + 1) % len(polygon.vertices)
                ti = types[i]
                tj = types[j]

                vi = polygon.vertices[i]
                vj = polygon.vertices[j]

                if (ti != BACK):
                    f.append(vi)
                if (ti != FRONT):
                    if ti != BACK:
                        b.append(vi.clone())
                    else:
                        b.append(vi)

                if ((ti | tj) == SPANNING):
                    t = (self.d - self.normal.dot(vi.pos)) / self.normal.dot(vj.pos - vi.pos)
                    v = vi.interpolate(vj, t)
                    f.append(v)
                    b.append(v.clone())

            if (len(f) >= 3):
                front.append(csgPolygon(f, polygon.shared))
            if (len(b) >= 3):
                back.append(csgPolygon(b, polygon.shared))

        return coplanarFront, coplanarBack, front, back

class csgPolygon(object):
    def __init__(self, vertices, shared):
        self.vertices = vertices
        self.shared = shared
        self.plane = csgPlane(vector.Vector(3).zero(), 0)
        self.plane.fromPoints(vertices[0].pos, vertices[1].pos, vertices[2].pos)

    def __repr__(self):
        return 'csgPolygon: vertices:{} , shared:{}, plane:{}'.format(self.vertices, self.shared, self.plane)

    def clone(self):
        return csgPolygon(self.vertices, self.shared)

    def flip(self):
        vertices = self.vertices[::-1]
        for i in range(len(self.vertices)):
            if self.vertices[i] == None:
                vertices.append(self.vertices[i].flip())

        self.vertices = vertices
        self.plane.flip()

class csgNode(CSG):
    def __init__(self, polygons):
        super(csgNode, self).__init__()
        self.plane = None
        self.front = None
        self.back = None
        self.polygons = []

        if polygons:
            self.build(polygons)

    def clone(self):
        newNode = csgNode([])
        newNode.plane = self.plane and self.plane.clone()
        newNode.front = self.front and self.front.clone()
        newNode.back = self.back and self.back.clone()
        newNode.polygons = self.polygons
        return newNode

    def invert(self):
        for i in range(len(self.polygons)):
            self.polygons[i].flip()

        self.plane.flip()

        if (self.front):
            self.front.invert()

        if (self.back):
            self.back.invert()

        temp = self.front
        self.front = self.back
        self.back = temp

    def clipPolygons(self, polygons):
        if (self.plane == 0):
            return polygons

        front = []
        back = []
        
        for i in range(len(polygons)):
            front, back, front, back = self.plane.splitPolygon(polygons[i], front, back, front, back)

        if self.front:
            front = self.front.clipPolygons(front)

        if self.back:
            back = self.back.clipPolygons(back)
        else:
            back = []

        return front + back

    def clipTo(self, bsp):
        self.polygons = bsp.clipPolygons(self.polygons)

        if self.front:
            self.front.clipTo(bsp)
        if self.back:
            self.back.clipTo(bsp)

    def allPolygons(self):
        polygons = self.polygons

        if self.front:
            polygons = polygons + (self.front.allPolygons())
        if self.back:
            polygons = polygons + (self.back.allPolygons())
        return polygons

    def build(self, polygons):
        if (len(polygons) == 0):
            return

        if (self.plane is None):
            self.plane = polygons[0].plane.clone()

        front = []
        back = []

        for i in range(len(polygons)):
            self.polygons, self.polygons, front, back = self.plane.splitPolygon(polygons[i], self.polygons, self.polygons, front, back)

        if len(front):
            if (self.front is None):
                self.front = csgNode([])
            self.front.build(front)

        if len(back):
            if(self.back is None):
                self.back = csgNode([])
            self.back.build(back)