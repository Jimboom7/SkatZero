from skatzero.game.utils import calculate_bidding_value, can_play_null, init_32_deck, evaluate_hand_strength

class Dealer:
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_32_deck()
        self.soloplayer = None
        self.skat = None
        self.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
        self.bid_jacks = [0, 0, 0]

    def shuffle(self):
        self.np_random.shuffle(self.deck)

    def set_player_hands(self, players):
        hand_num = 10

        for index, player in enumerate(players):
            current_hand = self.deck[index*hand_num:(index+1)*hand_num]
            player.current_hand = current_hand

        if evaluate_hand_strength(players[1].current_hand, 'D')['D'] > evaluate_hand_strength(players[0].current_hand, 'D')['D']:
            tmp = players[0].current_hand
            players[0].current_hand = players[1].current_hand
            players[1].current_hand = tmp

        if evaluate_hand_strength(players[2].current_hand, 'D')['D'] > evaluate_hand_strength(players[0].current_hand, 'D')['D']:
            tmp = players[0].current_hand
            players[0].current_hand = players[2].current_hand
            players[2].current_hand = tmp
        self.skat = self.deck[-2:]

    def set_bids(self, players):
        for player in players:
            if player.player_id == 0:
                continue
            values = evaluate_hand_strength(player.current_hand)
            max_value = max(values, key=values.get)
            if values[max_value] > 8 and self.np_random.rand() > 0.45 + (values[max_value] / 20): # "18" just looking chance
                self.bids[player.player_id]['D'] = 1
                self.bid_jacks[player.player_id] = 1
            elif values[max_value] > 8.5:
                self.bids[player.player_id][max_value] = 1
                with_without = calculate_bidding_value(player.current_hand) - 1
                self.bid_jacks[player.player_id] = with_without if self.np_random.rand() < 0.45 + (values[max_value] / 20) else 1 # Sometimes only bids with 1
            elif can_play_null(player.current_hand):
                self.bids[player.player_id]['N'] = 1

    def deal_cards(self, players):
        self.shuffle()
        self.set_player_hands(players)
        self.set_bids(players)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id
