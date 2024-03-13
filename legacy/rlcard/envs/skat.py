from collections import OrderedDict
import numpy as np

from rlcard.envs import Env

from rlcard.games.skat.utils import action_2_id, cards2str, id_2_action
from rlcard.games.skat import Game

class SkatEnv(Env):
    ''' Skat Environment
    '''

    def __init__(self, config):
        self._cards2str = cards2str

        self.name = 'skat'
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[1490], [1522], [1522]]
        self.action_shape = [[32] for _ in range(self.num_players)]

    def _extract_state(self, state):
        ''' Encode state

        Args:
            state (dict): dict of original state
        '''
        current_hand = _cards2array(state['current_hand'])
        others_hand = _cards2array(state['others_hand'])

        all_actions = _action_seq2array(_process_action_seq(state['trace']))
        #short_actions = _action_seq2array_short(_process_action_seq_short(state['trace'], self.game.round.winners))

        trick1 = _cards2array(None)
        trick2 = _cards2array(None)
        if len(state['trick']) >= 1:
            trick1 = _cards2array(state['trick'][0][1])
        if len(state['trick']) == 2:
            trick2 = _cards2array(state['trick'][1][1])

        if state['self'] == state['soloplayer']: # soloplayer
            soloplayer_up_played_cards = _cards2array(state['played_cards'][2])
            soloplayer_down_played_cards = _cards2array(state['played_cards'][1])

            missing_cards_up = _calculate_missing_cards(state['others_hand'], 2, state['trace'], self.game.round.trump)
            missing_cards_down = _calculate_missing_cards(state['others_hand'], 1, state['trace'], self.game.round.trump)

            points_own = _get_points_as_one_hot_vector(state['points'][0])
            points_opp = _get_points_as_one_hot_vector(state['points'][1])
            
            skat = _cards2array(str(self.game.round.dealer.skat[0]) + str(self.game.round.dealer.skat[1]))
            obs = np.concatenate((current_hand, # 32
                                  others_hand, # 32
                                  trick1, # 32
                                  trick2, # 32
                                  skat, #32
                                  all_actions, # 32*30
                                  missing_cards_up, # 32
                                  soloplayer_up_played_cards, # 32
                                  missing_cards_down, # 32
                                  soloplayer_down_played_cards, # 32
                                  points_own, # 121
                                  points_opp)) # 121
        else:
            soloplayer_played_cards = _cards2array(state['played_cards'][0]) 
            for i, action in reversed(state['trace']):
                if i == state['soloplayer']:
                    last_soloplayer_action = action
                    break
            last_soloplayer_action = _cards2array(last_soloplayer_action)

            teammate_id = 3 - state['self']

            missing_cards_solo = _calculate_missing_cards(state['others_hand'], 0, state['trace'], self.game.round.trump)
            missing_cards_teammate = _calculate_missing_cards(state['others_hand'], teammate_id, state['trace'], self.game.round.trump)

            points_own = _get_points_as_one_hot_vector(state['points'][1])
            points_opp = _get_points_as_one_hot_vector(state['points'][0])

            teammate_played_cards = _cards2array(state['played_cards'][teammate_id])
            last_teammate_action = None
            for i, action in reversed(state['trace']):
                if i == teammate_id:
                    last_teammate_action = action
                    break
            last_teammate_action = _cards2array(last_teammate_action)
            obs = np.concatenate((current_hand, # 32
                                  others_hand, # 32
                                  trick1, # 32
                                  trick2, # 32
                                  all_actions, # 32*30
                                  missing_cards_solo, # 32
                                  soloplayer_played_cards, # 32
                                  missing_cards_teammate, # 32
                                  teammate_played_cards, # 32
                                  last_soloplayer_action, # 32
                                  last_teammate_action, # 32
                                  points_own, # 121
                                  points_opp)) # 121

        extracted_state = OrderedDict({'obs': obs, 'legal_actions': self._get_legal_actions()})
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['actions']]
        extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.

        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        return self.game.judger.judge_payoffs(self.game.round.soloplayer_id, self.game.round.solo_points)

    def _decode_action(self, action_id):
        ''' Action id -> the action in the game. Must be implemented in the child class.

        Args:
            action_id (int): the id of the action

        Returns:
            action (string): the action that will be passed to the game engine.
        '''
        return id_2_action(action_id)

    def _get_legal_actions(self):
        ''' Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_actions = self.game.state['actions']
        legal_actions = {action_2_id(action): _cards2array(action) for action in legal_actions}
        return legal_actions

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['hand_cards_with_suit'] = [self._cards2str(player.current_hand) for player in self.game.players]
        state['hand_cards'] = [self._cards2str(player.current_hand) for player in self.game.players]
        state['trace'] = self.game.state['trace']
        state['current_player'] = self.game.round.current_player
        state['legal_actions'] = self.game.state['actions']
        return state

    def get_action_feature(self, action):
        ''' For some environments such as Skat, we can have action features

        Returns:
            (numpy.array): The action features
        '''
        return _cards2array(self._decode_action(action))

CardSuit2Column = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
Card2Column = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}

def _cards2array(cards):
    matrix = np.zeros([4, 8], dtype=np.int8)
    if cards is None:
        return matrix.flatten('F')
    it = iter(cards)
    for x in it:
        matrix[CardSuit2Column[next(it)], Card2Column[x]] = 1
    return matrix.flatten('F')

def _card2array_short(card, owner, winner):
    matrix = np.zeros([17], dtype=np.int8)
    if card is None or card == '':
        return matrix
    matrix[CardSuit2Column[card[1]]] = 1
    matrix[4 + Card2Column[card[0]]] = 1
    matrix[11 + owner] = 1
    matrix[14 + winner] = 1
    return matrix

def _get_points_as_one_hot_vector(points, max_points=120):
    one_hot = np.zeros(max_points + 1, dtype=np.int8)
    one_hot[points] = 1
    return one_hot

def _get_binary_points(points, max_len=7):
    return np.array([int(i) for i in bin(points)[2:].zfill(max_len)])

def _action_seq2array(action_seq_list):
    action_seq_array = np.zeros((len(action_seq_list), 32), np.int8)
    for row, cards in enumerate(action_seq_list):
        action_seq_array[row, :] = _cards2array(cards)
    action_seq_array = action_seq_array.flatten()
    return action_seq_array

def _action_seq2array_short(action_seq_list):
    action_seq_array = np.zeros((len(action_seq_list), 17), np.int8)
    for row, actions in enumerate(action_seq_list):
        card = actions[0]
        owner = actions[1]
        winner = actions[2]
        action_seq_array[row, :] = _card2array_short(card, owner, winner)
    action_seq_array = action_seq_array.flatten()
    return action_seq_array

def _process_action_seq(sequence, length=30):
    sequence = [action[1] for action in sequence[-length:]]
    if len(sequence) % 3 == 1:
        sequence.append('')
        sequence.append('')
    if len(sequence) % 3 == 2:
        sequence.append('')
    if len(sequence) < length:
        empty_sequence = ['' for _ in range(length - len(sequence))]
        empty_sequence.extend(sequence)
        sequence = empty_sequence
    return sequence

def _process_action_seq_short(sequence, winners, length=30):
    sequence = [[action[1], action[0], -1] for action in sequence[-length:]]
    j=0
    for i in range(0, len(sequence)-2, 3):
        sequence[i][2] = winners[j]
        sequence[i+1][2] = winners[j]
        sequence[i+2][2] = winners[j]
        j += 1
    sequence = sequence[:len(sequence) - (len(sequence) % 3)] # Only full tricks
    empty_sequence = [('', -1, -1) for _ in range(length - len(sequence))]
    empty_sequence.extend(sequence)
    sequence = empty_sequence
    return sequence

def _calculate_missing_cards(others_hand, player_id, trace, trump):
    matrix = np.zeros([4, 8], dtype=np.int8)
    it = iter(others_hand)
    trick_counter = 0
    for player, card in trace:
        trick_counter += 1
        if player == player_id:
            player_card = card
        if trick_counter % 3 == 1:
            base_card = card
        if trick_counter % 3 == 0:
            if (player_card[1] == base_card[1]
                or ((player_card[0] == 'J' or player_card[1] == trump) and
                (base_card[0] == 'J' or base_card[1] == trump))):
                continue
            if base_card[0] == 'J' or base_card[1] == trump:
                matrix[CardSuit2Column[trump], :7] = 1
                matrix[:, 7] = 1
            else:
                matrix[CardSuit2Column[base_card[1]], :7] = 1
    return matrix.flatten('F')
