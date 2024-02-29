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
        self.state_shape = [[690], [754], [754]]
        self.action_shape = [[32] for _ in range(self.num_players)]

    def _extract_state(self, state):
        ''' Encode state

        Args:
            state (dict): dict of original state
        '''
        current_hand = _cards2array(state['current_hand'])
        others_hand = _cards2array(state['others_hand'])

        last_action = ''
        if len(state['trace']) != 0:
            last_action = state['trace'][-1][1]
        last_action = _cards2array(last_action)

        last_9_actions = _action_seq2array(_process_action_seq(state['trace']))

        if state['self'] == 0: # soloplayer
            soloplayer_up_played_cards = _cards2array(state['played_cards'][2])
            soloplayer_down_played_cards = _cards2array(state['played_cards'][1])
            points_own = get_points_as_one_hot_vector(state['points'][0])
            points_opp = get_points_as_one_hot_vector(state['points'][1])
            obs = np.concatenate((current_hand,
                                  others_hand,
                                  last_action,
                                  last_9_actions,
                                  soloplayer_up_played_cards,
                                  soloplayer_down_played_cards,
                                  points_own,
                                  points_opp))
        else:
            soloplayer_played_cards = _cards2array(state['played_cards'][0])
            for i, action in reversed(state['trace']):
                if i == 0:
                    last_soloplayer_action = action
                    break
            last_soloplayer_action = _cards2array(last_soloplayer_action)
            points_own = get_points_as_one_hot_vector(state['points'][1])
            points_opp = get_points_as_one_hot_vector(state['points'][0])

            teammate_id = 3 - state['self']
            teammate_played_cards = _cards2array(state['played_cards'][teammate_id])
            last_teammate_action = None
            for i, action in reversed(state['trace']):
                if i == teammate_id:
                    last_teammate_action = action
                    break
            last_teammate_action = _cards2array(last_teammate_action)
            obs = np.concatenate((current_hand,
                                  others_hand,
                                  last_action,
                                  last_9_actions,
                                  soloplayer_played_cards,
                                  teammate_played_cards,
                                  last_soloplayer_action,
                                  last_teammate_action,
                                  points_own,
                                  points_opp))

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

def get_points_as_one_hot_vector(points, max_points=120):
    one_hot = np.zeros(max_points + 1, dtype=np.int8)
    one_hot[points] = 1
    return one_hot

def _action_seq2array(action_seq_list):
    action_seq_array = np.zeros((len(action_seq_list), 32), np.int8)
    for row, cards in enumerate(action_seq_list):
        action_seq_array[row, :] = _cards2array(cards)
    action_seq_array = action_seq_array.flatten()
    return action_seq_array

def _process_action_seq(sequence, length=9):
    sequence = [action[1] for action in sequence[-length:]]
    if len(sequence) < length:
        empty_sequence = ['' for _ in range(length - len(sequence))]
        empty_sequence.extend(sequence)
        sequence = empty_sequence
    return sequence
