import random

from skatzero.env.utils import format_hand

class RandomAgent():

    def __init__(self):
        self.name = 'Random'

    def act(self, infoset):
        #print(format_hand(infoset.player_hand_cards))
        return random.choice(infoset.legal_actions)
