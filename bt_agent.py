import numpy as np
import random

class BT_Agent:
    def __init__(self, args):
        self.args = args

        # self.n_agents = args.n_agents
        self.n_agents = 5
        self.n_actions = 11

    def act(self, obs=None, avail_actions=None):
        #observation

        actions = []

        for i in range(self.n_agents):
            agent_avail_actions = avail_actions[i]
            agent_action = [j for j, act in enumerate(agent_avail_actions) if act == 1]
            actions.append(random.choice(agent_action))

        # return np.random.randint(0,self.n_actions,self.n_agents)
        return actions