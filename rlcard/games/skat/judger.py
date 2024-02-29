# -*- coding: utf-8 -*-
''' Implement Skat Judger class
'''
import numpy as np

from rlcard.games.skat.utils import compare_cards, get_points

class SkatJudger:
    ''' Determine what cards a player can play and who won the game
    '''

    @staticmethod
    def playable_cards_from_hand(current_hand, suit=None, trump = 'D'): # TODO: Optimization: Zwischenspeichern der möglichen Karten?
        ''' Get playable cards from hand

        Returns:
            set: set of string of playable cards
        '''
        playable_cards = []
        if suit is not None:
            for c in current_hand:
                if c.suit == suit or (suit == trump and c.rank == 'J'):
                    playable_cards.append(str(c))

        if suit is None or not playable_cards:
            for c in current_hand:
                playable_cards.append(str(c))

        return playable_cards

    @staticmethod
    def judge_game(players):
        ''' Judge whether the game is over

        Args:
            players (list): list of SkatPlayer objects
            player_id (int): integer of player's id

        Returns:
            (bool): True if the game is over
        '''
        return not players[0].current_hand and not players[1].current_hand and not players[2].current_hand

    @staticmethod
    def judge_payoffs(soloplayer_id, solo_score): # TODO: Berechne "mit X Spiel Y", Trumpffarbe, Hand etc.
        payoffs = np.array([0, 0, 0])

        if solo_score >= 90:
            payoffs[soloplayer_id] = (4 * 10) + 50
        elif solo_score > 60:
            payoffs[soloplayer_id] = (3 * 10) + 50
        elif solo_score <= 30:
            payoffs[soloplayer_id] = (-8 * 10) - 50
            payoffs[(soloplayer_id + 1) % 3] = 40
            payoffs[(soloplayer_id + 2) % 3] = 40
        elif solo_score <= 60:
            payoffs[soloplayer_id] = (-6 * 10) - 50
            payoffs[(soloplayer_id + 1) % 3] = 40
            payoffs[(soloplayer_id + 2) % 3] = 40
        return payoffs

    @staticmethod
    def judge_trick(playround):
        if len(playround.current_trick) == 3:
            winner = playround.current_trick[0][0].player_id
            highest_card = None
            card1 = playround.current_trick[0][1]
            card2 = playround.current_trick[1][1]
            card3 = playround.current_trick[2][1]
            highest_card = card1
            if not compare_cards(card1, card2, playround.trump, playround.current_suit):
                highest_card = card2
                winner = playround.current_trick[1][0].player_id
            if not compare_cards(highest_card, card3, playround.trump, playround.current_suit):
                winner = playround.current_trick[2][0].player_id
            points = get_points(card1) + get_points(card2) + get_points(card3)
            if winner == playround.soloplayer_id:
                playround.solo_points += points
            else:
                playround.opponent_points += points
            playround.current_trick = []
            playround.current_suit = None
            # print("Trick: " + card1 + card2 + card3 + ". Won by player: " + str(winner)) # Only when not training
            return winner
        return -1
