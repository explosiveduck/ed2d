from ed2d.glmath import vector

class SimplexVerts(object):
    def __init__(self):
        self.p1 = vector.Vector(2)
        self.p2 = vector.Vector(2)
        self.p = vector.Vector(2)
        self.u = 1
        self.index1 = 0
        self.index2 = 0

    def copy(self, v):
        self.p1 = v.p1
        self.p2 = v.p2
        self.p = v.p
        self.u = v.u
        self.index1 = v.index1
        self.index2 = v.index2

class Simplex(object):
    def __init__(self, vertices):
        self.vertices = []
        self.vertices.append(vertices)

    def __getitem__(self, key):
        return self.vertices[key]

    def getCount(self):
        return len(self.vertices)

    def add(self, vertex):
        self.vertices.append(vertex)

    def copy(self, s):
        self.vertices = s.vertices

    def remove(self, vertex):
        index = 0
        for i in range(len(self.vertices)):
            if vertex == self.vertices[i]:
                index = i
        #Trash the value
        del self.vertices[index]

def Support(regionOne, regionTwo, direction):
    '''Makes use of the primities. Each primitive has its own getFurthestPoint function. '''
    return regionOne.getFurthestPoint(direction) - regionTwo.getFurthestPoint(-direction)

class GJK(object):
    def __init__(self):
        self.direction = vector.Vector(3)

    def intersects(self, regionOne, regionTwo):
        # Get initial point on the Minkowski difference
        s = Support(regionOne, regionTwo, vector.Vector(3).one())

        # Create the inital simplex
        simplex = Simplex(s)

        # Choose an initial direction towards the origin
        self.direction = -s

        # Choose a maximum number of iterations to avoid
        # an infinite loop during non-convergent search.
        maxIterations = 50

        for i in range(maxIterations):
            # Get our next simplex point towards the origin
            a = Support(regionOne, regionTwo, self.direction)

            # If we move toward the origin and didn't pass it
            # then we never will and there is no intersection
            if (a.isInOppositeDirection(self.direction)):
                return False

            # Otherwise we add the new point to the simplex and process it.
            simplex.add(a)

            # Here we either find a collision or we find the closest feature of 
            # simplex to the origin, make the new simplex and update the direction
            # to move toward the origin from that feature.
            if self.processSimplex(simplex):
                return True

        # If we still couldn't find a simplex that contains the origin
        # then we probably have an intersection
        return True

    def processSimplex(self, simplex):
        '''Either finds a collision or the closest feature of the simplex to the origin, and updates the simplex and direction'''
        if (simplex.getCount() == 2):
            return self.processLine(simplex)
        elif (simplex.getCount() == 3):
            return self.processTriangle(simplex)
        else:
            return self.processTetrehedron(simplex)

    def processLine(self, simplex):
        '''Determines which Veronoi region of a tetrehedron the origin is in, utilizing the preserved winding of the simplex to eliminate certain regions'''
        a = simplex[1]
        b = simplex[0]

        ab = b - a
        aO = -a

        if(ab.isInSameDirection(aO)):
            #dot = ab.dot(aO)
            #angle = math.acos(dot / ab.magnitude() * aO.magnitude())
            self.direction = vector.cross(vector.cross(ab, aO), ab)
        else:
            simplex.remove(b)
            self.direction = aO
        return False

    def processTriangle(self, simplex):
        '''Determines which Veronoi region of a tetrehedron the origin is in, utilizing the preserved winding of the simplex to eliminate certain regions'''
        a = simplex[2]
        b = simplex[1]
        c = simplex[0]

        ab = b - a
        ac = c - a
        abc = vector.cross(ab, ac)
        aO = -a

        acNormal = vector.cross(abc, ac)
        abNormal = vector.cross(ab, abc)

        if(acNormal.isInSameDirection(aO)):
            if(ac.isInSameDirection(aO)):
                simplex.remove(b)
                self.direction = vector.cross(vector.cross(ac, aO), ac)
            else:
                if(ab.isInSameDirection(aO)):
                    simplex.remove(c)
                    self.direction = vector.cross(vector.cross(ab, aO), ab)
                else:
                    simplex.remove(b)
                    simplex.remove(c)
                    self.direction = aO
        else:
            if (abNormal.isInSameDirection(aO)):
                if(ab.isInSameDirection(aO)):
                    simplex.remove(c)
                    self.direction = vector.cross(vector.cross(ab, aO), ab)
                else:
                    simplex.remove(b)
                    simplex.remove(c)
                    self.direction = aO
            else:
                if(abc.isInSameDirection(aO)):
                    self.direction = vector.cross(vector.cross(abc, aO), abc)
                else:
                    self.direction = vector.cross(vector.cross(-abc, aO), -abc)
        return False

    def processTetrehedron(self, simplex):
        '''Determines which Veronoi region of a tetrehedron the origin is in, utilizing the preserved winding of the simplex to eliminate certain regions'''
        a = simplex[3]
        b = simplex[2]
        c = simplex[1]
        d = simplex[0]

        ac = c - a
        ad = d - a
        ab = b - a
        #bc = c - b
        #bd = d - b

        acd = vector.cross(ad, ac)
        abd = vector.cross(ab, ad)
        abc = vector.cross(ac, ab)

        aO = -a

        if (abc.isInSameDirection(aO)):
            if (vector.cross(abc, ac).isInSameDirection(aO)):
                simplex.remove(b)
                simplex.remove(d)
                self.direction = vector.cross(vector.cross(ac, aO), ac)
            elif(vector.cross(ab, abc).isInSameDirection(aO)):
                simplex.remove(c)
                simplex.remove(d)
                self.direction = vector.cross(vector.cross(ab, aO), ab)
            else:
                simplex.remove(d)
                self.direction = abc
        elif (acd.isInSameDirection(aO)):
            if (vector.cross(acd, ad).isInSameDirection(aO)):
                simplex.remove(b)
                simplex.remove(c)
                self.direction = vector.cross(vector.cross(ad, aO), ad)
            elif(vector.cross(ac, acd).isInSameDirection(aO)):
                simplex.remove(b)
                simplex.remove(d)
                self.direction = vector.cross(vector.cross(ac, aO), ac)
            else:
                simplex.remove(b)
                self.direction = acd
        elif(abd.isInSameDirection(aO)):
            if(vector.cross(abd, ab).isInSameDirection(aO)):
                simplex.remove(b)
                simplex.remove(d)
                self.direction = vector.cross(vector.cross(ab, aO), ab)
            elif(vector.cross(ab, abd).isInSameDirection(aO)):
                simplex.remove(b)
                simplex.remove(c)
                self.direction = vector.cross(vector.cross(ad, aO), ad)
            else:
                simplex.remove(c)
                self.direction = abd
        else:
            return True
        return False






