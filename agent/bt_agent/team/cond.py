import py_trees
import numpy as np

from agent.bt_agent.team.node import Node

# selector节点下的条件应该是互斥的？？？

class CanEvade(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
    
    def update(self):
        state = self.gb.state
        # agent dead
        for idx in self.bb.group:
            if state[idx*self.eb.state_ally_feat_size] == 0:
                return py_trees.common.Status.FAILURE

        # 1 see anemy, 2 hp < evade hp, and is 3 under attack can evade
        if self.bb.target_visible == -1:
            return py_trees.common.Status.FAILURE

        for idx in self.bb.group:
            # print ('{} agent hp: {}'.format(idx, state[idx*self.eb.state_ally_feat_size]))
            if state[idx*self.eb.state_ally_feat_size] < self.gb.evade_hp and self.gb.under_attack[idx]:
                return py_trees.common.Status.SUCCESS
        
        return py_trees.common.Status.FAILURE

# kite ver1 condition node
# class CanKite(Node):
#     def __init__(self, namespace):
#         super().__init__(namespace)
    
#     def update(self):
#         state = self.gb.state
#         for idx in self.bb.group:
#             # hp < kite_hp then can kite
#             # print ('{} agent hp: {}'.format(idx, state[idx*self.eb.state_ally_feat_size]))
#             if state[idx*self.eb.state_ally_feat_size] < self.gb.kite_hp:
#                 self.bb.kite_action_type == 'move'
#                 return py_trees.common.Status.SUCCESS
        
#         return py_trees.common.Status.FAILURE

# kite ver2 condition node
class CanKite(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
    
    def update(self):
        state = self.gb.state
        # agent dead
        for idx in self.bb.group:
            if state[idx*self.eb.state_ally_feat_size] == 0:
                return py_trees.common.Status.FAILURE

        for idx in self.bb.group:
            # hp < kite_hp then can kite
            # print ('{} agent hp: {}'.format(idx, state[idx*self.eb.state_ally_feat_size]))
            if state[idx*self.eb.state_ally_feat_size] < self.gb.kite_hp and self.bb.kite_action_type == 'attack':
                self.bb.kite_action_type = 'move'
                return py_trees.common.Status.SUCCESS
        
        return py_trees.common.Status.FAILURE


class CanAttack(Node):
    def __init__(self, namespace, unit_mode):
        super().__init__(namespace)
        self.unit_mode = unit_mode
        self.agent_id = self.bb.agent_id

    def update(self):
        state = self.gb.state
        # agent dead
        # for idx in self.bb.group:
        #     if state[idx*self.eb.state_ally_feat_size] == 0:
        #         return py_trees.common.Status.FAILURE
        
        if state[self.agent_id*self.eb.state_ally_feat_size] == 0:
            return py_trees.common.Status.FAILURE

        ### kite calc (Zeolots does not need to kite)
        if self.unit_mode == 'Stalker':
            for idx in self.bb.group:
                # hp < kite_hp then judge whether to kite
                # print ('{} agent hp: {}'.format(idx, state[idx*self.eb.state_ally_feat_size]))
                if state[idx*self.eb.state_ally_feat_size] < self.gb.kite_hp:                
                    if self.bb.kite_action_type != 'move':
                        return py_trees.common.Status.FAILURE

        ### attack target calc        
        # target id calc
        # base info calc  
        avail_actions = self.gb.avail_actions      
        dis = self.gb.situation['enemy'].situation_list['enemy_dis_sort']
        ho = self.gb.situation['enemy'].situation_list['enemy_hpsp_sort']
        pfv = self.gb.situation['enemy'].situation_list['enemy_pfv_sort']
        ally_alive_num = self.gb.situation['ally'].situation_list['ally_alive_num']
        enemy_alive_num = self.gb.situation['enemy'].situation_list['enemy_alive_num']

        if self.unit_mode == 'Stalker': 
            for j, _ in ho[self.agent_id]:
                if avail_actions[self.agent_id][j+self.eb.none_attack_bits] == 1:
                    self.bb.target = j
                    break   
        elif self.unit_mode == 'Zeolots':             
            for j, _ in dis[self.agent_id]:
                if avail_actions[self.agent_id][j+self.eb.none_attack_bits] == 1:
                    self.bb.target = j
                    break
        
        if self.bb.target != -1:
            # refer to kite action, set the kite action type to attack
            self.bb.kite_action_type = 'attack'
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


class CanMove(Node):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.agent_id = self.bb.agent_id
    
    def update(self):
        ### canmove = ! (can attack || can kite)

        ### any attack target for failure
        # get enemies' canAttack, distance
        agent_obs = self.gb.obs[self.agent_id]
        idx_bases = [self.eb.move_feat_size + idx_enemy * self.eb.obs_ally_feat_size \
                                            for idx_enemy in range(self.eb.n_agents)]
        canatt_idx = [idx_base for idx_base in idx_bases]
        enemy_canatt = agent_obs[canatt_idx]

        # if enemy_canatt is empty, ith team's target must be set to -1
        # (otherwise previous attack target exists even if it out of range in the following steps)
        if enemy_canatt.sum() != 0:
            # self.bb.target = -1
            return py_trees.common.Status.FAILURE
        
        state = self.gb.state
        ### agent dead for failure
        if state[self.agent_id*self.eb.state_ally_feat_size] == 0:
            return py_trees.common.Status.FAILURE

        # for idx in self.bb.group:
        #     if state[idx*self.eb.state_ally_feat_size] < self.gb.evade_hp:
        #         return py_trees.common.Status.FAILURE

        # defatul move to west
        self.bb.move_direction = 'e'

        return py_trees.common.Status.SUCCESS
        