from ed2d.glmath import matrix


class BaseNode(object):
    def __init__(self, obj):
        self.nodeID = None
        self.isRoot = False
        self.root = None
        self.parent = None
        self.children = [self]

    def attach(self, parent):
        self.root = parent.root
        self.parent = parent
        nodeID = self.root._add_tree_child(self)
        self.nodeID = nodeID
        self.parent.children.append(self)
        return nodeID

    def detach(self):
        self.parent.children.remove(self)
        self.root._del_tree_child(self)
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


class RootNode(BaseNode):
    def __init__(self, obj):
        self.nodeID = 0
        self.treeChildren = [self]
        self.children = [self]
        self.root = self
        self.isRoot = True
        self.nodeCount = 0
        self.reusableIDs = []

    def reparent(self, parent):
        print('Error can\'t reparent root node.')

    def attach(self, parent):
        print('Error can\'t attach root node.')

    def dettach(self, parent):
        print('Error can\'t dettach root node.')

    def _add_tree_child(self, obj):
        if self.reusableIDs:
            nodeID = self.reusableIDs.pop(0)
            self.treeChildren[nodeID] = obj
        else:
            nodeID = len(self.treeChildren)
            self.treeChildren.append(obj)
        self.nodeCount += 1
        return nodeID

    def _del_tree_child(self, obj):
        nodeID = obj.nodeID
        self.treeChildren[nodeID] = None
        self.reusableIDs.append(nodeID)
        self.nodeCount -= 1


class GraphicsNode(BaseNode):
    def __init__(self, obj):
        super(GraphicsNode, self).__init__(obj)
        self.matrix = matrix.Matrix(4)
        self.appliedMatrix = self.matrix

    def bind_matrix(self, matrix):
        self.matrix = matrix


class SceneGraph(object):
    def __init__(self):
        self.root = RootNode(None)
        self.root.matrix = matrix.Matrix(4)
        self.root.appliedMatrix = self.root.matrix

    def establish(self, obj, parent=None):
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
    def _recurse_mtx_apply(self, parent, obj):
        obj.appliedMatrix = parent.appliedMatrix * obj.matrix

    def apply_matrix(self):
        self.root.recurse(self._recurse_mtx_apply)

    def render(self):
        self.apply_matrix()
