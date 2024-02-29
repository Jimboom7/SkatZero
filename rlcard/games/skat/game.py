# -*- coding: utf-8 -*-
''' Implement Skat Game class
'''
import functools
from heapq import merge
import numpy as np

from rlcard.games.skat.utils import CARD_SUIT_STR, cards2str, get_points, skat_sort_card, CARD_RANK_STR
from rlcard.games.skat import Player
from rlcard.games.skat import Round
from rlcard.games.skat import Judger


class SkatGame:
    ''' Provide game APIs for env to run skat and get corresponding state information.
    '''
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 3
        self.done = False
        self.history = []
        self.players = []
        self.played_cards = []
        self.round = None
        self.judger = None
        self.state = None

    def init_game(self):
        ''' Initialize players and state.

        Returns:
            dict: first state in one game
            int: current player's id
        '''
        # initialize public variables
        self.done = False
        self.history = []

        # initialize players
        self.players = [Player(num, self.np_random)
                        for num in range(self.num_players)]

        # initialize round to deal cards and determine soloplayer
        self.played_cards = [np.zeros((len(CARD_SUIT_STR), len(CARD_RANK_STR)), dtype=np.int32)
                                for _ in range(self.num_players)]
        self.round = Round(self.np_random, self.played_cards)
        self.round.initiate(self.players)

        # initialize judger
        self.judger = Judger()

        # get state of first player
        player_id = self.round.current_player
        self.state = self.get_state(player_id)

        return self.state, player_id

    def step(self, action):
        ''' Perform one draw of the game

        Args:
            action (str): specific action of skat. Eg: '7C'

        Returns:
            dict: next player's state
            int: next player's id
        '''
        if self.allow_step_back:
            pass

        # perform action
        player = self.players[self.round.current_player]
        self.round.proceed_round(player, action)

        next_id = self.judger.judge_trick(self.round)

        if self.judger.judge_game(self.players):
            self.done = True
        if next_id == -1:
            next_id = (player.player_id + 1) % len(self.players)
        self.round.current_player = next_id

        # get next state
        state = self.get_state(next_id)
        self.state = state

        return state, next_id

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.round.trace:
            return False

        #done will be always None no matter step_back from any case
        self.done = False

        #reverse round
        player_id, _ = self.round.step_back(self.players)

        #reverse player
        self.players[player_id].played_cards = self.round.find_last_played_card_in_trace(player_id)
        self.players[player_id].play_back()

        self.state = self.get_state(self.round.current_player)
        return True

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        player = self.players[player_id]
        others_hands = self._get_others_current_hand(player)
        solo_points = self.round.solo_points
        if player_id != self.round.soloplayer_id:
            solo_points -= (get_points(str(self.round.dealer.skat[0])) + get_points(str(self.round.dealer.skat[1])))
        points = [solo_points, self.round.opponent_points]
        if self.is_over():
            actions = []
        else:
            actions = list(player.available_actions(self.round.current_suit, self.judger))
        state = player.get_state(self.round.public, others_hands, points, actions)

        return state

    @staticmethod
    def get_num_actions():
        ''' Return the total number of abstract actions

        Returns:
            int: the total number of abstract actions of skat
        '''
        return 32

    def get_player_id(self):
        ''' Return current player's id

        Returns:
            int: current player's id
        '''
        return self.round.current_player

    def get_num_players(self):
        ''' Return the number of players in skat

        Returns:
            int: the number of players in skat
        '''
        return self.num_players

    def is_over(self):
        ''' Judge whether a game is over

        Returns:
            Bool: True(over) / False(not over)
        '''
        return self.done

    def _get_others_current_hand(self, player):
        player_up = self.players[(player.player_id+1) % len(self.players)]
        player_down = self.players[(player.player_id-1) % len(self.players)]
        others_hand = merge(player_up.current_hand, player_down.current_hand, key=functools.cmp_to_key(skat_sort_card)) #TODO: Remove sort and merge with other method
        if player.player_id != self.round.soloplayer_id: # Add Skat as possible unknown cards
            others_hand = merge(others_hand, self.round.dealer.skat, key=functools.cmp_to_key(skat_sort_card))
        return cards2str(others_hand)
