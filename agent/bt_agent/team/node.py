import py_trees

from agent.bt_agent.directive.node import register_gb_keys, register_eb_keys

def register_keys(self):
    self.bb.register_key('group', access = py_trees.common.Access.WRITE)
    self.bb.register_key('target', access = py_trees.common.Access.WRITE)

    register_gb_keys(self)
    register_eb_keys(self)

def init_keys(self):
    self.bb.group = []
    self.bb.target = -1

class Node(py_trees.behaviour.Behaviour):
    def __init__(self, namespace):
        super().__init__(type(self).__name__)
        self.bb = self.attach_blackboard_client(namespace=namespace)
        self.gb = self.attach_blackboard_client(namespace='global')
        self.eb = self.attach_blackboard_client(namespace='env')
        register_keys(self)