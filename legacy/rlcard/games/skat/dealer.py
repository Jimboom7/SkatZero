# -*- coding: utf-8 -*-
''' Implement Skat Dealer class
'''

from rlcard.utils import init_32_deck
from rlcard.games.skat.utils import evalute_hand_strength

class SkatDealer:
    ''' Dealer will shuffle, deal cards, and determine players' roles
    '''
    def __init__(self, np_random):
        '''Give dealer the deck

        Notes:
            1. deck with 32 cards
        '''
        self.np_random = np_random
        self.deck = init_32_deck()
        #self.deck.sort(key=functools.cmp_to_key(skat_sort_card))
        self.soloplayer = None
        self.skat = None

    def shuffle(self):
        ''' Randomly shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deal cards to players

        Args:
            players (list): list of SkatPlayer objects
        '''
        hand_num = 10
        for index, player in enumerate(players):
            current_hand = self.deck[index*hand_num:(index+1)*hand_num]
            # current_hand.sort(key=functools.cmp_to_key(skat_sort_card))
            player.set_current_hand(current_hand)
            # player.initial_hand = cards2str(player.current_hand)

        # TODO: Dynamisch das zu spielende Spiel ermitteln. Momentan kriegt Spieler 1 die "beste" Hand
        if evalute_hand_strength(players[1].current_hand) > evalute_hand_strength(players[0].current_hand):
            tmp = players[0].current_hand
            players[0].set_current_hand(players[1].current_hand)
            players[1].set_current_hand(tmp)

        if evalute_hand_strength(players[2].current_hand) > evalute_hand_strength(players[0].current_hand):
            tmp = players[0].current_hand
            players[0].set_current_hand(players[2].current_hand)
            players[2].set_current_hand(tmp)
        self.skat = self.deck[-2:]
        return

        

    def determine_role(self, players):
        ''' Determine soloplayer and opponents according to players' hand

        Args:
            players (list): list of SkatPlayer objects

        Returns:
            int: soloplayers's player_id
        '''
        # deal cards
        self.shuffle()
        self.deal_cards(players)
        players[0].role = 'soloplayer'
        self.soloplayer = players[0]
        players[1].role = 'opponent'
        players[2].role = 'opponent'

        # TODO: Give the 'soloplayer' the skat
        return self.soloplayer.player_id
