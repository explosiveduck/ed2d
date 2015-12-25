from gem import matrix
from ed2d import idgen

class BaseNode(object):
    def __init__(self, obj):
        self.nodeID = None
        self.isRoot = False
        self.root = None
        self.parent = None
        self.children = [self]
        self.obj = obj

    def attach(self, parent):
        self.root = parent.root
        self.parent = parent
        nodeID = self.root.add_tree_child(self)
        self.nodeID = nodeID
        self.parent.children.append(self)
        return nodeID

    def detach(self):
        self.parent.children.remove(self)
        self.root.del_tree_child(self)
        self.parent = None
        self.root = None
        self.nodeID = None

    def recurse(self, callback):
        for i in self.children[1:]:
            callback(self, i)
            i.recurse(callback)

    def recurse_up(self, callback):
        callback(self)
        if not self.parent.isRoot:
            self.parent.recurse_up(callback)

    def reparent(self, parent):
        self.detach()
        self.attach(parent)

    def __repr__(self):
        templ = (type(self).__name__, self.nodeID, hex(id(self)))
        return "<SceneGraph {0} (NodeID {1}) object at {2}>".format(*templ)


class RootNode(BaseNode):
    def __init__(self, obj):
        self.nodeID = 0
        self.treeChildren = [self]
        self.children = [self]
        self.root = self
        self.isRoot = True
        self.ids = idgen.IdGenerator()

    def reparent(self, parent):
        print('Error can\'t reparent root node.')

    def attach(self, parent):
        print('Error can\'t attach root node.')

    def dettach(self, parent):
        print('Error can\'t dettach root node.')

    def add_tree_child(self, obj):
        nodeID = self.ids.gen_id()

        idgen.set_uid_list(self.treeChildren, nodeID, obj)

        return nodeID

    def del_tree_child(self, obj):
        nodeID = obj.nodeID
        self.treeChildren[nodeID] = None
        obj.nodeID = None
        self.ids.del_id(nodeID)


class GraphicsNode(BaseNode):
    def __init__(self, obj, matrix=None):
        super(GraphicsNode, self).__init__(obj)
        if matrix is None:
            self.matrix = matrix.Matrix(4)
        else:
            self.matrix = matrix
        self.appliedMatrix = self.matrix

    def bind_matrix(self, matrix):
        self.matrix = matrix

class SceneGraph(object):
    def __init__(self):
        self.root = RootNode(None)
        self.root.matrix = matrix.Matrix(4)
        self.root.appliedMatrix = self.root.matrix

    def establish(self, obj, parent=None):
        if hasattr(obj, 'matrix'):
            node = GraphicsNode(obj, obj.matrix)
        else:
            node = GraphicsNode(obj)

        if parent is None:
            parent = self.root
        else:
            parent = self.aquire(parent)
        nodeID = node.attach(parent)
        return nodeID

    def reparent(self, nodeID, parentID):
        node = self.aquire(nodeID)
        parent = self.aquire(parentID)
        node.reparent(parent)

    def aquire(self, nodeID):
        return self.root.treeChildren[nodeID]

    def aquire_root(self):
        return self.root

    @classmethod
    def _recurse_update(self, parent, obj):
        obj.obj.update()
        obj.matrix = obj.obj.matrix
        obj.appliedMatrix = parent.appliedMatrix * obj.matrix

    def update(self):
        self.root.recurse(self._recurse_update)

    @classmethod
    def _recurse_render(self, parent, obj):
        obj.obj.render()

    def render(self):
        self.root.recurse(self._recurse_render)
