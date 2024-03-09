from skatzero.env.utils import compare_cards
from skatzero.evaluation.utils import format_card, format_hand


class HumanAgent():
    ''' A human agent for Skat. It can be used to play against trained models
    '''

    def __init__(self):
        self.name = 'Human Player'

    def act(self, infoset):
        ''' Human agent will display the state and make decisions through the interface

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        self.print_state(infoset)
        action = int(input('>> You choose action (Number): ')) - 1
        while action < 0 or action >= len(infoset.legal_actions):
            print('Action illegal...')
            action = int(input('>> Re-choose action (Number): '))
        return infoset.legal_actions[action]


    def print_state(self, infoset):
        ''' Print out important information

        Args:
            infoset
        '''
        try:
            last_player_action = [x for x, y in enumerate(infoset.card_play_action_seq[::1]) if y[0] == infoset.player_position][-1]
        except IndexError:
            last_player_action = -1
        if last_player_action != -1 and (last_player_action - 1) % 3 == 1:
            self.check_trick(infoset.card_play_action_seq[(round(last_player_action/3)*3):], infoset.trump)
        for i, play in enumerate(infoset.card_play_action_seq[(last_player_action+1):]):
            print(play[0] + " throws " + format_card(play[1]))
            if (last_player_action + i) % 3 == 1:
                self.check_trick(infoset.card_play_action_seq[(round(last_player_action/3)*3):], infoset.trump)

        print('===============   Current Trick   ===============')
        print(', '.join([format_card(card) for _, card in infoset.trick]))
        print('===============      Score      ===============')
        print(str(infoset.score['soloplayer']) + ' - ' + str(infoset.score['opponent']))
        print('===============   Your Cards    ===============')
        print(format_hand(infoset.player_hand_cards))
        print('\n=========== Actions You Can Choose ===========')
        print(', '.join([str(i + 1) + ': ' + format_card(action) for i, action in enumerate(infoset.legal_actions)]))
        print('')

    def check_trick(self, trick, trump):
        suit = trick[0][1][0]
        trick_winner = trick[0][0]
        card1 = trick[0][1]
        card2 = trick[1][1]
        card3 = trick[2][1]
        highest_card = card1
        if not compare_cards(card1, card2, trump, suit):
            highest_card = card2
            trick_winner = trick[1][0]
        if not compare_cards(highest_card, card3, trump, suit):
            trick_winner = trick[2][0]
        print(trick_winner + " wins the Trick: " + format_card(card1) + ", " + format_card(card2) + ", " + format_card(card3))
