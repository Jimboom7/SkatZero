import copy
import time
import os
import subprocess
import sys
import random

import numpy as np
import torch
from torch import multiprocessing as mp

from iss.SkatMatch import SkatMatch
from skatzero.agents.random_agent import RandomAgent
from skatzero.agents.human_agent import HumanAgent
from skatzero.agents.rule_based_agent import RuleBasedAgent
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.eval_env import EvalEnv
from skatzero.evaluation.utils import parse_bid, swap_bids, swap_colors
from skatzero.game.dealer import Dealer

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


def save_evaluation_duel(folder, folder2, model1, model2, num_games, num_actors=10, gametype='D', seed='42', dealer_from_log=True):
    print("Starting Evaluation")
    base_folder = 'models/checkpoints/'
    folder = str(folder)
    folder2 = str(folder2)
    number1 = str(model1)
    number2 = str(model2)

    models_solo = [
            base_folder + folder + '/0_' + number1 + '.pth',
            base_folder + folder2 + '/1_' + number2 + '.pth',
            base_folder + folder2 + '/2_' + number2 + '.pth'
        ]
    models_opponent = [
            base_folder + folder2 + '/0_' + number2 + '.pth',
            base_folder + folder + '/1_' + number1 + '.pth',
            base_folder + folder + '/2_' + number1 + '.pth'
        ]

    if number2 == 'random':
        models_solo[1] = 'random'
        models_solo[2] = 'random'
        models_opponent[0] = 'random'

    lstm_1 = 'lstm' in folder
    lstm_2 = 'lstm' in folder2

    set_seed(seed)

    dealers = None
    if dealer_from_log:
        print("Reading log file...")
        dealers = []
        for line in list(open('C:/Users/janvo/Desktop/Skat/skatgame-games-07-2024/high_elo_' + gametype +'.txt', encoding='utf-8')):
            try:
                match = SkatMatch(line)
                if not match.eingepasst and (gametype == match.gameType[0] or (gametype == 'D' and match.gameType[0] in ['H', 'S', 'C'])):
                    if match.playerElos[0] > 800 and match.playerElos[1] > 800 and match.playerElos[2] > 800:
                        dealer = set_dealer_data(match, gametype)
                        dealers.append(dealer)
                        if len(dealers) > 10000:
                            break
            except:
                pass
        if len(dealers) < num_games:
            num_games = len(dealers)

    env = EvalEnv(seed=seed, gametype=gametype, lstm=[lstm_1, lstm_2, lstm_2], dealers=dealers)

    # Evaluation 1: Soloplayer
    agents = []
    for _, model_path in enumerate(models_solo):
        agents.append(load_model(model_path))
    env.set_agents(agents)
    rewards = tournament(env, num_games, num_actors, seed)
    for position, reward in enumerate(rewards):
        print(position, models_solo[position], reward)

    set_seed(seed)
    env = EvalEnv(seed=seed, gametype=gametype, lstm=[lstm_2, lstm_1, lstm_1], dealers=dealers)

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
        logfile.write(str(folder) + "," + str(number1) + "," + str(number2) + "," + str(num_games) + "," +
                      str(round(rewards[0] - rewards2[0], 2)) + "," + str(round(rewards[0], 2)) + "," + str(round(rewards2[0], 2)) + "," + str(dealer_from_log) + "\n")
    return rewards[0], rewards2[0]

def set_dealer_data(match, gametype):
    dealer = Dealer(None)
    dealer.starting_player = (3 - match.alleinspielerInd) % 3

    dealer.deck = match.cards[match.playerNames[match.alleinspielerInd]]
    dealer.deck += match.originalSkat
    dealer.deck = [a for a in dealer.deck if a not in match.gedrueckt_cards]
    dealer.deck += match.cards[match.playerNames[(match.alleinspielerInd + 1) % 3]]
    dealer.deck += match.cards[match.playerNames[(match.alleinspielerInd + 2) % 3]]
    dealer.deck += match.gedrueckt_cards

    dealer.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    dealer.bid_jacks = [0, 0, 0]
    dealer.bids, dealer.bid_jacks = parse_bid(match.maxReizungen[(match.alleinspielerInd + 1) % 3], 1, dealer.bids, dealer.bid_jacks)
    dealer.bids, dealer.bid_jacks = parse_bid(match.maxReizungen[(match.alleinspielerInd + 2) % 3], 2, dealer.bids, dealer.bid_jacks)

    if gametype == 'D' and match.gameType[0] != 'D':
        dealer.deck = swap_colors(dealer.deck, 'D', match.gameType[0])
        dealer.bids[0] = swap_bids(dealer.bids[0], 'D', match.gameType[0])
        dealer.bids[1] = swap_bids(dealer.bids[1], 'D', match.gameType[0])
        dealer.bids[2] = swap_bids(dealer.bids[2], 'D', match.gameType[0])

    dealer.blind_hand = match.is_hand
    dealer.open_hand = False

    return dealer

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

    #state, _ = env.reset(always_solo=True)

    raw_state, _ = env.game.init_game()

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
        env = SkatEnv(gametype='D')
    else:
        seed = 52
        set_seed(seed)
        env = SkatEnv(seed=seed, gametype='D')

    env.set_agents(agents)

    raw_state, _ = env.game.init_game()
    env.game.round.blind_hand = True
    env.game.round.open_hand = False
    raw_state['blind_hand'] = True
    raw_state['open_hand'] = False
    raw_state['points'] = [0, 0]

    return env, raw_state
