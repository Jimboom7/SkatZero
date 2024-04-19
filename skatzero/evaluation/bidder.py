import copy
import itertools
import random

from skatzero.env.feature_transformations import extract_state
from skatzero.evaluation.utils import swap_colors, swap_bids
from skatzero.game.utils import get_points
from skatzero.test.utils import construct_state_from_history

class Bidder:

    def __init__(self, env, raw_state, pos = "0"):
        self.env = env
        self.raw_state = copy.deepcopy(raw_state)
        self.pos = pos
        self.raw_state['self'] = 0
        self.raw_state_cpy = self.raw_state
        self.estimates = {'C': [], 'S': [], 'H': [], 'D': []}
        self.skat_comb_inds = list(itertools.combinations(list(range(22)), 2))
        self.current_skat = 0
        random.shuffle(self.skat_comb_inds)
        self.drueck_comb_inds = list(itertools.combinations(list(range(12)), 2)) # Skat wird vor die Handkarten gesetzt.

    def get_hand_cards(self):
        return self.raw_state['current_hand']

    def prepare_state(self, game_mode, raw_state):
        raw_state['trump'] = 'D'
        self.env.game.round.trump = 'D'

        # Trumpf ist immer Karo, daher müssen die Farben getauscht werden
        raw_state['current_hand'] = swap_colors(raw_state['current_hand'], 'D', game_mode)
        raw_state['others_hand'] = swap_colors(raw_state['others_hand'], 'D', game_mode)
        raw_state['actions'] = swap_colors(raw_state['actions'], 'D', game_mode)
        # Skat ist normalerweise hier leer, daher muss der hier nicht getauscht werden

        raw_state['bids'][1] = swap_bids(raw_state['bids'][1], 'D', game_mode)
        raw_state['bids'][2] = swap_bids(raw_state['bids'][2], 'D', game_mode)

    def simulate_player_discards(self, raw_state):
        if self.pos == "0": # Forehand: No discards
            state = extract_state(raw_state, self.env.get_legal_actions(raw_state))
            _, vals_cards = self.env.agents[0].predict(state)
            return max(vals_cards)
        else:
            values = []
            original_actions = self.env.game.state['actions']
            for card in raw_state['others_hand']:
                current_raw_state = copy.deepcopy(raw_state)

                current_raw_state['trace'].append((2, card))
                played_cards, others_cards, trick, actions = construct_state_from_history(current_raw_state['current_hand'], current_raw_state['trace'], current_raw_state['skat'])

                current_raw_state['played_cards'] = played_cards
                current_raw_state['others_hand'] = others_cards
                current_raw_state['actions'] = actions
                self.env.game.state['actions'] = actions
                current_raw_state['trick'] = trick

                state = extract_state(current_raw_state, self.env.get_legal_actions(current_raw_state))

                _, vals_cards = self.env.agents[0].predict(state)
                values.append(max(vals_cards))
            self.env.game.state['actions'] = original_actions
            return min(values)
        # else: # self.pos == "2" -> Backhand. Returns the average of i card distributions, where the "worst" possible discards of both opponents is considered for each distribution
        # Problem: Resulting value is way too low. Real opponents don't know the "best" moves because they don't know the other cards.
        #     values = []
        #     original_actions = self.env.game.state['actions']
        #     for i in range(30):
        #         values.append(999)
        #         player1_cards =  random.sample(raw_state['others_hand'], 10)
        #         player2_cards = [x for x in raw_state['others_hand'] if x not in player1_cards]

        #         for card1 in player1_cards:
        #             available_actions = self.available_actions(player2_cards, card1[0], game_mode)
        #             for card2 in available_actions:
        #                 current_raw_state = copy.deepcopy(raw_state)
        #                 current_raw_state['trace'].append((1, card1))
        #                 current_raw_state['trace'].append((2, card2))
        #                 played_cards, others_cards, trick, actions = construct_state_from_history(current_raw_state['current_hand'], current_raw_state['trace'], current_raw_state['skat'])

        #                 current_raw_state['played_cards'] = played_cards
        #                 current_raw_state['others_hand'] = others_cards
        #                 current_raw_state['actions'] = actions
        #                 self.env.game.state['actions'] = actions
        #                 current_raw_state['trick'] = trick

        #                 state = extract_state(current_raw_state, self.env.get_legal_actions(current_raw_state))
        #                 _, vals_cards = self.env.agents[0].predict(state)
        #                 if max(vals_cards) < values[i]:
        #                     values[i] = max(vals_cards)
        #     self.env.game.state['actions'] = original_actions
        #     return sum(values) / len(values)

    def available_actions(self, hand, suit, trump):
        playable_cards = []
        for card in hand:
            if (card[0] == suit and card[1] != 'J') or (suit == trump and card[1] == 'J'):
                playable_cards.append(card)

        if not playable_cards:
            return hand

        return playable_cards

    def get_blind_hand_values(self):
        values = []
        for game_mode in ['C', 'S', 'H', 'D']:
            current_raw_state = copy.deepcopy(self.raw_state_cpy)
            self.prepare_state(game_mode, current_raw_state)

            vals_cards = self.simulate_player_discards(current_raw_state)

            values.append(vals_cards)
        return values

    def find_best_game_and_discard(self, raw_state_prep):
        best_discard = {'C': [], 'S': [], 'H': [], 'D': []}
        for game_mode in ['C', 'S', 'H', 'D']:
            raw_state_gamemode_prep = copy.deepcopy(raw_state_prep)
            self.prepare_state(game_mode, raw_state_gamemode_prep)

            # Performance hotfix -> TODO: Make better
            #if (len(self.estimates[game_mode]) > 5 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -30 or
            #    len(self.estimates[game_mode]) > 20 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -10):
            #    continue

            vals_drueckungen = []
            best_state = None
            for drueck_inds in self.drueck_comb_inds:
                current_raw_state = copy.deepcopy(raw_state_gamemode_prep)
                # drücken (Skat und Hand updaten)
                current_raw_state['skat'] = [current_raw_state['current_hand'][drueck_inds[0]], current_raw_state['current_hand'][drueck_inds[1]]]
                current_raw_state['current_hand'] = [i for j, i in enumerate(current_raw_state['current_hand']) if j not in drueck_inds]
                current_raw_state['actions'] = current_raw_state['current_hand']
                current_raw_state['points'] = [get_points(current_raw_state['skat'][0]) + get_points(current_raw_state['skat'][1]), 0]

                state = extract_state(current_raw_state, self.env.get_legal_actions(current_raw_state))
                _, vals_cards = self.env.agents[0].predict(state)
                if len(vals_drueckungen) == 0 or max(vals_cards) > max(vals_drueckungen):
                    best_discard[game_mode] = swap_colors(current_raw_state["skat"], game_mode, "D")
                    best_state = current_raw_state
                vals_drueckungen.append(max(vals_cards))
                #print(f'Gedrückt: {swap_colors(current_raw_state["skat"], game_mode, "D")}, Value: {max(vals_cards)}')

            #print(f'{game_mode}: {max(vals_drueckungen)}')
            vals_cards = self.simulate_player_discards(best_state)
            self.estimates[game_mode].append(vals_cards)
        return best_discard

    def update_value_estimates(self):
        # Rohzustand vorbereiten mit Skatkarten in eigener Hand (danach 12 Karten) und Abzug von Gegnerhand (danach 20 Karten)
        raw_state_prep = copy.deepcopy(self.raw_state_cpy)
        current_skat_inds = self.skat_comb_inds[self.current_skat]
        skat = [raw_state_prep['others_hand'][current_skat_inds[0]], raw_state_prep['others_hand'][current_skat_inds[1]]]
        #print(skat)
        raw_state_prep['current_hand'] = skat + raw_state_prep['current_hand']
        raw_state_prep['others_hand'] = [i for j, i in enumerate(raw_state_prep['others_hand']) if j not in current_skat_inds]
        raw_state_prep['blind_hand'] = False

        self.find_best_game_and_discard(raw_state_prep)

        self.current_skat += 1
        return self.estimates
