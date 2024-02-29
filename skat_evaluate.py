''' An example of evluating the trained models in RLCard
'''
import os
import argparse

import rlcard

from rlcard.utils import (
    set_seed,
    tournament
)

def load_model(model_path, env=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    return agent

def evaluate(args):
    import time
    start = time.time()

    # Check whether gpu is available
    #device = get_device()
    import torch
    device = torch.device("cpu") # hardcoded to cpu

    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make("skat", config={'seed': args.seed})

    # Load models
    agents = []
    for _, model_path in enumerate(args.models):
        agents.append(load_model(model_path, env, device))
    env.set_agents(agents)

    # Evaluate
    rewards = tournament(env, args.num_games)
    for position, reward in enumerate(rewards):
        print(position, args.models[position], reward)
    end = time.time()
    print("Time: " + str(end - start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")
    parser.add_argument(
        '--models',
        nargs='*',
        # default=[
        #     'experiments/skat/skat_1/0_7036800.pth',
        #     'random',
        #     'random',
        # ],
        default=[
            'random',
            'experiments/skat/skat_1/1_7036800.pth',
            'experiments/skat/skat_1/2_7036800.pth',
        ],
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
    )
    parser.add_argument(
        '--num_games',
        type=int,
        default=1000,
    )

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    evaluate(args)
