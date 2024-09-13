import numpy as np

from skatzero.game.utils import calculate_bidding_value, can_play_null, can_play_null_ouvert, can_play_null_ouvert_hand, evaluate_d_strength_for_druecken, evaluate_grand_strength_for_druecken, evaluate_null_strength, init_32_deck, evaluate_hand_strength
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
        self.starting_player = -1
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
        self.set_bids(players, gametype, starting_player)
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

        self.set_hand_and_open_flags(players, gametype, highest_bidder)

        if highest_bidder != 0:
            # print("Player did not win bid")
            return -1

        if gametype == 'D':
            suit = self.check_game_to_play_after_skat(players, highest_bidder, starting_player)
            if suit == 'G':
                return -1
            self.swap_suit_for_D_game(players, suit)

        if gametype == 'G':
            if not self.grand[highest_bidder]:
                suit = self.check_game_to_play_after_skat(players, highest_bidder, starting_player)
                if suit == 'G':
                    self.grand[highest_bidder] = True
                else:
                    return -1

        # For analyseOutcomes
        # self.is_hand[highest_bidder] = False
        # self.blind_hand = False

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

    def set_hand_and_open_flags(self, players, gametype, highest_bidder):
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


    def check_game_to_play_after_skat(self, players, highest_bidder, starting_player):
        try:
            suit = list(self.bids[0].keys())[list(self.bids[0].values()).index(1)]
        except ValueError:
            suit = ''
        if not self.is_hand[highest_bidder]: # Determine suit to play (can be different from the initial bid or even Grand, depending on the Skat)
            full_hand = players[0].current_hand + self.skat
            # print("Full Hand: " + str(full_hand))
            values = evaluate_hand_strength(full_hand, np_random=self.np_random)
            grand_value = evaluate_hand_strength(full_hand, gametype = 'G', is_FH = starting_player == 0, np_random=self.np_random)['G']
            if self.np_random.rand() < (grand_value / 2) - 3.8:
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

    def set_bids(self, players, gametype, starting_player):
        self.reset_bids()
        for player in players:
            values = evaluate_hand_strength(player.current_hand, np_random=self.np_random, more_random=player.player_id!=0)
            grand_value = evaluate_hand_strength(player.current_hand, gametype = 'G', is_FH = starting_player == player.player_id, np_random=self.np_random, more_random=player.player_id!=0)['G']
            values_sorted = sorted(values.items(),key=(lambda i: i[1]))
            max_value = values_sorted[-1][0]
            with_without = calculate_bidding_value(player.current_hand) - 1
            if with_without < 4 and self.np_random.rand() > 4.1 - (values[max_value] / 3): # Handgame: Good chance with strong hand
                # print("Stark: Handspiel")
                with_without += 1
                self.is_hand[player.player_id] = True
            if self.np_random.rand() < (grand_value / 2) - 3.3 or (player.player_id == 0 and self.np_random.rand() <= 0.03 and grand_value >= 3):
                # print("Sehr stark: Grand - " + str(grand_value))
                self.grand[player.player_id] = True
                self.bid_jacks[player.player_id] = with_without
                self.bids[player.player_id][max_value] = 1
                if self.np_random.rand() < (grand_value / 2) - 4.3:
                    # self.counter8 += 1
                    if not self.is_hand[player.player_id]:
                        self.is_hand[player.player_id] = True
                        with_without += 1
                else:
                    # self.counter7 += 1
                    if self.is_hand[player.player_id]:
                        self.is_hand[player.player_id] = False
                        with_without -= 1
            elif values[max_value] > 8.5 or (player.player_id == 0 and gametype=='D' and self.np_random.rand() <= 0.01):
                suits = ['D', 'H', 'S', 'C']
                if (values_sorted[-2][1] > 8.5  and # Bid second strongest suit
                    (self.suit_values[suits.index(values_sorted[-2][0])] > self.suit_values[suits.index(values_sorted[-1][0])]) and
                    self.np_random.rand() < -1 + (values_sorted[-2][1] / 5) and (not self.is_hand[player.player_id] or self.np_random.rand() > 4.1 - (values_sorted[-2][1] / 3))):
                    # print("Zweitstärkste Farbe bieten, weil mehr Reizung möglich")
                    self.bids[player.player_id][values_sorted[-2][0]] = 1
                    self.bid_jacks[player.player_id] = with_without if self.np_random.rand() < (values_sorted[-2][1] / 5) - 1 else 1
                    if with_without == 1 and 'D' == values_sorted[-2][0]: # Diamond with 1 -> mark same as "just 18"
                        self.bid_jacks[player.player_id] = 0
                else:
                    # print("Normale Reizung")
                    self.bids[player.player_id][max_value] = 1
                    self.bid_jacks[player.player_id] = with_without if self.np_random.rand() < (values[max_value] / 5) - 1.2 else 1 # Sometimes only bids with 1
                    if self.bid_jacks[player.player_id] == 1 and 'D' == max_value: # Diamond with 1 -> mark same as "just 18"
                        self.bid_jacks[player.player_id] = 0
            elif can_play_null(player.current_hand, gametype, self.np_random):
                self.bids[player.player_id]['N'] = 1
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
            elif values[max_value] > 7 and self.np_random.rand() < values[max_value] - 7: # "18" just looking chance between 7.5 and 8.5
                if self.np_random.rand() > values[max_value] - 7 or max_value == 'D':
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
        drueck = []

        best_drueck = -10000
        drueck = [players[0].current_hand[0], players[0].current_hand[11]]
        if self.np_random.rand() < 0.99:
            for c1 in players[0].current_hand:
                for c2 in players[0].current_hand:
                    if players[0].current_hand.index(c2) <= players[0].current_hand.index(c1):
                        continue
                    cards = [x for x in players[0].current_hand if x != c1 and x != c2]
                    if gametype == 'N':
                        value = evaluate_null_strength(cards, [c1, c2])
                    elif gametype == 'D':
                        value = evaluate_d_strength_for_druecken(cards, [c1, c2], self.np_random)
                    else:
                        value = evaluate_grand_strength_for_druecken(cards, [c1, c2], self.np_random)
                    if value > best_drueck and self.np_random.rand() < 0.60:
                        drueck = [c1, c2]
                        best_drueck = value

        #print(drueck)
        #print(" ")

        players[0].current_hand.remove(drueck[0])
        players[0].current_hand.remove(drueck[1])
        self.skat.append(drueck[0])
        self.skat.append(drueck[1])

    def deal_cards(self, players, gametype):
        initial_starting_player = self.np_random.randint(0, 3)
        while self.starting_player == -1:
            self.shuffle()
            self.set_player_hands(players)
            self.starting_player = self.determine_soloplayer(players, initial_starting_player, gametype)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id, self.starting_player, self.blind_hand, self.open_hand

# from skatzero.game.player import Player
# d = Dealer(np.random.RandomState())
# players = [{}]
# players[0] = Player(0)
# players[0].current_hand = ['CJ', 'SJ', 'S7', 'HT', 'S9', 'CT', 'CK', 'D7', 'D8', 'D9']
# d.skat = ['DK', 'DA']
# print(players[0].current_hand)
# miss = 0
# for i in range (0,1000):
#    d.druecken(players, 'D')
#    print(d.skat)
#    if 'HT' not in d.skat or 'S9' not in d.skat:
#        miss += 1
# print(miss)

# from skatzero.game.player import Player
# d = Dealer(np.random.RandomState())
# players = [{},{},{}]
# players[0] = Player(0)
# players[1] = Player(1)
# players[2] = Player(2)

# for i in range (0,1000):
#     d.starting_player = -1
#     d.deal_cards(players, 'D')
#     print(players[0].current_hand)
#     print(players[1].current_hand)
#     print(players[2].current_hand)
#     print(d.bids)
#     print(d.bid_jacks)
#     print("#######")
# print(d.counter1)
# print(d.counter2)
# print(d.counter3)
# print(d.counter4)
# print(d.counter5)
# print("Hand Farbspiel: " + str(d.counter5))
# print("Eingepasst: " + str(d.counter6))
# print("Grand: " + str(d.counter7))
# print("Grand Hand: " + str(d.counter8))