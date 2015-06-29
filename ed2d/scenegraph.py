class Node(object):
    def __init__(self, object):
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
        self.parent.children.remove(node)
        self.root._del_tree_child(self)
        self.parent = None
        self.root = None
        self.nodeID = None

    def recuse(self, callback):
        for i in self.children[1:]:
            callback(i)
            i.recuse(callback)

    def reparent(self, parent):
        self.detach()
        self.attach(parent)

class RootNode(Node):
    def __init__(self, object):
        self.nodeID = 0
        self.treeChildren = [self]
        self.children = [self]
        self.root = self
        self.isRoot = True
        self.nodeCount = 0
        self.reusableIDs = []

    def reparent(self, parent):
        print ('Error can\'t reparent root node.')

    def attach(self, parent):
        print ('Error can\'t attach root node.')

    def dettach(self, parent):
        print ('Error can\'t dettach root node.')

    def _add_tree_child(self, object):
        if self.reusableIDs:
            nodeID = self.reusableIDs.pop(0)
            self.treeChildren[nodeID] = object
        else:
            nodeID = len(self.treeChildren)
            self.treeChildren.append(object)
        self.nodeCount += 1
        return nodeID

    def _del_tree_child(self, object):
        nodeID = object.nodeID
        self.treeChildren[nodeID] = None
        self.reusableIDs.append(nodeID)
        self.nodeCount -= 1

class SceneGraph(object):
    def __init__(self):
        self.root = RootNode(None)

    def establish(self, object, parent=None):
        node = Node(object)
        if parent == None:
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