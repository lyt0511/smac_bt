import py_trees

from agent.bt_agent.directive.node import register_gb_keys, register_eb_keys

def register_keys(self):
    self.bb.register_key('agent_id', access = py_trees.common.Access.WRITE)
    self.bb.register_key('group', access = py_trees.common.Access.WRITE)
    self.bb.register_key('target', access = py_trees.common.Access.WRITE)
    self.bb.register_key('target_visible', access = py_trees.common.Access.WRITE)
    self.bb.register_key('move_direction', access = py_trees.common.Access.WRITE)
    self.bb.register_key('in_move_queue', access = py_trees.common.Access.WRITE)
    self.bb.register_key('move_queue_target_pos', access = py_trees.common.Access.WRITE)
    self.bb.register_key('kite_action_type', access = py_trees.common.Access.WRITE)
    self.bb.register_key('target_visible_center_pos', access = py_trees.common.Access.WRITE)

    register_gb_keys(self)
    register_eb_keys(self)

def init_keys(self):
    self.bb.agent_id = -1
    self.bb.group = []
    self.bb.target = -1
    self.bb.target_visible = -1
    self.bb.move_direction = 'N'
    self.bb.in_move_queue = False
    self.bb.move_queue_target_pos = []
    self.bb.kite_action_type = 'attack'
    self.bb.target_visible_center_pos = []

class Node(py_trees.behaviour.Behaviour):
    def __init__(self, namespace):
        super().__init__(type(self).__name__)
        self.bb = self.attach_blackboard_client(namespace=namespace)
        self.gb = self.attach_blackboard_client(namespace='global')
        self.eb = self.attach_blackboard_client(namespace='env')
        register_keys(self)