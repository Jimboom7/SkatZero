from skatzero.env.feature_transformations import convert_card_to_action_id, get_card_encoding
from skatzero.evaluation.utils import format_card, format_hand
from skatzero.game.utils import compare_cards

class HumanAgent():
    def __init__(self, num_actions):
        self.num_actions = num_actions

    def step(self, state):
        self.print_state(state['raw_obs'])
        action = int(input('>> You choose action (integer): ')) - 1
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegal...')
            action = int(input('>> Re-choose action (integer): ')) - 1
        card_encoding = get_card_encoding(state['raw_obs'])
        return convert_card_to_action_id(state['raw_legal_actions'][action], card_encoding)

    def eval_step(self, state):
        return self.step(state), {}


    def print_state(self, state):
        print('===============   Current Trick   ===============')
        print(', '.join([format_card(card) for _, card in state['trick']]))
        print('===============      Score      ===============')
        print(str(state['points'][0]) + ' - ' + str(state['points'][1]))
        print('===============   Your Cards    ===============')
        print(format_hand(state['current_hand']))
        print('\n=========== Actions You Can Choose ===========')
        print(', '.join([str(i + 1) + ': ' + format_card(action) for i, action in enumerate(state['actions'])]))
        print('')

    def player_number_to_name(self, own, nr):
        if nr == own:
            return 'You'
        player = 'Soloplayer'
        if nr == 1:
            player = 'Opponent Right'
            if own:
                player = 'Teammate'
        elif nr == 2:
            player = 'Opponent Left'
            if own:
                player = 'Teammate'
        return player
