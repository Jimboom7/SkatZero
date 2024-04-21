import copy
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
        agent.eval()
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


def act(act_num, env, result, count, num_games, lock, seed):
    try:
        print('Evaluation Actor ' + str(act_num) + ' started.')
        payoffs = [0 for _ in range(env.num_players)]
        while True:
            with lock:
                if count.value >= num_games:
                    break
                count.value += 1
                env.base_seed = count.value + seed
            _, _payoffs = env.run(is_training=False)
            for i, _ in enumerate(payoffs):
                with lock:
                    result[i] += _payoffs[i]
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exception in worker process %i', i)
        raise e


def tournament(env, num, num_actors, seed):
    ctx = mp.get_context('spawn')

    with mp.Manager() as manager:
        lock = manager.Lock()
        count = manager.Value(int, 0)
        result = manager.list([0 for _ in range(env.num_players)])

        actor_list = []
        for i in range(num_actors):
            actor = ctx.Process(
                target=act,
                args=(i, env, result, count, num, lock, seed))
            actor.start()
            actor_list.append(actor)

        while count.value < num:
            time.sleep(1)

        for actor in actor_list:
            actor.terminate()

        payoffs = [0 for _ in range(env.num_players)]
        for i in range(env.num_players):
            payoffs[i] = result[i] / count.value

    return payoffs


def save_evaluation_duel(folder, model1, model2, num_games, blind_hand_chance=0.1, num_actors=10, gametype='D', seed='42'):
    print("Starting Evaluation")
    base_folder = 'models/checkpoints/'
    folder = str(folder)
    number1 = str(model1)
    number2 = str(model2)

    models_solo = [
            base_folder + folder + '/0_' + number1 + '.pth',
            base_folder + folder + '/1_' + number2 + '.pth',
            base_folder + folder + '/2_' + number2 + '.pth'
        ]
    models_opponent = [
            base_folder + folder + '/0_' + number2 + '.pth',
            base_folder + folder + '/1_' + number1 + '.pth',
            base_folder + folder + '/2_' + number1 + '.pth'
        ]

    if number2 == 'random':
        models_solo[1] = 'random'
        models_solo[2] = 'random'
        models_opponent[0] = 'random'

    set_seed(seed)
    env = SkatEnv(blind_hand_chance, seed=seed, gametype=gametype)

    # Evaluation 1: Soloplayer
    agents = []
    for _, model_path in enumerate(models_solo):
        agents.append(load_model(model_path))
    env.set_agents(agents)
    rewards = tournament(env, num_games, num_actors, seed)
    for position, reward in enumerate(rewards):
        print(position, models_solo[position], reward)

    # Evaluation 2: Opponents
    agents = []
    for _, model_path in enumerate(models_opponent):
        agents.append(load_model(model_path))
    env.set_agents(agents)
    rewards2 = tournament(env, num_games, num_actors, seed)
    for position, reward in enumerate(rewards2):
        print(position, models_opponent[position], reward)

    print("Score: " + str(rewards[0] - rewards2[0]))
    with open("testresults/evaluate_log.csv", "a", encoding='utf-8') as logfile:
        logfile.write(str(folder) + "," + str(number1) + "," + str(number2) + "," + str(num_games) + "," + str(round(rewards[0] - rewards2[0], 2)) + "\n")


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
        env = SkatEnv(blind_hand_chance=1.0)
    else:
        seed = 42
        set_seed(seed)
        env = SkatEnv(blind_hand_chance=1.0, seed=seed)

    env.set_agents(agents)

    #state, _ = env.reset(always_solo=True)

    raw_state, _ = env.game.init_game(blind_hand=1.0)

    raw_state['self'] = 0

    # 4 mal in Schleife
    raw_state['trump'] = 'D'

    state = env.extract_state(raw_state)

    _, info = agents[0].eval_step(state)

    return info['values']


def prepare_env(random_game=False):
    basedir = os.path.dirname(os.path.realpath(__file__))

    agents = []

    for gametype in ['D', 'G', 'N']:
        for i in range(0, 3):
            agents.append(load_model(basedir + "/../../models/latest/" + gametype + "_" + str(i) + ".pth"))

    if random_game:
        env = SkatEnv(blind_hand_chance=1.0, gametype='D')
    else:
        seed = 52
        set_seed(seed)
        env = SkatEnv(blind_hand_chance=1.0, seed=seed, gametype='D')

    env.set_agents(agents)

    raw_state, _ = env.game.init_game(blind_hand=True)

    return env, raw_state
