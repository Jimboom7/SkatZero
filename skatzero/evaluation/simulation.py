import time
import os
import subprocess
import sys
import random

import numpy as np
import torch
from torch import multiprocessing as mp

from skatzero.agents.random_agent import RandomAgent
from skatzero.agents.human_agent import HumanAgent
from skatzero.agents.rule_based_agent import RuleBasedAgent
from skatzero.env.skat import SkatEnv

def load_model(model_path, device='cpu'):
    if os.path.isfile(model_path):  # Torch model
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':
        agent = RandomAgent(num_actions=32)
    elif model_path == 'human':
        agent = HumanAgent(num_actions=32)
    elif model_path == 'rule_based':
        agent = RuleBasedAgent(num_actions=32)
    else:
        print("Modell kann nicht geladen werden!!!")
        print(model_path)
    return agent


def set_seed(seed):
    if seed is not None:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        if 'torch' in installed_packages:
            torch.backends.cudnn.deterministic = True
            torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)


def act(i, env, result, count, num_games, lock):
    try:
        print('Evaluation Actor ' + str(i) + ' started.')
        payoffs = [0 for _ in range(env.num_players)]
        while count[0] < num_games:
            _, _payoffs = env.run(is_training=False)
            if isinstance(_payoffs, list):
                for _p in _payoffs:
                    for i, _ in enumerate(payoffs):
                        with lock:
                            count[i] += 1
                            result[i] += _p[i]
            else:
                for i, _ in enumerate(payoffs):
                    with lock:
                        count[i] += 1
                        result[i] += _payoffs[i]
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exception in worker process %i', i)
        raise e


def tournament(env, num, num_actors):
    ctx = mp.get_context('spawn')

    with mp.Manager() as manager:
        lock = manager.Lock()
        count = manager.list([0 for _ in range(env.num_players)])
        result = manager.list([0 for _ in range(env.num_players)])

        actor_list = []
        for i in range(num_actors):
            actor = ctx.Process(
                target=act,
                args=(i, env, result, count, num, lock))
            actor.start()
            actor_list.append(actor)

        while count[0] < num:
            time.sleep(1)

        for actor in actor_list:
            actor.terminate()

        payoffs = [0 for _ in range(env.num_players)]
        for i in range(env.num_players):
            payoffs[i] = result[i] / count[i]

    return payoffs


def save_evaluation_duel(folder, number, num_games, num_actors=10):
    print("Starting Evaluation")
    base_folder = 'checkpoints/'
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

    seed = 42
    set_seed(seed)
    env = SkatEnv(seed=seed)

    # Evaluation 1: Soloplayer
    agents = []
    for _, model_path in enumerate(model_solo):
        agents.append(load_model(model_path))
    env.set_agents(agents)
    rewards = tournament(env, num_games, num_actors)
    for position, reward in enumerate(rewards):
        print(position, model_solo[position], reward)

    # Evaluation 2: Opponents
    agents = []
    for _, model_path in enumerate(model_opponent):
        agents.append(load_model(model_path))
    env.set_agents(agents)
    rewards2 = tournament(env, num_games, num_actors)
    for position, reward in enumerate(rewards2):
        print(position, model_opponent[position], reward)

    print("Score: " + str(rewards[0] - rewards2[0]))
    with open(base_folder + "/evaluate_log.csv", "a", encoding='utf-8') as logfile:
        logfile.write(str(folder) + "," + str(number) + "," + str(num_games) + "," + str(round(rewards[0] - rewards2[0], 2)) + "\n")


def get_bidding_data(player, random_game=False):
    models = [
            player,
            player,
            player
        ]

    agents = []
    for _, model_path in enumerate(models):
        agents.append(load_model(model_path))

    if random_game:
        env = SkatEnv()
    else:
        seed = 42
        set_seed(seed)
        env = SkatEnv(seed=seed)

    env.set_agents(agents)
    # TODO: Handspiel setzen!
    
    state, _ = env.reset()

    _, info = agents[0].eval_step(state)

    return info['values']
