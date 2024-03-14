import pprint

from skatzero.env.skat import SkatEnv
from skatzero.agents.random_agent import RandomAgent
from skatzero.evaluation.simulation import load_model, set_seed

if __name__ == '__main__':
    env = SkatEnv(seed=42)

    set_seed(42)

    #agent = RandomAgent(num_actions=env.num_actions)
    #env.set_agents([agent for _ in range(env.num_players)])

    MODEL1 = 'random'
    MODEL2 = 'random'
    MODEL3 = 'random'
    #MODEL1 = 'checkpoints/skat_19_blind_hand/0_100.pth'
    #MODEL2 = 'checkpoints/skat_19_blind_hand/1_100.pth'
    #MODEL3 = 'checkpoints/skat_19_blind_hand/2_100.pth'

    random_agent = RandomAgent(num_actions=env.num_actions)
    dcm_agent_0 = load_model(MODEL1)
    dcm_agent_1 = load_model(MODEL2)
    dcm_agent_2 = load_model(MODEL3)
    env.set_agents([
        dcm_agent_0,
        dcm_agent_1,
        dcm_agent_2,
    ])

    trajectories, _ = env.run(is_training=False)

    print('\nTrajectories:')
    print(trajectories)
    print('\nSample raw observation:')
    pprint.pprint(trajectories[0][0]['raw_obs'])
    pprint.pprint(trajectories[1][0]['raw_obs'])
    pprint.pprint(trajectories[0][20]['raw_obs'])
    pprint.pprint(trajectories[1][20]['raw_obs'])
    print('\nSample raw legal_actions:')
    pprint.pprint(trajectories[0][0]['raw_legal_actions'])
    print('State Size')
    print(str(len(trajectories[0][0]['obs'])) + " - " + str(len(trajectories[1][0]['obs'])) + " - " + str(len(trajectories[1][0]['obs'])))
