import py_trees
import numpy as np
from agent.bt_agent.team.node import Node

class Moving(Node):
    def __init__(self, namespace, move_type='forward'):
        super().__init__(namespace)
        self.move_type = move_type

    def update(self):
        avail_actions = self.gb.avail_actions
        if self.move_type == 'forward':
            group_actions = []
            for idx in self.bb.group:
                if avail_actions[idx][self.eb.move_east_id] == 1:
                    # move east
                    self.gb.action[idx] = self.eb.move_east_id
                    # group_actions.append(self.eb.move_east_id)
                else:       
                    # stop       
                    self.gb.action[idx] = self.eb.stop_id     
                    # group_actions.append(self.eb.stop_id)

        return py_trees.common.Status.SUCCESS


class Attack(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
    
    def update(self):
        target = self.bb.target
        group_actions = []
        avail_actions = self.gb.avail_actions
        state = self.gb.state
        for idx in self.bb.group:
            if avail_actions[idx][target+self.eb.none_attack_bits] == 1:
                # attack target (id = target id + self.eb.none_attack_bits (noop stop n s e w))
                self.gb.action[idx] = target+self.eb.none_attack_bits
                # group_actions.append(target+6)
            else:
                # out of attack range, move towards the target
                pos_x = state[idx*self.eb.state_ally_feat_size + self.eb.state_ally_x_id]
                pos_y = state[idx*self.eb.state_ally_feat_size + self.eb.state_ally_y_id]
                e_pos_x = state[(idx+1)*self.eb.state_ally_feat_size+\
                                    target*self.eb.state_enemy_feat_size+self.eb.state_enemy_x_id]
                e_pos_y = state[(idx+1)*self.eb.state_ally_feat_size+\
                                    target*self.eb.state_enemy_feat_size+self.eb.state_enemy_y_id]
                # delta_x value: positive - target at east, negative -  target at west
                # delta_y value: positive - target at north, negative - target at south
                delta_x = e_pos_x - pos_x 
                delta_y = e_pos_y - pos_y
                if abs(delta_x) > abs(delta_y):
                    if delta_x < 0:
                        self.gb.action[idx] = self.eb.move_west_id
                        # group_actions.append(5)
                    else:               
                        self.gb.action[idx] = self.eb.move_east_id         
                        # group_actions.append(4)
                else:
                    if delta_y < 0:
                        self.gb.action[idx] = self.eb.move_south_id
                        # group_actions.append(3)
                    else:
                        self.gb.action[idx] = self.eb.move_north_id                        
                        # group_actions.append(2)

        return py_trees.common.Status.SUCCESS


class Kite(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.attack_flag = False

    def update(self):        
        target = self.bb.target
        group_actions = []
        avail_actions = self.gb.avail_actions
        state = self.gb.state

        for idx in self.bb.group:
            if avail_actions[idx][target+self.eb.none_attack_bits] == 1:
                if self.attack_flag == False:
                    # attack target (id = target id + 6 (noop stop n s e w))
                    # group_actions.append(target+self.none_attack_bits)
                    self.gb.action[idx] = target + self.eb.none_attack_bits
                    self.attack_flag = True
                else:                    
                    pos_x = state[idx*self.eb.state_ally_feat_size + self.eb.state_ally_x_id]
                    pos_y = state[idx*self.eb.state_ally_feat_size + self.eb.state_ally_y_id]
                    e_pos_x = state[(idx+1)*self.eb.state_ally_feat_size+\
                                        target*self.eb.state_enemy_feat_size+self.eb.state_enemy_x_id]
                    e_pos_y = state[(idx+1)*self.eb.state_ally_feat_size+\
                                        target*self.eb.state_enemy_feat_size+self.eb.state_enemy_y_id]
                    # delta_x value: positive - target at east, negative -  target at west
                    # delta_y value: positive - target at north, negative - target at south
                    delta_x = e_pos_x - pos_x 
                    delta_y = e_pos_y - pos_y
                    if abs(delta_x) > abs(delta_y):
                        if delta_x < 0:
                            self.gb.action[idx] = self.eb.move_east_id
                            # group_actions.append(self.eb.move_east_id)
                        else:    
                            self.gb.action[idx] = self.eb.move_west_id                    
                            # group_actions.append(self.eb.move_west_id)
                    else:
                        if delta_y < 0:
                            self.gb.action[idx] = self.eb.move_north_id
                            # group_actions.append(self.eb.move_north_id)
                        else:   
                            self.gb.action[idx] = self.eb.move_south_id                     
                            # group_actions.append(self.eb.move_south_id)
                    self.attack_flag = False
            else:
                # out of attack range, stop (Todo: better move strategy)
                self.gb.action[idx] = self.eb.stop_id
                # group_actions.append(self.eb.stop_id)
        return py_trees.common.Status.SUCCESS