# -*- coding: utf-8 -*-
''' Implement Skat Player class
'''
from rlcard.games.skat.utils import cards2str


class SkatPlayer:
    ''' Player can store cards in the player's hand and the role,
    determine the actions that can be made according to the rules,
    and can perform corresponding action
    '''
    def __init__(self, player_id, np_random):
        ''' Give the player an id in one game

        Args:
            player_id (int): the player_id of a player

        Notes:
            1. role: A player's temporary role in one game(soloplayer or opponent)
            2. played_cards: The cards played in one round
            3. hand: Initial cards
            4. _current_hand: The rest of the cards after playing some of them
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.initial_hand = None
        self._current_hand = []
        self.role = ''
        self.played_cards = None

        #record cards removed from self._current_hand for each play()
        # and restore cards back to self._current_hand when play_back()
        self._recorded_played_cards = []

    @property
    def current_hand(self):
        return self._current_hand

    def set_current_hand(self, value):
        self._current_hand = value

    def get_state(self, public, others_hands, points, actions, trick):
        state = {}
        state['seen_cards'] = public['seen_cards']
        state['soloplayer'] = public['soloplayer']
        state['trace'] = public['trace'].copy()
        state['played_cards'] = public['played_cards']
        state['self'] = self.player_id
        state['current_hand'] = cards2str(self._current_hand)
        state['others_hand'] = others_hands
        state['points'] = points
        state['actions'] = actions
        state['trick'] = trick.copy()

        return state

    def available_actions(self, suit=None, judger=None):
        ''' Get the actions can be made based on the rules

        Args:
            suit: First played suit in this round
            judger (SkatJudger object): object of SkatJudger

        Returns:
            list: list of string of actions. Eg: ['8C', '9H', 'TH', 'JH']
        '''
        actions = judger.playable_cards_from_hand(self.current_hand, suit)
        return actions

    def play(self, action):
        ''' Perform action

        Args:
            action (string): specific action
        '''
        for _, remain_card in enumerate(self._current_hand):
            if remain_card.rank == action[0] and remain_card.suit == action[1]:
                self._current_hand.remove(self._current_hand[_])
                break
        self.played_cards = action
        self._recorded_played_cards.append(action)

    def play_back(self):
        ''' Restore recorded cards back to self._current_hand
        '''
        removed_card = self._recorded_played_cards.pop()
        self._current_hand.extend(removed_card)
