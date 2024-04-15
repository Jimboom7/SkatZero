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

    def set_player_hands(self, players, gametype):
        for index, player in enumerate(players):
            current_hand = self.deck[index*10:(index+1)*10]
            player.current_hand = current_hand

        best_hand_value = 0
        if evaluate_hand_strength(players[1].current_hand, gametype, self.np_random)[gametype] > evaluate_hand_strength(players[0].current_hand, gametype, self.np_random)[gametype]:
            tmp = players[0].current_hand
            players[0].current_hand = players[1].current_hand
            players[1].current_hand = tmp

        value2 = evaluate_hand_strength(players[2].current_hand, gametype, self.np_random)[gametype]
        value1 = evaluate_hand_strength(players[0].current_hand, gametype, self.np_random)[gametype]
        best_hand_value = value1
        if value2 > value1:
            tmp = players[0].current_hand
            players[0].current_hand = players[2].current_hand
            players[2].current_hand = tmp
            best_hand_value = value2
        self.skat = self.deck[-2:]

        return best_hand_value

    def set_bids(self, players):
        diamond = self.np_random.choice(['D', 'H', 'S', 'C'])
        first_bidder = self.np_random.choice([1, 2])
        for player in players:
            if player.player_id == 0:
                continue
            values = evaluate_hand_strength(player.current_hand, np_random=self.np_random)
            max_value = max(values, key=values.get)
            with_without = calculate_bidding_value(player.current_hand) - 1
            if with_without < 4 and self.np_random.rand() > 4.4 - (values[max_value] / 3): # Handgame: Starting at 10.5 value sometimes plays hand
                with_without += 1
            if values[max_value] > 8 and self.np_random.rand() > 0.45 + (values[max_value] / 20): # "18" just looking chance
                self.bids[player.player_id][diamond] = 1
                self.bid_jacks[player.player_id] = 0
            elif values[max_value] > 8.5:
                self.bids[player.player_id][max_value] = 1
                self.bid_jacks[player.player_id] = with_without if self.np_random.rand() < 0.45 + (values[max_value] / 20) else 1 # Sometimes only bids with 1
                if with_without == 1 and diamond == max_value: # Diamond with 1 -> mark same as "just 18"
                    self.bid_jacks[player.player_id] = 0
            elif can_play_null(player.current_hand):
                self.bids[player.player_id]['N'] = 1
        for player in players:
            if player.player_id == 0:
                continue
            if player.player_id != first_bidder and self.np_random.rand() < 0.66: # no bid if not first and other already bid more
                bid1 = self.bid_jacks[player.player_id] + (self.bids[player.player_id]['N'] * 1.25)
                bid2 = self.bid_jacks[first_bidder] + (self.bids[first_bidder]['N'] * 1.25)
                if bid1 < bid2 or bid1 + 0.5 - self.np_random.rand() < bid2:
                    for x in ['D', 'H', 'S', 'C', 'N']:
                        self.bids[player.player_id][x] = 0
                    self.bid_jacks[player.player_id] = 0


    def deal_cards(self, players, gametype):
        self.shuffle()
        if gametype == 'N': # Good Null Games are rare: Shuffle a few more times and pick a decent hand
            best_deck = []
            best_value = -1000
            for _ in range(15):
                self.shuffle()
                value = self.set_player_hands(players, gametype)
                if value > best_value:
                    best_value = value
                    best_deck = self.deck.copy()
            self.deck = best_deck
            self.set_player_hands(players, gametype)
        else:
            self.set_player_hands(players, gametype)
        self.set_bids(players)
        players[0].role = 'soloplayer'
        players[1].role = 'opponent'
        players[2].role = 'opponent'
        self.soloplayer = players[0]

        return self.soloplayer.player_id
