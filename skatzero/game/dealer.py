from skatzero.game.utils import init_32_deck, evaluate_hand_strength

class Dealer:
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_32_deck()
        self.soloplayer = None
        self.skat = None

    def shuffle(self):
        self.np_random.shuffle(self.deck)

    def set_player_hands(self, players):
        hand_num = 10

        for index, player in enumerate(players):
            current_hand = self.deck[index*hand_num:(index+1)*hand_num]
            player.current_hand = current_hand

        if evaluate_hand_strength(players[1].current_hand, 'D') > evaluate_hand_strength(players[0].current_hand, 'D'):
            tmp = players[0].current_hand
            players[0].current_hand = players[1].current_hand
            players[1].current_hand = tmp

        if evaluate_hand_strength(players[2].current_hand, 'D') > evaluate_hand_strength(players[0].current_hand, 'D'):
            tmp = players[0].current_hand
            players[0].current_hand = players[2].current_hand
            players[2].current_hand = tmp
        self.skat = self.deck[-2:]


    def deal_cards(self, players):
        self.shuffle()
        self.set_player_hands(players)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id
