from skatzero.game.dealer import Dealer
from skatzero.game.utils import get_points

class Round:
    def __init__(self, np_random, gametype):
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
        self.blind_hand = False
        self.open_hand = False

        self.trump = None
        self.gametype=gametype

        self.dealer = Dealer(self.np_random)

    def initiate(self, players, starting_player=None):
        if starting_player is None:
            starting_player = self.np_random.randint(0, 3)
        soloplayer_id, self.current_player, self.blind_hand, self.open_hand = self.dealer.deal_cards(players, self.gametype, starting_player)
        self.soloplayer_id = soloplayer_id
        self.public = {'deck': self.dealer.deck, 'soloplayer': self.soloplayer_id,
                       'trace': self.trace, 'played_cards': ['' for _ in range(len(players))],
                       'soloplayer_open_cards': players[0].current_hand}
        self.current_suit = None
        self.current_trick = []
        self.solo_points = get_points(self.dealer.skat[0]) + get_points(self.dealer.skat[1])
        self.opponent_points = 0
        self.winners = []
        self.trump = 'D'
        if self.gametype == 'G':
            self.trump = 'J'
        elif self.gametype == 'N':
            self.trump = None
        self.played_cards = [[], [], []]

    def update_public(self, player, action):
        self.trace.append((self.current_player, action))
        self.played_cards[self.current_player].append(action)
        if self.current_player == 0:
            self.public['soloplayer_open_cards'] = player.current_hand
        self.public['played_cards'] = [self.played_cards[0], self.played_cards[1], self.played_cards[2]]

    def proceed_round(self, player, action):
        player.play(action)
        self.update_public(player, action)

        self.current_trick.append((player, action))

        if len(self.current_trick) == 1:
            self.current_suit = action[0]
            if action[1] == "J" and self.trump is not None:
                self.current_suit = self.trump

    def find_last_played_card_in_trace(self, player_id):
        for i in range(len(self.trace) - 1, -1, -1):
            _id, action = self.trace[i]
            if _id == player_id:
                return action
        return None
