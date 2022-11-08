from envs import REGISTRY as env_REGISTRY
from bt_agent import BT_Agent
from agent.bt_agent.agent import Agent
from types import SimpleNamespace as SN

from config.env_config import env_args

def run(env,agent):
    ep_t = 0
    while (True):
        # avail_actions = env.get_avail_actions()
        # actions = agent.act(None, avail_actions)
        
        state = env.get_state()
        avail_actions = env.get_avail_actions()
        obs = env.get_obs()
        
        actions = agent.get_action(state, obs, avail_actions)
        reward, terminated, env_info = env.step(actions)

        if terminated:
            break
        else:
            ep_t += 1
    
if __name__ == '__main__':
    args = SN()

    env = env_REGISTRY["sc2"](**env_args)
    # agent = BT_Agent(args)
    
    env_info = env.get_env_info()
    args.n_agents = env_info["n_agents"]
    args.n_actions = env_info["n_actions"]
    args.state_shape = env_info["state_shape"]
    args.n_enemies = env_info["n_enemies"]
    args.shield_bits_ally = env_info["shield_bits_ally"]
    args.shield_bits_enemy = env_info["shield_bits_enemy"]
    args.unit_type_bits = env_info["unit_type_bits"]

    agent = Agent(args)

    ep = 0
    # while (ep < args.max_episode):
    while (ep < 100):
        env.reset()
        agent.reset()

        run(env,agent)

        ep += 1