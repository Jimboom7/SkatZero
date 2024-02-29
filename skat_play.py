''' A toy example of playing against pretrained AI on Skat
'''

import os
import rlcard
from rlcard.agents.human_agents.skat_human_agent import SkatHumanAgent

def load_model(model_path):
    import torch
    device = torch.device("cpu") # hardcoded to cpu
    if os.path.isfile(model_path):  # Torch model
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    return agent

# Make environment
env = rlcard.make('skat')
human_agent = SkatHumanAgent(env.num_actions)
dcm_agent_0 = load_model('experiments/skat/skat_1/0_7036800.pth')
dcm_agent_2 = load_model('experiments/skat/skat_1/2_7036800.pth')
env.set_agents([
    dcm_agent_0,
    human_agent,
    dcm_agent_2,
])

print(">> Skat pre-trained model")

while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False, verbose=True)

    print('===============     Result     ===============')
    print("Payoffs:")
    print(payoffs)

    input("Press any key to continue...")
