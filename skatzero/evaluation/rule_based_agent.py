from collections import Counter
import random

from skatzero.env.utils import compare_cards, get_points
from skatzero.evaluation.utils import format_hand

class RuleBasedAgent():

    def __init__(self):
        self.name = 'Rule Based Agent'

    def act(self, infoset):
        #print(format_hand(infoset.player_hand_cards))
        if infoset.player_position == 'soloplayer':
            if len(infoset.trick) == 0: # Trümpfe ziehen
                return self.try_to_play_trump(infoset)

        if infoset.player_position == 'opponent_right':
            if len(infoset.trick) == 0: # Dem Freunde kurz
                return self.play_short_suit(infoset)

        if infoset.player_position == 'opponent_left':
            if len(infoset.trick) == 0: # Dem Feinde lang
                return self.play_long_suit(infoset)

        if self.get_trick_value(infoset) >= 10:
            return self.try_to_play_higher_card(infoset)

        return random.choice(infoset.legal_actions)

    def try_to_play_trump(self, infoset):
        if 'CJ' in infoset.legal_actions:
            return 'CJ'
        if 'SJ' in infoset.legal_actions:
            return 'SJ'
        if 'HJ' in infoset.legal_actions:
            return 'HJ'
        if 'DJ' in infoset.legal_actions:
            return 'DJ'
        if infoset.trump + '9' in infoset.legal_actions:
            return infoset.trump + '9'
        if infoset.trump + '8' in infoset.legal_actions:
            return infoset.trump + '8'
        if infoset.trump + '7' in infoset.legal_actions:
            return infoset.trump + '7'
        if infoset.trump + 'Q' in infoset.legal_actions:
            return infoset.trump + 'Q'
        if infoset.trump + 'K' in infoset.legal_actions:
            return infoset.trump + 'K'
        if infoset.trump + 'A' in infoset.legal_actions:
            return infoset.trump + 'A'
        if infoset.trump + 'T' in infoset.legal_actions:
            return infoset.trump + 'T'
        return random.choice(infoset.legal_actions)

    def get_trick_value(self, infoset):
        value = 0
        if len(infoset.trick) >= 1:
            value += get_points(infoset.trick[0][1])
        if len(infoset.trick) == 2:
            value += get_points(infoset.trick[1][1])
        return value

    def try_to_play_higher_card(self, infoset):
        for action in infoset.legal_actions:
            if compare_cards(action, infoset.trick[0][1], infoset.trump, infoset.trick[0][1][0]):
                return action
        return random.choice(infoset.legal_actions)

    def play_long_suit(self, infoset):
        c = Counter(card[0] if card[0] != infoset.trump and card[1] != 'J' else '' for card in infoset.player_hand_cards)
        try:
            long_suit = c.most_common(1)[0][0]
            if long_suit == '':
                long_suit = c.most_common(1)[1][0]
            for action in infoset.legal_actions:
                if action[0] == long_suit:
                    return action
        except IndexError:
            pass
        return random.choice(infoset.legal_actions)

    def play_short_suit(self, infoset):
        c = Counter(card[0] if card[0] != infoset.trump and card[1] != 'J' else '' for card in infoset.player_hand_cards)
        try:
            short_suit = c.most_common()[-1][0]
            if short_suit == '':
                short_suit = c.most_common(1)[-2][0]
            for action in infoset.legal_actions:
                if action[0] == short_suit:
                    return action
        except IndexError:
            pass
        return random.choice(infoset.legal_actions)
