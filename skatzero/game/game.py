import numpy as np

from skatzero.game.utils import get_points
from skatzero.game.player import Player
from skatzero.game.round import Round
from skatzero.game.utils import compare_cards


class Game:
    def __init__(self):
        self.np_random = np.random.RandomState()  # pylint: disable=no-member
        self.num_players = 3
        self.done = False
        self.history = []
        self.players = []
        self.round = None
        self.state = None
        self.blind_hand = False

    def init_game(self, blind_hand=False):
        self.done = False
        self.history = []
        self.blind_hand = blind_hand

        self.players = [Player(num) for num in range(self.num_players)]

        self.round = Round(self.np_random)
        self.round.initiate(self.players)

        player_id = self.round.current_player
        self.state = self.get_state(player_id)

        return self.state, player_id

    def step(self, action):

        player = self.players[self.round.current_player]

        self.round.proceed_round(player, action)

        next_id = self.check_trick()

        if not self.players[0].current_hand and not self.players[1].current_hand and not self.players[2].current_hand:
            self.done = True
        if next_id == -1:
            next_id = (player.player_id + 1) % self.num_players
        self.round.current_player = next_id

        state = self.get_state(next_id)
        self.state = state

        return state, next_id

    def get_state(self, player_id):
        player = self.players[player_id]
        others_hands = self.get_others_current_hand(player)
        solo_points = self.round.solo_points
        if player_id != self.round.soloplayer_id or self.blind_hand:
            solo_points -= (get_points(self.round.dealer.skat[0]) + get_points(self.round.dealer.skat[1]))
        points = [solo_points, self.round.opponent_points]
        if self.is_over():
            actions = []
        else:
            actions = list(player.available_actions(self.round.current_suit, self.round.trump))
        state = player.get_state(self.round.public, others_hands, points, actions, self.round.current_trick, self.blind_hand)

        return state

    def compute_rewards(self):
        soloplayer_id = self.round.soloplayer_id
        payoffs = np.array([0, 0, 0])

        if self.round.solo_points >= 90:
            payoffs[soloplayer_id] = (4 * 10) + 50
        elif self.round.solo_points > 60:
            payoffs[soloplayer_id] = (3 * 10) + 50
        elif self.round.solo_points <= 30:
            payoffs[soloplayer_id] = (-8 * 10) - 50
            payoffs[(soloplayer_id + 1) % 3] = 40
            payoffs[(soloplayer_id + 2) % 3] = 40
        elif self.round.solo_points <= 60:
            payoffs[soloplayer_id] = (-6 * 10) - 50
            payoffs[(soloplayer_id + 1) % 3] = 40
            payoffs[(soloplayer_id + 2) % 3] = 40
        return payoffs

    def check_trick(self):
        if len(self.round.current_trick) == 3:
            winner = self.round.current_trick[0][0].player_id
            highest_card = None
            card1 = self.round.current_trick[0][1]
            card2 = self.round.current_trick[1][1]
            card3 = self.round.current_trick[2][1]
            highest_card = card1
            if not compare_cards(card1, card2, self.round.trump, self.round.current_suit):
                highest_card = card2
                winner = self.round.current_trick[1][0].player_id
            if not compare_cards(highest_card, card3, self.round.trump, self.round.current_suit):
                winner = self.round.current_trick[2][0].player_id
            points = get_points(card1) + get_points(card2) + get_points(card3)
            if winner == self.round.soloplayer_id:
                self.round.solo_points += points
            else:
                self.round.opponent_points += points
            self.round.current_trick = []
            self.round.current_suit = None
            self.round.winners.append(winner)
            return winner
        return -1

    @staticmethod
    def get_num_actions():
        return 32

    def get_player_id(self):
        return self.round.current_player

    def get_num_players(self):
        return self.num_players

    def is_over(self):
        return self.done

    def get_others_current_hand(self, player):
        player_right = self.players[(player.player_id+1) % self.num_players]
        player_left = self.players[(player.player_id-1) % self.num_players]
        others_hand = player_right.current_hand + player_left.current_hand
        if player.player_id != self.round.soloplayer_id or self.blind_hand:
            others_hand = others_hand + self.round.dealer.skat
        return others_hand.copy()
