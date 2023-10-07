from agent.bt_agent.situation.base import base_situation

class ally_situation(base_situation):
    def __init__(self, environment_args):
        super().__init__(environment_args)
        self.obs = None
        self.situation_list = {
            'ally_hp': [],
            'ally_alive_num': 0,
            'ally_pos': [(0,0) for i in range(self.eb.n_agents)],
            'ally_last_hpsp': [[] for i in range(self.eb.n_agents)],
            'ally_under_attack': [False for i in range(self.eb.n_agents)],
            'ally_visible_target': [[] for i in range(self.eb.n_enemies)],
            'ally_canatt_target': [[] for i in range(self.eb.n_enemies)],
            'ally_visnotatt_target': [[] for i in range(self.eb.n_enemies)],
        }

    def update_situation_list(self):
        self.update_ally_hp()
        self.update_ally_alive_num()
        self.update_ally_position()
        self.update_ally_under_attack()
        self.update_ally_visible_target()
        self.update_ally_canattack_target()
        self.update_ally_visiblenotattack_target()
    
    def update_ally_hp(self):
        idx_ally_hp = [self.eb.state_ally_feat_size*i for i in range(self.eb.n_agents)]
        self.situation_list['ally_hp'] = self.state[idx_ally_hp]

    def update_ally_alive_num(self):
        #idx_ally_hp = [self.eb.state_ally_feat_size*i for i in range(self.eb.n_agents)]
        #ally_hp_list = self.state[idx_ally_hp]
        ally_alive_count = 0
        for hp in self.situation_list['ally_hp']:
            if hp != 0:
                ally_alive_count += 1
        self.situation_list['ally_alive_num'] = ally_alive_count

    def update_ally_position(self):
        for i in range(self.eb.n_agents):
            pos_x = self.state[i*self.eb.state_ally_feat_size + self.eb.state_ally_x_id]
            pos_y = self.state[i*self.eb.state_ally_feat_size + self.eb.state_ally_y_id]
            self.situation_list['ally_pos'][i] = (pos_x, pos_y)

    def update_ally_under_attack(self):
        # get the nearest enemy (Todo: get all enemies?)
        hp_id = self.eb.obs_agent_hp_id
        if self.eb.shield_bits_ally > 0:
            sp_id = self.eb.obs_agent_hp_id + 1

        for i, agent_obs in enumerate(self.obs):
            # get agents' hp + sp(shield if exists)
            hpsp = 0
            if self.eb.shield_bits_ally > 0:
                hpsp = agent_obs[hp_id] + agent_obs[sp_id]
            else:                
                hpsp = agent_obs[hp_id]
            
            if self.situation_list['ally_last_hpsp'][i] - hpsp > 0:
                self.situation_list['ally_under_attack'][i] = True

            # update the last agent hpsp
            self.situation_list['ally_last_hpsp'][i] = hpsp

    def update_ally_visible_target(self):
        self.situation_list['ally_visible_target'] = [[] for i in range(self.eb.n_enemies)]
        for i, agent_obs in enumerate(self.obs):
            for j in range(self.eb.n_enemies):
                j_visible_id = self.eb.move_feat_size + self.eb.obs_ally_feat_size * j + 1
                if agent_obs[j_visible_id] != 0:
                    self.situation_list['ally_visible_target'][i].append(j)


    def update_ally_canattack_target(self):
        self.situation_list['ally_canatt_target'] = [[] for i in range(self.eb.n_enemies)]
        for i, agent_obs in enumerate(self.obs):
            for j in range(self.eb.n_enemies):
                j_canatt_id = self.eb.move_feat_size + self.eb.obs_ally_feat_size * j
                if agent_obs[j_canatt_id] != 0:
                    self.situation_list['ally_canatt_target'][i].append(j)

    def update_ally_visiblenotattack_target(self):
        self.situation_list['ally_visnotatt_target'] = [[] for i in range(self.eb.n_enemies)]
        for i, agent_obs in enumerate(self.obs):
            self.situation_list['ally_visnotatt_target'][i] = \
                list(set(self.situation_list['ally_visible_target'][i])-set(self.situation_list['ally_canatt_target'][i]))

