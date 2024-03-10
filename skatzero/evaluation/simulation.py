import pickle
import random
from torch import multiprocessing as mp
import numpy as np

from skatzero.env.game import GameEnv
from skatzero.evaluation.random_agent import RandomAgent
from skatzero.evaluation.deep_agent import DeepAgent
from skatzero.evaluation.human_agent import HumanAgent
from skatzero.evaluation.rule_based_agent import RuleBasedAgent

def set_seed(seed):
    if seed is not None:
        import subprocess
        import sys

        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        if 'torch' in installed_packages:
            import torch
            torch.backends.cudnn.deterministic = True
            torch.manual_seed(seed)
        np.random.seed(seed)
        import random
        random.seed(seed)

def load_card_play_models(card_play_model_path_dict):
    players = {}

    for position in ['soloplayer', 'opponent_left', 'opponent_right']:
        if card_play_model_path_dict[position] == 'random':
            players[position] = RandomAgent()
        elif card_play_model_path_dict[position] == 'human':
            players[position] = HumanAgent()
        elif card_play_model_path_dict[position] == 'rulebased':
            players[position] = RuleBasedAgent()
        else:
            players[position] = DeepAgent(position, card_play_model_path_dict[position])
    return players

def mp_simulate(i, card_play_data_list, card_play_model_path_dict, q):
    print(f"Starting Simulation Agent {i}")
    players = load_card_play_models(card_play_model_path_dict)

    env = GameEnv(players)
    for _, card_play_data in enumerate(card_play_data_list):

        env.init_new_game(card_play_data)
        while not env.game_over:
            env.step()
        env.reset()

    q.put((env.num_wins['soloplayer'],
           env.num_wins['opponent'],
           env.sum_rewards['soloplayer'],
           env.sum_rewards['opponent']
         ))
    print(f"Finished Simulation Agent {i}")

def data_allocation_per_worker(card_play_data_list, num_workers):
    card_play_data_list_each_worker = [[] for _ in range(num_workers)]
    for idx, data in enumerate(card_play_data_list):
        card_play_data_list_each_worker[idx % num_workers].append(data)

    return card_play_data_list_each_worker

def evaluate(soloplayer, opponent_left, opponent_right, eval_data, num_workers, num_games):
    with open(eval_data, 'rb') as f:
        card_play_data_list = pickle.load(f)[:num_games]

    card_play_data_list_each_worker = data_allocation_per_worker(
        card_play_data_list, num_workers)
    del card_play_data_list

    model_path_dict = {
        'soloplayer': soloplayer,
        'opponent_left': opponent_left,
        'opponent_right': opponent_right}

    num_soloplayer_wins = 0
    num_opponent_wins = 0
    sum_soloplayer_scores = 0
    sum_opponent_scores = 0

    ctx = mp.get_context('spawn')
    q = ctx.SimpleQueue()
    processes = []
    for i, card_play_data in enumerate(card_play_data_list_each_worker):
        p = ctx.Process(target=mp_simulate, args=(i, card_play_data, model_path_dict, q))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    for _ in range(num_workers):
        result = q.get()
        num_soloplayer_wins += result[0]
        num_opponent_wins += result[1]
        sum_soloplayer_scores += result[2]
        sum_opponent_scores += result[3]

    num_total_wins = num_soloplayer_wins + num_opponent_wins
    print('Results for Soloplayer: ' + soloplayer)
    print('Opponents: ' + opponent_left)
    print(f'WINS:   Soloplayer : Opponents | {num_soloplayer_wins / num_total_wins} : {num_opponent_wins / num_total_wins}')
    print(f'SCORES: Soloplayer : Opponents | {sum_soloplayer_scores / num_total_wins} : {sum_opponent_scores / num_total_wins}')
    return sum_soloplayer_scores / num_total_wins

def save_evaluation_duel(checkpoint_dir, model, frames, num_workers, num_games, hand_quality, blind_hand_chance):
    soloplayer = checkpoint_dir + model + "/soloplayer_" + frames + ".pth"
    opponent_left = checkpoint_dir + model + "/opponent_left_" + frames + ".pth"
    opponent_right = checkpoint_dir + model + "/opponent_right_" + frames + ".pth"
    eval_data = "eval_data_" + hand_quality + "_" + blind_hand_chance + ".pkl"
    rewards1 = evaluate(soloplayer,
             "random",
             "random",
             eval_data,
             num_workers,
             num_games)

    rewards2 = evaluate("random",
             opponent_left,
             opponent_right,
             eval_data,
             num_workers,
             num_games)

    print("Card Quality: " + str(hand_quality) + ", Blind Hand Chance: " + str(blind_hand_chance))
    print("Evaluation Score: " + str(round(rewards1 - rewards2, 2)))
    with open(checkpoint_dir + "evaluate_log.csv", "a", encoding='utf-8') as logfile:
        logfile.write(str(model) + "," + str(frames) + "," + str(num_games) + "," + str(hand_quality) + "," + str(blind_hand_chance) + "," + str(round(rewards1 - rewards2, 2)) + "\n")


def sample(eval_data, p1, p2, p3, random_game=False):
    card_play_model_path_dict = {
        'soloplayer': p1,
        'opponent_left': p2,
        'opponent_right': p3}

    players = load_card_play_models(card_play_model_path_dict)
    with open(eval_data, 'rb') as f:
        card_play_data_list = pickle.load(f)

    if random_game:
        random.shuffle(card_play_data_list)

    env = GameEnv(players)
    cards = card_play_data_list[0]

    infosets = []
    infosets.append(env.init_new_game(cards))
    while not env.game_over:
        infosets.append(env.step())
    return infosets

def bidding(eval_data, p1, p2, p3, random_game=False):
    card_play_model_path_dict = {
        'soloplayer': p1,
        'opponent_left': p2,
        'opponent_right': p3}

    players = load_card_play_models(card_play_model_path_dict)
    with open(eval_data, 'rb') as f:
        card_play_data_list = pickle.load(f)

    if random_game:
        random.shuffle(card_play_data_list)

    env = GameEnv(players)
    cards = card_play_data_list[0]
    cards['hand'] = True

    infoset = env.init_new_game(cards)

    values = players['soloplayer'].get_all_action_values(infoset)

    return values, infoset.legal_actions
