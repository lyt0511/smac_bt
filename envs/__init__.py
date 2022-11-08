from functools import partial
# from smac.env import MultiAgentEnv, StarCraft2Env
from envs.starcraft2 import StarCraft2Env
from envs.btagentenv import BTAgentEnv
import sys
import os

def env_fn(env, **kwargs) -> BTAgentEnv:
    return env(**kwargs)

REGISTRY = {}
REGISTRY["sc2"] = partial(env_fn, env=StarCraft2Env)

if sys.platform == "linux":
    os.environ.setdefault("SC2PATH",
                          os.path.join(os.getcwd(), "3rdparty", "StarCraftII"))
