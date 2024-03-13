from skatzero.game.dealer import Dealer
from skatzero.game.utils import get_points

class Round:
    def __init__(self, np_random):
        self.np_random = np_random
        self.played_cards = []
        self.trace = []

        self.current_player = None
        self.soloplayer_id = 0
        self.public = None
        self.current_suit = None
        self.current_trick = None
        self.solo_points = 0
        self.opponent_points = 0
        self.winners = []

        self.trump = None

        self.dealer = Dealer(self.np_random)

    def initiate(self, players):
        soloplayer_id = self.dealer.deal_cards(players)
        self.soloplayer_id = soloplayer_id
        self.current_player = soloplayer_id
        self.public = {'deck': self.dealer.deck, 'soloplayer': self.soloplayer_id,
                       'trace': self.trace, 'played_cards': ['' for _ in range(len(players))]}
        self.current_suit = None
        self.current_trick = []
        self.solo_points = get_points(self.dealer.skat[0]) + get_points(self.dealer.skat[1])
        self.opponent_points = 0
        self.winners = []
        self.trump = 'D'
        self.played_cards = [[], [], []]

    def update_public(self, action):
        self.trace.append((self.current_player, action))
        self.played_cards[self.current_player].append(action)
        self.public['played_cards'] = [self.played_cards[0], self.played_cards[1], self.played_cards[2]]

    def proceed_round(self, player, action):
        self.update_public(action)
        player.play(action)

        self.current_trick.append((player, action))

        if len(self.current_trick) == 1:
            self.current_suit = action[0]
            if action[1] == "J":
                self.current_suit = self.trump

    def find_last_played_card_in_trace(self, player_id):
        for i in range(len(self.trace) - 1, -1, -1):
            _id, action = self.trace[i]
            if _id == player_id:
                return action
        return None
