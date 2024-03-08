from copy import deepcopy
from skatzero.env.utils import compare_cards, get_points, evalute_hand_strength

class GameEnv():

    def __init__(self, players):

        self.card_play_action_seq = []

        self.winner = None
        self.game_over = False

        self.acting_player_position = None

        self.players = players

        self.last_move_dict = {'soloplayer': '',
                               'opponent_left': '',
                               'opponent_right': ''}

        self.played_cards = {'soloplayer': [],
                             'opponent_left': [],
                             'opponent_right': []}

        self.trick = []
        self.trump = None
        self.current_suit = None
        self.skat_cards = None
        self.solo_reward = 0  # "Reward" Points at end of game
        self.opponent_reward = 0
        self.score = {'soloplayer': 0, # Score in the current round, up to 120
                         'opponent': 0}

        self.num_wins = {'soloplayer': 0,
                         'opponent': 0}

        self.sum_rewards = {'soloplayer': 0,
                           'opponent': 0}

        self.info_sets = {'soloplayer': InfoSet('soloplayer'),
                         'opponent_left': InfoSet('opponent_left'),
                         'opponent_right': InfoSet('opponent_right')}

        self.game_infoset = {}


    def init_new_game(self, card_play_data):
        # TODO: Dynamisch das zu spielende Spiel ermitteln mit reizen etc. Momentan kriegt Spieler 1 die "beste" Hand
        strongest = 0
        s0 = evalute_hand_strength(card_play_data['0'])
        s1 = evalute_hand_strength(card_play_data['1'])
        s2 = evalute_hand_strength(card_play_data['2'])
        if s1 > s0 and s1 > s2:
            strongest = 1
        if s2 > s1 and s2 > s0:
            strongest = 2

        self.info_sets['soloplayer'].player_hand_cards = card_play_data[str(strongest)]
        self.info_sets['opponent_left'].player_hand_cards = card_play_data[str((strongest + 1) % 3)]
        self.info_sets['opponent_right'].player_hand_cards = card_play_data[str((strongest + 2) % 3)]

        self.skat_cards = card_play_data['skat_cards']
        self.score['soloplayer'] = get_points(self.skat_cards[0]) + get_points(self.skat_cards[1])
        self.trump = 'D'

        self.update_acting_player_position()
        self.game_infoset = self.update_infoset_for_current_player()
        return self.game_infoset

    def check_game_done(self):
        if len(self.info_sets['soloplayer'].player_hand_cards) == 0 and \
                len(self.info_sets['opponent_left'].player_hand_cards) == 0 and \
                len(self.info_sets['opponent_right'].player_hand_cards) == 0:
            self.compute_reward()
            self.update_num_wins_scores()

            self.game_over = True

    def compute_reward(self): # TODO: Add Mit X Spiel Y
        if self.score['soloplayer'] >= 90:
            self.solo_reward = 90
            self.opponent_reward = 0
        elif self.score['soloplayer'] > 60:
            self.solo_reward = 80
            self.opponent_reward = 0
        elif self.score['soloplayer'] <= 30:
            self.solo_reward = -130
            self.opponent_reward = 40
        elif self.score['soloplayer'] <= 60:
            self.solo_reward = -110
            self.opponent_reward = 40

    def update_num_wins_scores(self):
        if self.solo_reward > 0:
            self.num_wins['soloplayer'] += 1
            self.winner = 'soloplayer'
        else:
            self.num_wins['opponent'] += 1
            self.winner = 'opponent'
        self.sum_rewards['soloplayer'] += self.solo_reward
        self.sum_rewards['opponent'] += self.opponent_reward

    def get_winner(self):
        return self.winner

    def step(self):
        action = self.players[self.acting_player_position].act(self.game_infoset)
        assert action in self.game_infoset.legal_actions

        self.last_move_dict[self.acting_player_position] = action

        self.card_play_action_seq.append((self.acting_player_position, action))
        self.update_acting_player_hand_cards(action)

        self.played_cards[self.acting_player_position].append(action)

        self.trick.append((self.acting_player_position, action))

        if len(self.trick) == 1:
            self.current_suit = action[0]
            if action[1] == "J":
                self.current_suit = self.trump

        trick_winner = self.check_trick()

        self.check_game_done()
        if not self.game_over:
            self.update_acting_player_position(trick_winner)
            self.game_infoset = self.update_infoset_for_current_player()
        return self.game_infoset

    def check_trick(self):
        if len(self.trick) == 3:
            trick_winner = self.trick[0][0]
            highest_card = None
            card1 = self.trick[0][1]
            card2 = self.trick[1][1]
            card3 = self.trick[2][1]
            highest_card = card1
            if not compare_cards(card1, card2, self.trump, self.current_suit):
                highest_card = card2
                trick_winner = self.trick[1][0]
            if not compare_cards(highest_card, card3, self.trump, self.current_suit):
                trick_winner = self.trick[2][0]
            points = get_points(card1) + get_points(card2) + get_points(card3)
            if trick_winner == 'soloplayer':
                self.score['soloplayer'] += points
            else:
                self.score['opponent'] += points
            self.trick = []
            self.current_suit = None
            return trick_winner
        return None

    def update_acting_player_position(self, trick_winner=None):
        if trick_winner is not None:
            self.acting_player_position = trick_winner

        elif self.acting_player_position is None:
            self.acting_player_position = 'soloplayer'

        else:
            if self.acting_player_position == 'soloplayer':
                self.acting_player_position = 'opponent_right'

            elif self.acting_player_position == 'opponent_right':
                self.acting_player_position = 'opponent_left'

            else:
                self.acting_player_position = 'soloplayer'

        return self.acting_player_position

    def update_acting_player_hand_cards(self, action):
        if action != '':
            self.info_sets[self.acting_player_position].player_hand_cards.remove(action)

    def get_legal_card_play_actions(self):
        playable_cards = []
        if self.current_suit is not None:
            for c in self.info_sets[self.acting_player_position].player_hand_cards:
                if (c[0] == self.current_suit and c[1] != 'J') or (self.current_suit == self.trump and c[1] == 'J'):
                    playable_cards.append(str(c))

        if self.current_suit is None or not playable_cards:
            for c in self.info_sets[self.acting_player_position].player_hand_cards:
                playable_cards.append(str(c))

        return playable_cards

    def calculate_missing_cards(self, for_player):
        possible_cards = self.info_sets[self.acting_player_position].other_hand_cards.copy()
        trick_counter = 0
        for player, card in self.info_sets[self.acting_player_position].card_play_action_seq:
            trick_counter += 1
            if player == for_player:
                player_card = card
            if trick_counter % 3 == 1:
                base_card = card
            if trick_counter % 3 == 0:
                if (player_card[0] == base_card[0]
                    or ((player_card[1] == 'J' or player_card[0] == self.trump) and
                    (base_card[1] == 'J' or base_card[0] == self.trump))):
                    continue
                to_remove = []
                if base_card[1] == 'J' or base_card[0] == self.trump:
                    to_remove = [self.trump + i for i in ["7", "8", "9", "Q", "K", "T", "A"]]
                    to_remove.append(["DJ", "HJ", "SJ", "CJ"])
                else:
                    to_remove = [base_card[0] + i for i in ["7", "8", "9", "Q", "K", "T", "A"]]
                possible_cards = [i for i in possible_cards if i not in to_remove]
        return possible_cards


    def reset(self):
        self.card_play_action_seq = []

        self.game_over = False

        self.acting_player_position = None

        self.last_move_dict = {'soloplayer': '',
                               'opponent_left': '',
                               'opponent_right': ''}

        self.played_cards = {'soloplayer': [],
                             'opponent_left': [],
                             'opponent_right': []}

        self.info_sets = {'soloplayer': InfoSet('soloplayer'),
                         'opponent_left': InfoSet('opponent_left'),
                         'opponent_right': InfoSet('opponent_right')}

        self.trick = []
        self.trump = None
        self.current_suit = None
        self.skat_cards = None
        self.solo_reward = 0
        self.opponent_reward = 0
        self.score = {'soloplayer': 0,
                         'opponent': 0}


    def update_infoset_for_current_player(self):
        self.info_sets[self.acting_player_position].legal_actions = self.get_legal_card_play_actions()

        self.info_sets[self.acting_player_position].last_move_dict = self.last_move_dict

        self.info_sets[self.acting_player_position].other_hand_cards = []
        for pos in ['soloplayer', 'opponent_left', 'opponent_right']:
            if pos != self.acting_player_position:
                self.info_sets[self.acting_player_position].other_hand_cards += self.info_sets[pos].player_hand_cards
                self.info_sets[self.acting_player_position].other_hand_cards = self.calculate_missing_cards(pos)
        if self.acting_player_position != 'soloplayer':
            self.info_sets[self.acting_player_position].other_hand_cards += self.skat_cards

        self.info_sets[self.acting_player_position].played_cards = self.played_cards
        self.info_sets[self.acting_player_position].card_play_action_seq = self.card_play_action_seq

        self.info_sets[self.acting_player_position].trick = self.trick
        self.info_sets[self.acting_player_position].score = {'soloplayer': self.score['soloplayer'],
                        'opponent': self.score['opponent']}
        if self.acting_player_position != 'soloplayer':
            self.info_sets[self.acting_player_position].score['soloplayer'] -= (get_points(self.skat_cards[0]) + get_points(self.skat_cards[1]))

        self.info_sets[self.acting_player_position].skat_cards = self.skat_cards

        self.info_sets[self.acting_player_position].trump = self.trump

        return deepcopy(self.info_sets[self.acting_player_position])

class InfoSet(object):
    """
    The game state is described as infoset, which
    includes all the information in the current situation,
    such as the hand cards of the three players, the
    historical moves, etc.
    """
    def __init__(self, player_position):
        # The player position, i.e., soloplayer, opponent_right, or opponent_left
        self.player_position = player_position
        # The hand cands of the current player. A list.
        self.player_hand_cards = None
        # The two skat cards. A list.
        self.skat_cards = None
        # The historical moves. It is a list of list
        self.card_play_action_seq = []
        # The union of the hand cards of the other two players for the current player
        self.other_hand_cards = None
        # The legal actions for the current move. It is a list of list
        self.legal_actions = None
        # The last moves for all the postions
        self.last_move_dict = None
        # The played cards so far. It is a list.
        self.played_cards = None
        # Current cards in the trick. A list with 0-2 entries.
        self.trick = []
        # The score of the players so far, opponents don't know soloplayer skat score
        self.score = {'soloplayer': 0,
                        'opponent': 0}
        # Only used for calculating missing cards of a player
        self.trump = None
