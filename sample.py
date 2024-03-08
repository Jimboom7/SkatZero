''' An sample of playing skat randomly. Good for checking the internal values of the game, observation data etc.
'''
import numpy as np
from skatzero.env.utils import print_hand

from skatzero.evaluation.simulation import sample
from skatzero.env.env import get_obs

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

if __name__ == '__main__':
    set_seed(42)

    CHECKPOINT_DIR = "checkpoints/skat_0"
    FRAMES = "50035200"
    SOLOPLAYER = CHECKPOINT_DIR + "/soloplayer_" + FRAMES + ".pth"
    #OPPONENT_LEFT = CHECKPOINT_DIR + "/opponent_left_" + FRAMES + ".pth"
    #OPPONENT_RIGHT = CHECKPOINT_DIR + "/opponent_right_" + FRAMES + ".pth"
    # SOLOPLAYER = "random"
    OPPONENT_LEFT = "random"
    OPPONENT_RIGHT = "random"

    game_infosets = sample('eval_data.pkl', SOLOPLAYER, OPPONENT_LEFT, OPPONENT_RIGHT)

    for game_infoset in game_infosets[:-1]:
        obs = get_obs(game_infoset)
        print('Player')
        print(obs['position'])
        print('Card Sequence')
        print(game_infoset.card_play_action_seq)
        print('Trick')
        print(game_infoset.trick)
        print('Hand Cards')
        print_hand(game_infoset.player_hand_cards)
        # print('Other Hand Cards')
        # print(game_infoset.other_hand_cards)
        # print('Played Cards')
        # print(game_infoset.played_cards)
        print('Score')
        print(str(game_infoset.score['soloplayer']) + " - " + str(game_infoset.score['opponent']))
        #print('Legal Moves')
        #print(game_infoset.legal_actions)
        print('State Size')
        print(str(obs['x_batch'].size))
        print("")
