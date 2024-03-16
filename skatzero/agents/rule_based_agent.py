from collections import Counter
import random

from skatzero.env.feature_transformations import convert_card_to_action_id, get_card_encoding
from skatzero.game.utils import compare_cards, get_points

class RuleBasedAgent():

    def __init__(self, num_actions):
        self.num_actions = num_actions

    def step(self, state):
        action = self.get_action(state['raw_obs'])

        if action is None:
           action = random.choice(state['raw_obs']['actions'])

        card_encoding = get_card_encoding(state['raw_obs'])

        return convert_card_to_action_id(action, card_encoding)

    def eval_step(self, state):
        return self.step(state), {}

    def get_action(self, state):
        if state['self'] == 0:
            if len(state['trick']) == 0: # Trümpfe ziehen
                return self.try_to_play_trump(state['trick'])

        if state['self'] == 1:
            if len(state['trick']) == 0: # Dem Freunde kurz
                return self.play_short_suit(state)

        if state['self'] == 2:
            if len(state['trick']) == 0: # Dem Feinde lang
                return self.play_long_suit(state)

        if self.get_trick_value(state) >= 10:
            return self.try_to_play_higher_card(state)

        return None

    def try_to_play_trump(self, state):
        if 'CJ' in state['actions']:
            return 'CJ'
        if 'SJ' in state['actions']:
            return 'SJ'
        if 'HJ' in state['actions']:
            return 'HJ'
        if 'DJ' in state['actions']:
            return 'DJ'
        if state['trump'] + '9' in state['actions']:
            return state['trump'] + '9'
        if state['trump'] + '8' in state['actions']:
            return state['trump'] + '8'
        if state['trump'] + '7' in state['actions']:
            return state['trump'] + '7'
        if state['trump'] + 'Q' in state['actions']:
            return state['trump'] + 'Q'
        if state['trump'] + 'K' in state['actions']:
            return state['trump'] + 'K'
        if state['trump'] + 'A' in state['actions']:
            return state['trump'] + 'A'
        if state['trump'] + 'T' in state['actions']:
            return state['trump'] + 'T'
        return random.choice(state['actions'])

    def get_trick_value(self, state):
        value = 0
        if len(state['trick']) >= 1:
            value += get_points(state['trick'][0][1])
        if len(state['trick']) == 2:
            value += get_points(state['trick'][1][1])
        return value

    def try_to_play_higher_card(self, state):
        for action in state['actions']:
            if compare_cards(action, state['trick'][0][1], state['trump'], state['trick'][0][1][0]):
                return action
        return random.choice(state['actions'])

    def play_long_suit(self, state):
        c = Counter(card[0] if card[0] != state['trump'] and card[1] != 'J' else '' for card in state['current_hand'])
        try:
            long_suit = c.most_common(1)[0][0]
            if long_suit == '':
                long_suit = c.most_common(1)[1][0]
            for action in state['actions']:
                if action[0] == long_suit:
                    return action
        except IndexError:
            pass
        return random.choice(state['actions'])

    def play_short_suit(self, state):
        c = Counter(card[0] if card[0] != state['trump'] and card[1] != 'J' else '' for card in state['current_hand'])
        try:
            short_suit = c.most_common()[-1][0]
            if short_suit == '':
                short_suit = c.most_common(1)[-2][0]
            for action in state['actions']:
                if action[0] == short_suit:
                    return action
        except IndexError:
            pass
        return random.choice(state['actions'])
