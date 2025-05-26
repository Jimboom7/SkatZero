from skatzero.game.utils import calculate_bidding_value, can_play_null, can_play_null_after_skat, can_play_null_ouvert, can_play_null_ouvert_after_skat, can_play_null_ouvert_hand, evaluate_null_strength, init_32_deck, evaluate_hand_strength
from skatzero.evaluation.utils import swap_colors, swap_bids

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
        self.max_bids = [0, 0, 0]
        self.blind_hand = False
        self.open_hand = False
        self.suits = ['D', 'H', 'S', 'C']
        self.suit_values = [9, 10, 11, 12]
        self.is_hand = [False, False, False]
        self.starting_player = -1

    def reset_bids(self):
        self.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
        self.bid_jacks = [0, 0, 0]
        self.max_bids = [0, 0, 0]
        self.is_hand = [False, False, False]
        self.blind_hand = False
        self.open_hand = False

    def shuffle(self):
        self.np_random.shuffle(self.deck)

    def set_player_hands(self, players):
        for index, player in enumerate(players):
            current_hand = self.deck[index*10:(index+1)*10]
            player.current_hand = current_hand

        self.skat = self.deck[-2:]

    def parse_and_set_bid(self, pos):
        d_bids = [18, 27, 45]
        h_bids = [20, 30, 40, 50]
        s_bids = [22, 33, 44, 55]
        c_bids = [24, 36, 48, 60]
        n_bids = [23, 35, 46, 59]

        if self.max_bids[pos] in d_bids:
            self.bids[pos]['D'] = 1
            if self.max_bids[pos] != 18:
                self.bid_jacks[pos] = int(self.max_bids[pos] / 9) - 1
        elif self.max_bids[pos] in h_bids:
            self.bids[pos]['H'] = 1
            self.bid_jacks[pos] = int(self.max_bids[pos] / 10) - 1
        elif self.max_bids[pos] in s_bids:
            self.bids[pos]['S'] = 1
            self.bid_jacks[pos] = int(self.max_bids[pos] / 11) - 1
        elif self.max_bids[pos] in c_bids:
            self.bids[pos]['C'] = 1
            self.bid_jacks[pos] = int(self.max_bids[pos] / 12) - 1
        elif self.max_bids[pos] in n_bids:
            self.bids[pos]['N'] = 1

    def simulate_bidding(self, players, gametype):
        self.set_bids(players)

        if sum(self.max_bids) == 0:
            return False # No Bids

        max_bid = 0
        first_bid = -1
        highest_bidder = -1
        for p in [(0 + self.starting_player) % 3, (1 + self.starting_player) % 3, (2 + self.starting_player) % 3]: # Simulates 3 player bidding
            player = players[p]
            bid = self.max_bids[player.player_id]
            if p == (2 + self.starting_player) % 3 and bid <= first_bid: # No bid if first player already bid more <- Falsch, da p == starting bedeutet, dass man hören ist. müsste geber sein (+2)
                self.max_bids[player.player_id] = 0
            if p != (2 + self.starting_player) % 3 and (bid < first_bid or first_bid <= 0):
                if first_bid == 0 and bid > 0:
                    first_bid = 18
                else:
                    first_bid = bid
            if bid > max_bid:
                max_bid = bid
                highest_bidder = p

        if highest_bidder != 0:
            return False

        self.parse_and_set_bid(0)
        self.parse_and_set_bid(1)
        self.parse_and_set_bid(2)

        suit = self.decide_skat_or_hand(players, gametype, highest_bidder)

        if self.blind_hand:
            if ((gametype == 'D' and suit not in ['D', 'H', 'S', 'C']) or
                (gametype == 'G' and suit != 'G') or
                (gametype == 'N' and suit != 'N')):
                return False
            else:
                if gametype in ['D', 'H', 'S', 'C']:
                    self.swap_suit_for_D_game(players, suit)
                return True

        self.pickup_skat(players)

        suit = self.check_game_to_play_after_skat(players, gametype)

        if ((gametype == 'D' and suit not in ['D', 'H', 'S', 'C']) or
            (gametype == 'G' and suit != 'G') or
            (gametype == 'N' and suit != 'N')):
            return False

        if gametype == 'D':
            self.swap_suit_for_D_game(players, suit)

        return True

    def decide_skat_or_hand(self, players, gametype, highest_bidder):
        values = evaluate_hand_strength(players[0].current_hand, np_random=self.np_random)
        grand_value = evaluate_hand_strength(players[0].current_hand, gametype = 'G', is_FH = self.starting_player == players[0].player_id, np_random=self.np_random)['G']
        values_sorted = sorted(values.items(), key=lambda i: i[1])
        best_suit = values_sorted[-1][0]
        factor = calculate_bidding_value(players[0].current_hand)

        if self.np_random.rand() < grand_value - 8.0 or (factor == 2 and (self.max_bids[1] > 48 or self.max_bids[2] > 48)):
            self.blind_hand = True
            return 'G'

        if self.max_bids[0] in [23, 35, 46, 59]:
            if (self.max_bids[1] > 46 or self.max_bids[2] > 46) or can_play_null_ouvert_hand(players[0].current_hand, self.np_random):
                self.blind_hand = True
                self.open_hand = True
                return 'N'
            if (self.max_bids[1] > 23 or self.max_bids[2] > 23) or can_play_null_ouvert(players[0].current_hand, self.np_random):
                if self.np_random.rand() < 0.15:
                    self.blind_hand = True
                    return 'N'

        values = evaluate_hand_strength(players[highest_bidder].current_hand, np_random=self.np_random)
        values_sorted = sorted(values.items(), key=lambda i: i[1])
        best_suit = values_sorted[-1][0]
        factor = calculate_bidding_value(players[0].current_hand)
        own_bid_without_hand = factor * self.suit_values[self.suits.index(best_suit)]
        own_bid_with_hand = (factor + 1) * self.suit_values[self.suits.index(best_suit)]
        bid_to_beat = max(self.max_bids[1], self.max_bids[2])
        if (own_bid_without_hand < bid_to_beat and own_bid_with_hand > bid_to_beat) and self.is_hand[highest_bidder]:
            self.blind_hand = True
        else:
            if self.is_hand[highest_bidder] and own_bid_without_hand >= bid_to_beat and self.np_random.rand() < (values[best_suit] / 2) - 5:
                self.blind_hand = True
            else:
                self.blind_hand = False

        return best_suit


    def check_game_to_play_after_skat(self, players, gametype):
        values = evaluate_hand_strength(players[0].current_hand, np_random=self.np_random)
        grand_value = evaluate_hand_strength(players[0].current_hand, gametype = 'G', is_FH = self.starting_player == 0, np_random=self.np_random)['G']
        bonus = 0.3 if gametype != 'G' else -0.2
        if self.np_random.rand() < grand_value - 6.3 - bonus:
            return 'G'

        bid_to_beat = max(self.max_bids[1], self.max_bids[2])

        null_cards = self.druecken_null(players)

        if bid_to_beat <= 46 and can_play_null_ouvert_after_skat(null_cards, self.np_random):
            self.open_hand = True
            return 'N'

        if bid_to_beat <= 23 and can_play_null_after_skat(null_cards, self.np_random):
            return 'N'

        values_sorted = sorted(values.items(), key=lambda i: i[1])
        factor = calculate_bidding_value(players[0].current_hand)

        for hand_val in reversed(values_sorted):
            if factor * self.suit_values[self.suits.index(hand_val[0])] >= bid_to_beat:
                if hand_val[1] > 5.5 or self.np_random.rand() < 0.01:
                    return hand_val[0]

        if grand_value > 5.5 or self.np_random.rand() < 0.01:
            return 'G'
        else:
            return ''

    def swap_suit_for_D_game(self, players, suit):
        players[0].current_hand = swap_colors(players[0].current_hand, 'D', suit)
        players[1].current_hand = swap_colors(players[1].current_hand, 'D', suit)
        players[2].current_hand = swap_colors(players[2].current_hand, 'D', suit)
        self.skat = swap_colors(self.skat, 'D', suit)
        self.bids[0] = swap_bids(self.bids[0], 'D', suit)
        self.bids[1] = swap_bids(self.bids[1], 'D', suit)
        self.bids[2] = swap_bids(self.bids[2], 'D', suit)

    def druecken_null(self, players):
        hand = []

        best_drueck = -10000
        hand = players[0].current_hand[0:10]
        for c1 in players[0].current_hand:
            for c2 in players[0].current_hand:
                if players[0].current_hand.index(c2) <= players[0].current_hand.index(c1):
                    continue
                cards = [x for x in players[0].current_hand if x != c1 and x != c2]
                value = evaluate_null_strength(cards, [c1, c2])
                if value > best_drueck:
                    hand = cards
                    best_drueck = value
        return hand

    def set_bids(self, players):
        self.reset_bids()
        for player in players:
            values = evaluate_hand_strength(player.current_hand, np_random=self.np_random, opponent=player.player_id!=0)
            grand_value = evaluate_hand_strength(player.current_hand, gametype = 'G', is_FH = self.starting_player == player.player_id, np_random=self.np_random, opponent=player.player_id!=0)['G']
            values_sorted = sorted(values.items(), key=lambda i: i[1])
            best_suit = values_sorted[-1][0]
            factor = calculate_bidding_value(player.current_hand)

            if self.np_random.rand() < grand_value - 6:
                if self.np_random.rand() < grand_value - 8:
                    self.is_hand[player.player_id] = True
                    self.max_bids[player.player_id] = (factor + 1) * 24
                else:
                    self.is_hand[player.player_id] = False
                    self.max_bids[player.player_id] = factor * 24
                continue

            if factor <= 4 and self.np_random.rand() > 4.0 - (values[best_suit] / 3): # Handgame: Good chance with strong hand
                factor += 1
                self.is_hand[player.player_id] = True

            if self.np_random.rand() < values[best_suit] - 8 or self.np_random.rand() < values_sorted[-2][1] - 7 or self.np_random.rand() < values_sorted[-3][1] - 6.5: # Bid Color Game
                if ((self.np_random.rand() < values_sorted[-2][1] - 8 and # Bid second strongest suit. Case 1: Is strong and can bid more
                    (self.suit_values[self.suits.index(values_sorted[-2][0])] > self.suit_values[self.suits.index(values_sorted[-1][0])]) and
                    self.np_random.rand() < -3.5 + (values_sorted[-2][1] / 2) and (not self.is_hand[player.player_id] or self.np_random.rand() > 4.1 - (values_sorted[-2][1] / 3))) or
                    (self.np_random.rand() > values[best_suit] - 7.5 and self.suit_values[self.suits.index(values_sorted[-2][0])] < self.suit_values[self.suits.index(values_sorted[-1][0])] and
                     self.np_random.rand() < values_sorted[-2][1] - 7)): # Case 2: First suit is weak and second suit is lower bid
                    self.max_bids[player.player_id] = factor * self.suit_values[self.suits.index(values_sorted[-2][0])] if self.np_random.rand() < (values_sorted[-2][1] / 2) - 3.5 else 2 * self.suit_values[self.suits.index(values_sorted[-2][0])]
                else:
                    self.max_bids[player.player_id] = factor * self.suit_values[self.suits.index(values_sorted[-1][0])] if self.np_random.rand() < (values[best_suit] / 5) - 1.2 else 2 * self.suit_values[self.suits.index(values_sorted[-1][0])] # Sometimes only bids with 1

            if can_play_null(player.current_hand, self.np_random, player.player_id!=0):
                self.max_bids[player.player_id] = max(23, self.max_bids[player.player_id])
                if can_play_null_ouvert_hand(player.current_hand, self.np_random):
                    self.max_bids[player.player_id] = max(59, self.max_bids[player.player_id])
                elif can_play_null_ouvert(player.current_hand, self.np_random, player.player_id!=0):
                    if self.np_random.rand() < 0.15:
                        self.max_bids[player.player_id] = max(35, self.max_bids[player.player_id])
                    else:
                        self.max_bids[player.player_id] = max(46, self.max_bids[player.player_id])

            if self.np_random.rand() < values[best_suit] - 7: # "18" just looking chance above 7
                if self.np_random.rand() > values[best_suit] - 7.25:
                    self.max_bids[player.player_id] = max(18, self.max_bids[player.player_id])
                else:
                    self.max_bids[player.player_id] = max(2 * self.suit_values[self.suits.index(best_suit)], self.max_bids[player.player_id])

    def pickup_skat(self, players):
        players[0].current_hand.append(self.skat[0])
        players[0].current_hand.append(self.skat[1])
        self.skat = []

    def deal_cards(self, players, gametype):
        self.starting_player = self.np_random.randint(0, 3)
        valid_game = False
        while not valid_game:
            self.shuffle()
            self.set_player_hands(players)
            valid_game = self.simulate_bidding(players, gametype)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id, self.starting_player, self.blind_hand, self.open_hand
