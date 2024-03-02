''' An sample of playing skat randomly. Good for checking the internal values of the game, observation data etc.
'''
import pprint

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import set_seed

def run():
    # Make environment
    env = rlcard.make(
        'skat',
        config={
            'seed': 44,
        }
    )

    # Seed numpy, torch, random
    set_seed(44)

    # Set agents
    agent = RandomAgent(num_actions=env.num_actions)
    env.set_agents([agent for _ in range(env.num_players)])

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)
    # Print out the trajectories
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

if __name__ == '__main__':
    run()
