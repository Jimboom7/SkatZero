from skatzero.env.feature_transformations import convert_card_to_action_id, get_card_encoding
from skatzero.evaluation.utils import format_card

class HumanAgent():
    def __init__(self, num_actions):
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        _print_state(state['raw_obs'])
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegal...')
            action = int(input('>> Re-choose action (integer): '))
        card_encoding = get_card_encoding(state['raw_obs'])
        return convert_card_to_action_id(state['raw_legal_actions'][action], card_encoding)

    def eval_step(self, state):
        return self.step(state), {}


def _print_state(state):
    print('===============   Score    ===============')
    print(str(state['points'][0]) + ' - ' + str(state['points'][1]))
    print('\n=========== Actions You Can Choose ===========')
    print(', '.join([str(index) + ': ' + format_card(action) for index, action in enumerate(state['actions'])]))
    print('')
