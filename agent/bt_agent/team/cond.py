import py_trees
import numpy as np

from agent.bt_agent.team.node import Node

# selector节点下的条件应该是互斥的？？？

class CanAttack(Node):
    def __init__(self, namespace):
        super().__init__(namespace)

    def update(self):
        state = self.gb.state
        for idx in self.bb.group:
            # hp < 50% then can kite
            # print ('{} agent hp: {}'.format(idx, state[idx*self.eb.state_ally_feat_size]))
            if state[idx*self.eb.state_ally_feat_size] < self.gb.evade_hp:
                return py_trees.common.Status.FAILURE
        
        if self.bb.target != -1:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class CanKite(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
    
    def update(self):
        state = self.gb.state
        for idx in self.bb.group:
            # hp < 50% then can kite
            # print ('{} agent hp: {}'.format(idx, state[idx*self.eb.state_ally_feat_size]))
            if state[idx*self.eb.state_ally_feat_size] < self.gb.evade_hp:
                return py_trees.common.Status.SUCCESS
        
        return py_trees.common.Status.FAILURE

class CanMove(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
    
    def update(self):
        # canmove = ! (can attack || can kite)
        if self.bb.target != -1:
            return py_trees.common.Status.FAILURE
        
        state = self.gb.state
        for idx in self.bb.group:
            if state[idx*self.eb.state_ally_feat_size] < self.gb.evade_hp:
                return py_trees.common.Status.FAILURE

        
        return py_trees.common.Status.SUCCESS
        