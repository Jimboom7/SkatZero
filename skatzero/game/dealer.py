from skatzero.game.utils import calculate_bidding_value, can_play_null, init_32_deck, evaluate_hand_strength

class Dealer:
    def __init__(self, np_random, blind_hand, open_hand):
        self.np_random = np_random
        self.deck = init_32_deck()
        self.soloplayer = None
        self.skat = None
        self.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
        self.bid_jacks = [0, 0, 0]
        self.blind_hand = blind_hand
        self.open_hand = open_hand
        self.suit_values = [10, 11, 12]

    def reset_bids(self):
        self.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
        self.bid_jacks = [0, 0, 0]

    def shuffle(self):
        self.np_random.shuffle(self.deck)
        self.np_random.shuffle(self.suit_values)

    def set_player_hands(self, players, gametype):
        for index, player in enumerate(players):
            current_hand = self.deck[index*10:(index+1)*10]
            player.current_hand = current_hand

        self.skat = self.deck[-2:]

        return evaluate_hand_strength(players[0].current_hand, gametype, self.np_random)[gametype]

    def set_bids(self, players, starting_player, gametype):
        self.reset_bids()
        diamond = self.np_random.choice(['D', 'H', 'S', 'C'])
        for player in players:
            plays_hand = False
            if player.player_id == 0:
                continue
            values = evaluate_hand_strength(player.current_hand, np_random=self.np_random)
            values_sorted = sorted(values.items(),key=(lambda i: i[1]))
            max_value = values_sorted[-1][0]
            with_without = calculate_bidding_value(player.current_hand) - 1
            if with_without < 4 and self.np_random.rand() > 4.4 - (values[max_value] / 3): # Handgame: Starting at 10.5 value sometimes plays hand
                with_without += 1
                plays_hand = True
            if values[max_value] > 8 and self.np_random.rand() > 0.45 + (values[max_value] / 20): # "18" just looking chance
                self.bids[player.player_id][diamond] = 1
                self.bid_jacks[player.player_id] = 0
            elif values[max_value] > 8.5:
                suits = ['D', 'H', 'S', 'C']
                suits.remove(diamond)
                if values_sorted[0][1] > 9.5: # Grand
                    if gametype != 'G':
                        return False
                if (values_sorted[-2][1] > 8.5 and values_sorted[-2][0] != diamond and # Bid second strongest suit
                    (values_sorted[-1][0] == diamond or self.suit_values[suits.index(values_sorted[-2][0])] > self.suit_values[suits.index(values_sorted[-1][0])]) and
                    self.np_random.rand() < -1 + (values_sorted[-2][1] / 5) and (not plays_hand or self.np_random.rand() > 4.4 - (values_sorted[-2][1] / 3))):
                    self.bids[player.player_id][values_sorted[-2][0]] = 1
                    self.bid_jacks[player.player_id] = with_without
                    if with_without == 1 and diamond == values_sorted[-2][0]: # Diamond with 1 -> mark same as "just 18"
                        self.bid_jacks[player.player_id] = 0
                else:
                    self.bids[player.player_id][max_value] = 1
                    self.bid_jacks[player.player_id] = with_without if self.np_random.rand() < 0.45 + (values[max_value] / 20) else 1 # Sometimes only bids with 1
                    if with_without == 1 and diamond == max_value: # Diamond with 1 -> mark same as "just 18"
                        self.bid_jacks[player.player_id] = 0
            elif can_play_null(player.current_hand):
                self.bids[player.player_id]['N'] = 1

        if gametype == 'N':
            self.bids[0]['N'] = 1
        elif gametype == 'D':
            self.bids[0]['D'] = 1
            self.bid_jacks[0] = calculate_bidding_value(players[0].current_hand) - 1 + self.blind_hand
        else:
            self.bids[0]['D'] = 1
            self.bid_jacks[0] = 10

        max_bid = 0
        first_bid = -1
        player_is_max = False
        for p in [(1 + starting_player) % 3, (2 + starting_player) % 3, (0 + starting_player) % 3]: # Simulates 3 player bidding
            player = players[p]
            bid = self.get_bid_value(self.bids[player.player_id], self.bid_jacks[player.player_id], diamond, p == 0)
            if p == starting_player and bid <= first_bid: # no bid if first player already bid more
                for x in ['D', 'H', 'S', 'C', 'N']:
                    self.bids[player.player_id][x] = 0
                self.bid_jacks[player.player_id] = 0
            if p != starting_player and (bid < first_bid or first_bid <= 0):
                if first_bid == 0 and bid > 0:
                    first_bid = 18
                else:
                    first_bid = bid
            if bid > max_bid:
                max_bid = bid
                player_is_max = p == 0
        return player_is_max

    def get_bid_value(self, bid, bid_jack, diamond, own_player):
        if bid['D'] == 0 and bid['H'] == 0 and bid['S'] == 0 and bid['C'] == 0 and bid['N'] == 0:
            return 0
        if bid['N'] == 1:
            if not own_player:
                if self.np_random.rand() < 0.35:
                    return 35
                return 23
            if self.open_hand and self.blind_hand:
                return 59
            if self.open_hand:
                return 46
            if self.blind_hand:
                return 35
            return 23
        if bid[diamond] == 1:
            if bid_jack == 0:
                return 18
            return 9 * (bid_jack + 1)
        i = 0
        for suit in ['D', 'H', 'S', 'C']:
            if suit == diamond:
                continue
            if bid[suit] == 1:
                return self.suit_values[i] * (bid_jack + 1)
            i += 1
        return 0

    def deal_cards(self, players, gametype, starting_player):
        self.shuffle()
        best_deck = []
        best_value = -1000
        num_shuffles = 4
        if gametype == 'G':
            num_shuffles = 3
        if gametype == 'N':
            num_shuffles = 35
        for _ in range(num_shuffles):
            self.shuffle()
            value = self.set_player_hands(players, gametype)
            if value > best_value:
                best_value = value
                best_deck = self.deck.copy()
        self.deck = best_deck
        self.set_player_hands(players, gametype)
        if not self.set_bids(players, starting_player, gametype):
            self.deal_cards(players, gametype, starting_player)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id
