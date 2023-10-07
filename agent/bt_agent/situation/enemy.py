from agent.bt_agent.situation.base import base_situation

class enemy_situation(base_situation):
    def __init__(self, environment_args):
        super().__init__(environment_args)
        self.obs = None
        ### 1. create situation term
        self.situation_list = {
            'enemy_alive_num': 0,
            'enemy_pos': [(0,0) for i in range(self.eb.n_enemies)],
            'enemy_visible': [[] for i in range(self.eb.n_enemies)],
            'enemy_dis_sort': [[] for i in range(self.eb.n_enemies)],
            'enemy_hpsp_sort': [[] for i in range(self.eb.n_enemies)],
            'enemy_pfv_sort': [[] for i in range(self.eb.n_enemies)],
        }

    ### 2. create situation update function
    def update_situation_list(self):
        self.update_enemy_alive_number()
        self.update_enemy_position()
        self.update_enemy_dis_sort_list()
        self.update_enemy_hpsp_sort_list()
        # self.update_enemy_visible_list()
        self.update_enemy_pfv_sort_list()
    
    ### 3. write situation update function
    def update_enemy_alive_number(self):
        idx_enemy_hp = [self.eb.state_ally_feat_size*self.eb.n_agents+\
                                i*self.eb.state_enemy_feat_size for i in range(self.eb.n_enemies)]
        enemy_hp_list = self.state[idx_enemy_hp]
        enemy_alive_count = 0
        for hp in enemy_hp_list:
            if hp != 0:
                enemy_alive_count += 1
        self.situation_list['enemy_alive_num'] = enemy_alive_count

    def update_enemy_position(self):
        for i in range(self.eb.n_enemies):
            pos_x = self.state[self.eb.n_agents*self.eb.state_ally_feat_size+\
                                i*self.eb.state_enemy_feat_size+self.eb.state_enemy_x_id]
            pos_y = self.state[self.eb.n_agents*self.eb.state_ally_feat_size+\
                                i*self.eb.state_enemy_feat_size+self.eb.state_enemy_y_id]
            self.situation_list['enemy_pos'][i] = (pos_x, pos_y)


    def update_enemy_visible_list(self):
        # Todo: calc visible but cannot be attacked enemies
        return      

    def update_enemy_dis_sort_list(self):
        for i, agent_obs in enumerate(self.obs):
            # get enemies' canAttack, distance
            idx_bases = [self.eb.move_feat_size + idx_enemy * self.eb.obs_ally_feat_size for idx_enemy in range(self.eb.n_agents)]
            dis_idx = [idx_base+1 for idx_base in idx_bases]
            
            # sort target enemy by distance
            enemy_dis = agent_obs[dis_idx]
            enemy_dis_tuple = [(j,dis) for j,dis in enumerate(enemy_dis.tolist())]            
            self.situation_list['enemy_dis_sort'][i] = sorted(enemy_dis_tuple, key=lambda x:x[1])


    def update_enemy_hpsp_sort_list(self):     
        for i, agent_obs in enumerate(self.obs):
            # get enemies' canAttack, distance
            idx_bases = [self.eb.move_feat_size + idx_enemy * self.eb.obs_ally_feat_size for idx_enemy in range(self.eb.n_agents)]
            hp_idx = [idx_base+4 for idx_base in idx_bases]
            enemy_hpsp = agent_obs[hp_idx]
            if self.eb.shield_bits_ally > 0:
                sp_idx = [idx_base+5 for idx_base in idx_bases]
                enemy_sp = agent_obs[sp_idx]
                enemy_hpsp += enemy_sp

            # sort target enemy by hp(+sp)
            enemy_hpsp_tuple = [(j,hpsp) for j,hpsp in enumerate(enemy_hpsp.tolist())]

            self.situation_list['enemy_hpsp_sort'][i] = sorted(enemy_hpsp_tuple, key=lambda x:x[1])

    def update_enemy_pfv_sort_list(self):
        for i, agent_obs in enumerate(self.obs):
            ### potential field value ver.1: only include the type of enemies 
            # for 2s3z, 0 1 enemy are 's' (long attacking range and more hpsp)
            #           2 3 4 enemy are 'z' (short attacking range and lower hpsp)
            pfv_list = [1,1,0.1,0.1,0.1]
            # sort target enemy by hp(+sp)
            enemy_pfv_tuple = [(j,pfv) for j,pfv in enumerate(pfv_list)]

            self.situation_list['enemy_pfv_sort'][i] = sorted(enemy_pfv_tuple, key=lambda x:x[1])





