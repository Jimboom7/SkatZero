# -*- coding: utf-8 -*-
''' Implement Skat Round class
'''

from rlcard.games.skat import Dealer
from rlcard.games.skat.utils import CARD_SUIT_STR, cards2str, get_points
from rlcard.games.skat.utils import CARD_RANK_STR, CARD_RANK_STR_INDEX, CARD_SUIT_STR_INDEX

class SkatRound:
    ''' Round can call other Classes' functions to keep the game running
    '''
    def __init__(self, np_random, played_cards):
        self.np_random = np_random
        self.played_cards = played_cards
        self.trace = []

        self.current_player = None
        self.soloplayer_id = 0
        self.public = None
        self.seen_cards = ''
        self.current_suit = None
        self.current_trick = None
        self.solo_points = 0
        self.opponent_points = 0

        self.trump = None

        self.dealer = Dealer(self.np_random)
        self.deck_str = cards2str(self.dealer.deck)

    def initiate(self, players):
        ''' Call dealer to deal cards and bid soloplayer.

        Args:
            players (list): list of SkatPlayer objects
        '''
        soloplayer_id = self.dealer.determine_role(players)
        self.seen_cards = ''
        self.soloplayer_id = soloplayer_id
        self.current_player = soloplayer_id
        self.public = {'deck': self.deck_str, 'seen_cards': self.seen_cards, 'soloplayer': self.soloplayer_id,
                       'trace': self.trace, 'played_cards': ['' for _ in range(len(players))]}
        self.current_suit = None
        self.current_trick = []
        self.solo_points = get_points(str(self.dealer.skat[0])) + get_points(str(self.dealer.skat[1]))
        self.opponent_points = 0
        self.trump = "D" # TODO: Hardcoded for now -> Dynamisch ermitteln (Beste Farbe des Spielers?), und dann aber auch die Observation entsprechend codieren (und actions)

    @staticmethod
    def cards_ndarray_to_str(ndarray_cards):
        result = []
        for cards in ndarray_cards:
            _result = []
            for i, x in enumerate(cards):
                for j, _ in enumerate(x):
                    if cards[i][j] != 0:
                        _result.extend([CARD_RANK_STR[j]] + [CARD_SUIT_STR[i]])
            result.append(''.join(_result))
        return result

    def update_public(self, action):
        ''' Update public trace and played cards

        Args:
            action(str): string of legal specific action
        '''
        self.trace.append((self.current_player, action))
        self.played_cards[self.current_player][CARD_SUIT_STR_INDEX[action[1]]][CARD_RANK_STR_INDEX[action[0]]] = 1
        self.seen_cards += action
        self.public['seen_cards'] = self.seen_cards
        self.public['played_cards'] = self.cards_ndarray_to_str(self.played_cards)

    def proceed_round(self, player, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of SkatPlayer
            action (str): string of legal specific action

        Returns:
            object of SkatPlayer: player who played current biggest cards.
        '''
        self.update_public(action)
        player.play(action)

        self.current_trick.append((player, action))

        if len(self.current_trick) == 1:
            self.current_suit = action[1]
            if action[0] == "J":
                self.current_suit = self.trump

    def step_back(self, players):
        ''' Reverse the last action

        Args:
            players (list): list of SkatPlayer objects
        Returns:
            The last player id and the card played

            NOT USED BY DCM ALGORITHM
        '''
        player_id, card = self.trace.pop()
        self.current_player = player_id
        self.played_cards[player_id][CARD_SUIT_STR_INDEX[card]][CARD_RANK_STR_INDEX[card]] = 0
        self.public['played_cards'] = self.cards_ndarray_to_str(self.played_cards)

        return player_id, card

    def find_last_played_card_in_trace(self, player_id):
        ''' Find the player_id's last played_card in trace

        Returns:
            The player_id's last played_card in trace
        '''
        for i in range(len(self.trace) - 1, -1, -1):
            _id, action = self.trace[i]
            if _id == player_id:
                return action
        return None
