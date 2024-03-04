''' An example of evluating the trained models in RLCard
'''
import os

import rlcard

from rlcard.utils import (
    set_seed,
    tournament,
    tournament_multiproc
)

def load_model(model_path, env=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    else:
        print("Modell kann nicht geladen werden!!!")
    return agent

def evaluate(folder, number, num_games, num_actors=4):
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    #os.environ["OPENBLAS_NUM_THREADS"] = "1"
    #os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    #os.environ["NUMEXPR_NUM_THREADS"] = "1"
    print("Starting Evaluation")
    base_folder =  'experiments/skat/'
    folder = str(folder)
    number = str(number)

    model_solo = [
            base_folder + folder + '/0_' + number + '.pth',
            'random',
            'random'
        ]
    model_opponent = [
            'random',
            base_folder + folder + '/1_' + number + '.pth',
            base_folder + folder + '/2_' + number + '.pth'
        ]


    # Check whether gpu is available
    #device = get_device()
    import torch
    device = torch.device("cpu") # hardcoded to cpu

    # Seed numpy, torch, random
    set_seed(42)

    # Make the environment with seed
    env = rlcard.make("skat", config={'seed': 42})

    # Load models
    agents = []
    for _, model_path in enumerate(model_solo):
        agents.append(load_model(model_path, env, device))
    env.set_agents(agents)

    # Evaluate
    if num_actors == 1:
        rewards = tournament(env, num_games)
    else:
        rewards = tournament_multiproc(env, num_games, num_actors)
    for position, reward in enumerate(rewards):
        print(position, model_solo[position], reward)

    # Load models 2
    agents = []
    for _, model_path in enumerate(model_opponent):
        agents.append(load_model(model_path, env, device))
    env.set_agents(agents)

    # Evaluate 2
    if num_actors == 1:
        rewards2 = tournament(env, num_games)
    else:
        rewards2 = tournament_multiproc(env, num_games, num_actors)
    for position, reward in enumerate(rewards2):
        print(position, model_opponent[position], reward)

    print("Score: " + str(rewards[0] - rewards2[0]))
    with open(base_folder + "/evaluate_log.csv", "a", encoding='utf-8') as logfile:
        logfile.write(str(folder) + "," + str(number) + "," + str(num_games) + "," + str(rewards[0] - rewards2[0]) + "\n")


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    NUM_GAMES = 10000
    FOLDER = "skat_0"
    NUMBER = "30035200"
    evaluate(FOLDER, NUMBER, NUM_GAMES)
