import numpy as np

from skatzero.game.utils import calculate_bidding_value, can_play_null, can_play_null_ouvert, can_play_null_ouvert_hand, evaluate_null_strength, evaluate_null_strength_for_druecken, init_32_deck, evaluate_hand_strength
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
        self.blind_hand = False
        self.open_hand = False
        self.suit_values = [9, 10, 11, 12]
        self.grand = [False, False, False]
        self.is_hand = [False, False, False]
        self.is_open = [False, False, False]
        # self.counter1 = 0
        # self.counter2 = 0
        # self.counter3 = 0
        # self.counter4 = 0
        # self.counter5 = 0
        # self.counter6 = 0
        # self.counter7 = 0
        # self.counter8 = 0

    def reset_bids(self):
        self.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
        self.bid_jacks = [0, 0, 0]
        self.grand = [False, False, False]
        self.is_hand = [False, False, False]
        self.is_open = [False, False, False]
        self.blind_hand = False
        self.open_hand = False

    def shuffle(self):
        self.np_random.shuffle(self.deck)

    def set_player_hands(self, players):
        for index, player in enumerate(players):
            current_hand = self.deck[index*10:(index+1)*10]
            player.current_hand = current_hand

        self.skat = self.deck[-2:]

    def get_bid_value(self, bid, bid_jack, player):
        if self.grand[player]:
            return (bid_jack + 1) * 24
        if bid['D'] == 0 and bid['H'] == 0 and bid['S'] == 0 and bid['C'] == 0 and bid['N'] == 0:
            return 0
        if bid['N'] == 1:
            if self.is_open[player] and self.is_hand[player]:
                return 59
            if self.is_open[player]:
                return 46
            if self.is_hand[player]:
                return 35
            return 23
        if bid['D'] == 1:
            if bid_jack == 0:
                return 18
            return 9 * (bid_jack + 1)
        i = 0
        for suit in ['D', 'H', 'S', 'C']:
            if bid[suit] == 1:
                return self.suit_values[i] * (bid_jack + 1)
            i += 1
        return 0

    def determine_soloplayer(self, players, starting_player, gametype):
        # print("############################")
        self.set_bids(players, gametype)
        # print(self.bids)
        # print(self.bid_jacks)

        if (self.get_bid_value(self.bids[0], self.bid_jacks[0], 0) == 0 and
            self.get_bid_value(self.bids[1], self.bid_jacks[1], 1) == 0 and
            self.get_bid_value(self.bids[2], self.bid_jacks[2], 2) == 0):
            return -1 # No Bids

        max_bid = 0
        first_bid = -1
        highest_bidder = -1
        for p in [(1 + starting_player) % 3, (2 + starting_player) % 3, (0 + starting_player) % 3]: # Simulates 3 player bidding
            player = players[p]
            bid = self.get_bid_value(self.bids[player.player_id], self.bid_jacks[player.player_id], p)
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
                highest_bidder = p
        
        # print(highest_bidder)
        # if self.bids[highest_bidder]['N'] == 1:
        #     self.counter5 += 1
        #     if not self.is_open[highest_bidder] and not self.is_hand[highest_bidder]:
        #         self.counter1 += 1
        #         print("closed")
        #     if not self.is_open[highest_bidder] and self.is_hand[highest_bidder]:
        #         self.counter2 += 1
        #         print("hand")
        #     if self.is_open[highest_bidder] and not self.is_hand[highest_bidder]:
        #         self.counter3 += 1
        #         print("open1")
        #     if self.is_open[highest_bidder] and self.is_hand[highest_bidder]:
        #         self.counter4 += 1
        #         print("ouverthand")

        # Get hand that the highest bidder plays
        if self.bids[highest_bidder]['N'] == 0 and gametype == 'N':
            # print("Wrong Gamemode!")
            return -1
        elif gametype == 'D':
            if ((self.bids[highest_bidder]['D'] == 0 and self.bids[highest_bidder]['H'] == 0 and
                self.bids[highest_bidder]['S'] == 0 and self.bids[highest_bidder]['C'] == 0) or
                self.grand[highest_bidder]):
                # if (self.bids[highest_bidder]['D'] == 0 and self.bids[highest_bidder]['H'] == 0 and
                # self.bids[highest_bidder]['S'] == 0 and self.bids[highest_bidder]['C'] == 0 and self.bids[highest_bidder]['N'] == 0):
                #     self.counter6 += 1
                # if self.grand[highest_bidder]:
                #     self.counter7 += 1
                # print("Wrong Gamemode!")
                return -1

        self.set_hand_and_open_flags(players, gametype, highest_bidder, p)

        starting_player = self.swap_hands_and_starting_player(players, highest_bidder, starting_player)

        if gametype == 'D':
            suit = self.check_game_to_play_after_skat(players, highest_bidder)
            if suit == 'G':
                return -1
            self.swap_suit_for_D_game(players, suit)

        if gametype == 'G':
            if not self.grand[highest_bidder]:
                suit = self.check_game_to_play_after_skat(players, highest_bidder)
                if suit == 'G':
                    self.grand[highest_bidder] = True
                else:
                    return -1

        if not self.is_hand[highest_bidder]:
            # print("Skat vorher: " + str(self.skat))
            self.druecken(players, gametype)
            # print("Hand 0: " + str(players[0].current_hand))
            # print("Skat: " + str(self.skat))

        if gametype == 'N': # Check if ouvert can be played, depending on the skat
            if not self.is_hand[highest_bidder] and not self.is_open[highest_bidder]:
                if can_play_null_ouvert_hand(players[0].current_hand, gametype, self.np_random):
                    self.is_open[highest_bidder] = True
                    self.open_hand = True
                    # self.counter1 -= 1
                    # self.counter3 += 1
                    # print("open2")

        # if self.is_hand[highest_bidder]:
        #     self.counter5 += 1

        return starting_player

    def set_hand_and_open_flags(self, players, gametype, highest_bidder, p):
        if self.is_hand[highest_bidder] and gametype == 'D':
            # print("Is Hand!")
            # If not necessary to play hand: Add a chance to still play it as a normal hand
            self.is_hand[highest_bidder] = False
            bid1 = self.get_bid_value(self.bids[highest_bidder], self.bid_jacks[highest_bidder] - 1, highest_bidder)
            bid2 = self.get_bid_value(self.bids[(highest_bidder + 1) % 3], self.bid_jacks[(highest_bidder + 1) % 3], highest_bidder)
            bid3 = self.get_bid_value(self.bids[(highest_bidder + 2) % 3], self.bid_jacks[(highest_bidder + 2) % 3], highest_bidder)
            values = evaluate_hand_strength(players[highest_bidder].current_hand, np_random=self.np_random)
            values_sorted = sorted(values.items(),key=(lambda i: i[1]))
            max_value = values_sorted[-1][0]
            if bid1 > bid2 and bid1 > bid3 and self.np_random.rand() > (values[max_value] / 2) - 4.5:
                self.is_hand[highest_bidder] = False
                self.blind_hand = False
                if gametype != 'N':
                    self.bid_jacks[highest_bidder] -= 1
                # print("No Hand!")
            else:
                self.is_hand[highest_bidder] = True
                self.blind_hand = True
                # print("Keep Hand!")

        if self.is_hand[highest_bidder] and gametype != 'D':
            self.blind_hand = True

        if self.is_open[highest_bidder] and gametype == 'N':
            # print("Is Open!")
            self.open_hand = True

    def swap_hands_and_starting_player(self, players, highest_bidder, starting_player):
        # print("Hand0: " + str(players[0].current_hand))
        # print("Hand1: " + str(players[1].current_hand))
        # print("Hand2: " + str(players[2].current_hand))
        tmp = [None, None, None]
        tmp[0] = players[0].current_hand
        tmp[1] = players[1].current_hand
        tmp[2] = players[2].current_hand
        players[0].current_hand = tmp[highest_bidder]
        players[1].current_hand = tmp[(highest_bidder + 1) % 3]
        players[2].current_hand = tmp[(highest_bidder + 2) % 3]
        tmp[0] = self.bids[0]
        tmp[1] = self.bids[1]
        tmp[2] = self.bids[2]
        self.bids[0] = tmp[highest_bidder]
        self.bids[1] = tmp[(highest_bidder + 1) % 3]
        self.bids[2] = tmp[(highest_bidder + 2) % 3]
        tmp[0] = self.bid_jacks[0]
        tmp[1] = self.bid_jacks[1]
        tmp[2] = self.bid_jacks[2]
        self.bid_jacks[0] = tmp[highest_bidder]
        self.bid_jacks[1] = tmp[(highest_bidder + 1) % 3]
        self.bid_jacks[2] = tmp[(highest_bidder + 2) % 3]
        # print("Hand 0: " + str(players[0].current_hand))
        # print("Hand 1: " + str(players[1].current_hand))
        # print("Hand 2: " + str(players[2].current_hand))
        # print("Bids 1: " + str(self.bids[1]))
        #print("Starting Player Alt: " + str(starting_player))
        starting_player = (3 + starting_player - highest_bidder) % 3
        #print("Starting Player Neu: " + str(starting_player))
        return starting_player

    def check_game_to_play_after_skat(self, players, highest_bidder):
        try:
            suit = list(self.bids[0].keys())[list(self.bids[0].values()).index(1)]
        except ValueError:
            suit = ''
        if not self.is_hand[highest_bidder]: # Determine suit to play (can be different from the initial bid or even Grand, depending on the Skat)
            full_hand = players[0].current_hand + self.skat
            # print("Full Hand: " + str(full_hand))
            values = evaluate_hand_strength(full_hand, np_random=self.np_random)
            grand_value = evaluate_hand_strength(full_hand, gametype = 'G', np_random=self.np_random)['G']
            if grand_value > self.np_random.rand() < (grand_value / 2) - 2.3:
                # print("Grand nach Skat!")
                # self.counter7 += 1
                return 'G'
            # print(values)

            if self.np_random.rand() > 0.9:
                return suit
            values_sorted = sorted(values.items(),key=(lambda i: i[1]))
            with_without = calculate_bidding_value(full_hand) - 1
            self.bid_jacks[0] = with_without

            bid_to_beat = max(self.get_bid_value(self.bids[1], self.bid_jacks[1], 1), self.get_bid_value(self.bids[2], self.bid_jacks[2], 2))
            for hand_val in reversed(values_sorted):
                self.bids[0] = {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}
                self.bids[0][hand_val[0]] = 1
                if self.get_bid_value(self.bids[0], self.bid_jacks[0], 0) >= bid_to_beat:
                    suit = hand_val[0]
                    break
            return suit
        return suit

    def swap_suit_for_D_game(self, players, suit):
        # print("Farbspiel: " + suit)
        players[0].current_hand = swap_colors(players[0].current_hand, 'D', suit)
        players[1].current_hand = swap_colors(players[1].current_hand, 'D', suit)
        players[2].current_hand = swap_colors(players[2].current_hand, 'D', suit)
        self.skat = swap_colors(self.skat, 'D', suit)
        self.bids[0] = swap_bids(self.bids[0], 'D', suit)
        self.bids[1] = swap_bids(self.bids[1], 'D', suit)
        self.bids[2] = swap_bids(self.bids[2], 'D', suit)
        # print("NeuD: " + str(players[0].current_hand))

    def set_bids(self, players, gametype):
        self.reset_bids()
        for player in players:
            values = evaluate_hand_strength(player.current_hand, np_random=self.np_random)
            grand_value = evaluate_hand_strength(player.current_hand, gametype = 'G', np_random=self.np_random)['G']
            values_sorted = sorted(values.items(),key=(lambda i: i[1]))
            max_value = values_sorted[-1][0]
            with_without = calculate_bidding_value(player.current_hand) - 1
            if with_without < 4 and self.np_random.rand() > 4.1 - (values[max_value] / 3): # Handgame: Good chance with strong hand
                # print("Stark: Handspiel")
                with_without += 1
                self.is_hand[player.player_id] = True
            if self.np_random.rand() < (grand_value / 2) - 2:
                # print("Sehr stark: Grand - " + str(grand_value))
                self.grand[player.player_id] = True
                self.bid_jacks[player.player_id] = with_without
                self.bids[player.player_id][max_value] = 1
                if self.np_random.rand() < (grand_value / 2) - 2.55:
                    # self.counter8 += 1
                    if not self.is_hand[player.player_id]:
                        self.is_hand[player.player_id] = True
                        with_without += 1
                else:
                    if self.is_hand[player.player_id]:
                        self.is_hand[player.player_id] = False
                        with_without -= 1
            elif values[max_value] > 8.5:
                suits = ['D', 'H', 'S', 'C']
                if (values_sorted[-2][1] > 8.5  and # Bid second strongest suit
                    (self.suit_values[suits.index(values_sorted[-2][0])] > self.suit_values[suits.index(values_sorted[-1][0])]) and
                    self.np_random.rand() < -1 + (values_sorted[-2][1] / 5) and (not self.is_hand[player.player_id] or self.np_random.rand() > 4.1 - (values_sorted[-2][1] / 3))):
                    # print("Zweitstärkste Farbe bieten, weil mehr Reizung möglich")
                    self.bids[player.player_id][values_sorted[-2][0]] = 1
                    self.bid_jacks[player.player_id] = with_without
                    if with_without == 1 and 'D' == values_sorted[-2][0]: # Diamond with 1 -> mark same as "just 18"
                        self.bid_jacks[player.player_id] = 0
                    if with_without > 1 and self.np_random.rand() > (values_sorted[-2][1] / 5) - 1: # Sometimes only bids with 1
                        self.bid_jacks[player.player_id] = 1
                        if 'D' == values_sorted[-2][0]:
                            self.bid_jacks[player.player_id] = 0
                else:
                    # print("Normale Reizung")
                    self.bids[player.player_id][max_value] = 1
                    self.bid_jacks[player.player_id] = with_without if self.np_random.rand() < 0.45 + (values[max_value] / 20) else 1 # Sometimes only bids with 1
                    if self.bid_jacks[player.player_id] == 1 and 'D' == max_value: # Diamond with 1 -> mark same as "just 18"
                        self.bid_jacks[player.player_id] = 0
                    if with_without > 1 and self.np_random.rand() > (values[max_value] / 5) - 1: # Sometimes only bids with 1
                        self.bid_jacks[player.player_id] = 1
                        if 'D' == values_sorted[-2][0]:
                            self.bid_jacks[player.player_id] = 0
            elif can_play_null(player.current_hand, gametype, self.np_random):
                self.bids[player.player_id]['N'] = 1
                # print(evaluate_null_strength(player.current_hand))
                if can_play_null_ouvert_hand(player.current_hand, gametype, self.np_random):
                    if gametype == 'N' and self.np_random.rand() < 0.6:
                        return -1
                    self.is_open[player.player_id] = True
                    self.is_hand[player.player_id] = True
                elif can_play_null_ouvert(player.current_hand, gametype, self.np_random):
                    if self.np_random.rand() < 0.15:
                        self.is_hand[player.player_id] = True
                    else:
                        self.is_open[player.player_id] = True
            elif values[max_value] > 7.5 and self.np_random.rand() < values[max_value] - 7.5: # "18" just looking chance between 7.5 and 8.5
                if self.np_random.rand() > values[max_value] - 7.5 or max_value == 'D':
                    # print("Schwach: 18 nur gucken")
                    self.bids[player.player_id]['D'] = 1
                    self.bid_jacks[player.player_id] = 0
                else:
                    # print("Schwach: Mit 1 nur gucken")
                    self.bids[player.player_id][max_value] = 1
                    self.bid_jacks[player.player_id] = 1

    def druecken(self, players, gametype):
        players[0].current_hand.append(self.skat[0])
        players[0].current_hand.append(self.skat[1])
        self.skat = []
        drueck_probs = [0,0,0,0,0,0,0,0,0,0,0,0]
        drueck = []

        if gametype == 'N':
            drueck = self.druecken_null(players)
        elif gametype == 'D':
            self.druecken_d(players, drueck_probs)
        else:
            self.druecken_grand(players, drueck_probs)

        if gametype == 'D' or gametype == 'G':
            drueck_probs = np.array(drueck_probs)
            drueck_probs /= drueck_probs.sum()
            if self.np_random.rand() < 0.1:
                drueck = self.np_random.choice(players[0].current_hand, 2, p=drueck_probs, replace=False)
                max2 = players[0].current_hand.index(drueck[1])
            else:
                max1 = drueck_probs.argsort()[-1]
                max2 = drueck_probs.argsort()[-2]
                drueck = [players[0].current_hand[max1], players[0].current_hand[max2]] # variant without randomness

            if (sum(drueck[0][0] in s and s[1] != 'J' and s[1] != 'A' for s in players[0].current_hand) == 2 and drueck[1][0] != drueck[0][0] and self.np_random.rand() < 0.9 and drueck[0][1] != 'T'):
                d = next(x for x in players[0].current_hand if x[0] == drueck[0][0] and x[1] != drueck[0][1] and x[1] != 'J' and x[1] != 'A') # If two from one suit: drueck both
                if drueck_probs[players[0].current_hand.index(d)] + 1 + self.np_random.rand() > drueck_probs[max2]:
                    drueck[1] = d

        #print(drueck)
        #print(" ")

        players[0].current_hand.remove(drueck[0])
        players[0].current_hand.remove(drueck[1])
        self.skat.append(drueck[0])
        self.skat.append(drueck[1])

    def druecken_grand(self, players, drueck_probs):
        i = -1
        for card in players[0].current_hand:
            i += 1
            drueck_probs[i] = 0.001
            num_trump = sum('J' in s for s in players[0].current_hand)
            trump_threshold = 2
            num_curr_suit = sum(card[0] in s and s[1] != 'J' for s in players[0].current_hand)
            if card[1] == 'J':
                continue
            if card[1] == 'A' and card[0] + 'T' in players[0].current_hand and num_trump < trump_threshold: # Ace: When low on trump and 10 in hand, and suit is long: higher chance to drueck
                if num_curr_suit >= 3:
                    drueck_probs[i] = num_curr_suit - 3 + (trump_threshold - num_trump)
            elif card[1] == 'T' and card[0] + 'A' not in players[0].current_hand: # 10 without ace: always high chance to drueck with less cards
                drueck_probs[i] = 3.5 - (num_curr_suit / 1)
                if card[0] + 'K' in players[0].current_hand and num_curr_suit == 2:
                    drueck_probs[i] = 0.5
            elif card[1] == 'T' and card[0] + 'A' in players[0].current_hand and num_trump < trump_threshold: # 10: When low on trump and Ace in hand, and suit is long: higher chance to drueck
                if num_curr_suit >= 3:
                    drueck_probs[i] = num_curr_suit - 3 + (trump_threshold - num_trump)
            elif card[1] == 'K': # king: small chance to drueck
                drueck_probs[i] = 0.2 - (num_curr_suit / 20)
                if card[0] + 'T' in players[0].current_hand and num_curr_suit == 2:
                    drueck_probs[i] = -0.7
            elif card[1] == 'Q': # queen: small chance to drueck
                drueck_probs[i] = 0.2 - (num_curr_suit / 20)
                if drueck_probs[i] < 0:
                    drueck_probs[i] = 0.004
                if card[0] + 'K' in players[0].current_hand:
                    drueck_probs[i] -= 0.01
            elif card[1] in ['7', '8', '9']: # 7, 8, 9: small chance to drueck
                drueck_probs[i] = 0.1 - (num_curr_suit / 20)
                if drueck_probs[i] < 0:
                    drueck_probs[i] = 0.003
            if num_curr_suit == 1 and card[1] != 'A': # single card (no ace) in suit: high chance to drueck
                drueck_probs[i] += 1.2
            if num_curr_suit == 2 and card[1] != 'A' and (card[1] != 'T' or card[0] + 'A' not in players[0].current_hand): # suit with 2 cards (no ace, or no ace + 10): medium chance to drueck
                drueck_probs[i] += 0.7
                if (sum('D' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1 or
                        sum('H' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1 or
                        sum('S' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1 or
                        sum('C' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1):
                    drueck_probs[i] += 0.5
            if num_curr_suit == 2 and card[1] != 'A' and (card[0] + 'A' in players[0].current_hand):
                drueck_probs[i] -= 0.5
            if drueck_probs[i] <= 0:
                drueck_probs[i] = 0.002
        #print(drueck_probs)

    def druecken_d(self, players, drueck_probs):
        i = -1
        for card in players[0].current_hand:
            i += 1
            drueck_probs[i] = 0.001
            num_trump = sum('J' in s for s in players[0].current_hand) + sum('D' in s and s[1] != 'J' for s in players[0].current_hand)
            trump_threshold = 4.5
            num_curr_suit = sum(card[0] in s and s[1] != 'J' for s in players[0].current_hand)
            if card[1] == 'J' or card[0] == 'D':
                continue
            if card[1] == 'A' and card[0] + 'T' in players[0].current_hand and num_trump < trump_threshold: # Ace: When low on trump and 10 in hand, and suit is long: higher chance to drueck
                if num_curr_suit >= 4:
                    drueck_probs[i] = num_curr_suit - 3 + (trump_threshold - num_trump)
            elif card[1] == 'T' and card[0] + 'A' not in players[0].current_hand: # 10 without ace: always high chance to drueck with less cards
                drueck_probs[i] = 3.5 - (num_curr_suit / 1)
                if card[0] + 'K' in players[0].current_hand and num_curr_suit == 2:
                    drueck_probs[i] = 0
            elif card[1] == 'T' and card[0] + 'A' in players[0].current_hand and num_trump < trump_threshold: # 10: When low on trump and Ace in hand, and suit is long: higher chance to drueck
                if num_curr_suit >= 4:
                    drueck_probs[i] = num_curr_suit - 3 + (trump_threshold - num_trump)
            elif card[1] == 'K': # king: small chance to drueck
                drueck_probs[i] = 0.2 - (num_curr_suit / 20)
                if card[0] + 'T' in players[0].current_hand and num_curr_suit == 2:
                    drueck_probs[i] = -0.7
            elif card[1] == 'Q': # queen: small chance to drueck
                drueck_probs[i] = 0.2 - (num_curr_suit / 20)
                if card[0] + 'K' in players[0].current_hand:
                    drueck_probs[i] -= 0.01
            elif card[1] in ['7', '8', '9']: # 7, 8, 9: small chance to drueck
                drueck_probs[i] = 0.1 - (num_curr_suit / 20)
                if drueck_probs[i] < 0:
                    drueck_probs[i] = 0.003
            if num_curr_suit == 1 and card[1] != 'A': # single card (no ace) in suit: high chance to drueck
                drueck_probs[i] += 1.2
            if num_curr_suit == 2 and card[1] != 'A' and (card[1] != 'T' or card[0] + 'A' not in players[0].current_hand): # suit with 2 cards (no ace, or no ace + 10): medium chance to drueck
                drueck_probs[i] += 0.7
                if (sum('H' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1 or
                        sum('S' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1 or
                        sum('C' in s and s[1] != 'J' and s[1] != 'T' and s[1] != 'A' for s in players[0].current_hand) == 1):
                    drueck_probs[i] += 0.4
            if num_curr_suit == 2 and card[1] != 'A' and (card[0] + 'A' in players[0].current_hand):
                drueck_probs[i] -= 0.5
            if drueck_probs[i] <= 0:
                drueck_probs[i] = 0.002

    def druecken_null(self, players):
        best_drueck = -10000
        drueck = [players[0].current_hand[0], players[0].current_hand[1]]
        for c1 in players[0].current_hand:
            for c2 in players[0].current_hand:
                if c1 == c2:
                    continue
                cards = [x for x in players[0].current_hand if x != c1 and x != c2]
                value = evaluate_null_strength_for_druecken(cards)
                if value > best_drueck and self.np_random.rand() < 0.95:
                    drueck = [c1, c2]
                    best_drueck = value
        return drueck

    def deal_cards(self, players, gametype, starting_player):
        new_starting_player = -1
        while new_starting_player == -1:
            self.shuffle()
            self.set_player_hands(players)
            new_starting_player = self.determine_soloplayer(players, starting_player, gametype)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id, new_starting_player, self.blind_hand, self.open_hand

# from skatzero.game.player import Player
# d = Dealer(np.random.RandomState())
# players = [{}]
# players[0] = Player(0)
# players[0].current_hand = ['S7', 'S9', 'SK', 'H7', 'HK', 'HQ', 'C8', 'D7', 'D8', 'D9']
# d.skat = ['DK', 'DA']
# print(players[0].current_hand)
# for i in range (0,10):
#    d.druecken(players, 'N')
#    print(d.skat)



# from skatzero.game.player import Player
# d = Dealer(np.random.RandomState())
# players = [{},{},{}]
# players[0] = Player(0)
# players[1] = Player(1)
# players[2] = Player(2)

# for i in range (0,1312):
#     d.deal_cards(players, 'N', 0)
# print(d.counter1)
# print(d.counter2)
# print(d.counter3)
# print(d.counter4)
# print(d.counter5)
# print("Hand Farbspiel: " + str(d.counter5))
# print("Eingepasst: " + str(d.counter6))
# print("Grand: " + str(d.counter7))
# print("Grand Hand: " + str(d.counter8))