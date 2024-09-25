import copy
import itertools
import random
import numpy as np

from skatzero.env.feature_transformations import extract_state
from skatzero.evaluation.utils import swap_colors, swap_bids
from skatzero.game.utils import evaluate_null_strength, get_points
from skatzero.test.utils import available_actions, construct_state_from_history
from bidding.bidder_simulated_data import SimulatedDataBidder

class Bidder:

    def __init__(self, env, raw_state, pos = "0", gegenreizung_penalties = {'D': 0, 'G': 0, 'N': 0, 'NO': 0, 'DH': 0, 'GH': 0, 'NH': 0, 'NOH': 0}):
        self.simulated_data_bidder = SimulatedDataBidder(gegenreizung_penalties)
        self.env = env
        self.pos = int(pos)
        self.raw_state = copy.deepcopy(raw_state)
        self.raw_state['self'] = 0
        self.estimates = {'C': [], 'S': [], 'H': [], 'D': [], 'G': [], 'N': [], 'NO': []}
        self.bid_table = None
        self.skat_comb_inds = list(itertools.combinations(list(range(22)), 2))
        self.current_skat = 0
        random.shuffle(self.skat_comb_inds)
        self.bid_value_table_list = []

    def get_hand_cards(self):
        return self.raw_state['current_hand']

    def prepare_state(self, game_mode, raw_state):
        self.env.set_state_shape(game_mode)
        if game_mode == 'N' or game_mode == 'NO':
            self.env.game.gametype = 'N'
            self.env.game.round.gametype = 'N'
            raw_state['trump'] = None
            self.env.game.round.trump = None
            if game_mode == 'NO':
                self.env.game.open_hand = True
                raw_state['open_hand'] = True
            else:
                self.env.game.open_hand = False
                raw_state['open_hand'] = False
            return
        elif game_mode == 'G':
            self.env.game.gametype = 'G'
            self.env.game.round.gametype = 'G'
            raw_state['trump'] = 'J'
            self.env.game.round.trump = 'J'
            return
        self.env.game.gametype = 'D'
        self.env.game.round.gametype = 'D'
        raw_state['trump'] = 'D'
        self.env.game.round.trump = 'D'

        # Trumpf ist immer Karo, daher müssen die Farben getauscht werden
        raw_state['current_hand'] = swap_colors(raw_state['current_hand'], 'D', game_mode)
        raw_state['others_hand'] = swap_colors(raw_state['others_hand'], 'D', game_mode)
        raw_state['actions'] = swap_colors(raw_state['actions'], 'D', game_mode)
        # Das Tauschen des Skats wurde einmal entfernt und keiner weiß wieso. ggf. gefährlich.
        # raw_state['skat'] = swap_colors(raw_state['skat'], 'D', game_mode)

        raw_state['bids'][1] = swap_bids(raw_state['bids'][1], 'D', game_mode)
        raw_state['bids'][2] = swap_bids(raw_state['bids'][2], 'D', game_mode)

    def simulate_player_discards(self, raw_state):
        if self.pos == 0: # Forehand: No discards.
            original_state = copy.deepcopy(self.env.game.state)
            self.env.game.state = copy.deepcopy(raw_state)

            state = extract_state(raw_state, self.env.get_legal_actions())
            agent_id = 0
            self.env.game.state = original_state
            if raw_state['trump'] == 'J':
                agent_id = 3
            elif raw_state['trump'] is None:
                agent_id = 6
            _, vals_cards = self.env.agents[agent_id].predict(state, raw=True)
            return max(vals_cards)
        else:
            values = []
            original_state = copy.deepcopy(self.env.game.state)
            for card in raw_state['others_hand']:
                current_raw_state = copy.deepcopy(raw_state)

                current_raw_state['trace'].append((2, card))
                played_cards, others_cards, trick, actions = construct_state_from_history(current_raw_state['current_hand'], current_raw_state['trace'],
                                                                                          current_raw_state['skat'], trump = raw_state['trump'])

                current_raw_state['played_cards'] = played_cards
                current_raw_state['others_hand'] = others_cards
                current_raw_state['actions'] = actions
                current_raw_state['trick'] = trick

                self.env.game.state = copy.deepcopy(current_raw_state)
                state = extract_state(current_raw_state, self.env.get_legal_actions())

                agent_id = 0
                if current_raw_state['trump'] == 'J':
                    agent_id = 3
                elif current_raw_state['trump'] is None:
                    agent_id = 6
                _, vals_cards = self.env.agents[agent_id].predict(state, raw=True)
                values.append(max(vals_cards))
            self.env.game.state = original_state
            values.sort()
            if self.pos == 1: # Middlehand: Take average of 10 worst discards of opponent
                return sum(values[:5]) / 5
            else: # Backhand: Can't simulate 2 discards, so take an average that is usually close to that
                return sum(values[-10:]) / 10

    def get_blind_hand_values(self):
        values = []
        for game_mode in ['C', 'S', 'H', 'D', 'G', 'N', 'NO']:
            values.append(self.get_blind_hand_values_for_game(game_mode))
        return values

    def get_blind_hand_values_for_game(self, game_mode):
        current_raw_state = copy.deepcopy(self.raw_state)
        self.prepare_state(game_mode, current_raw_state)

        vals_cards = self.simulate_player_discards(current_raw_state)
        return vals_cards

    def get_blind_hand_bidding_table(self, blind_hand_values, return_only_max=True, penalty=False):
        game_modes = ['CH', 'SH', 'HH', 'DH', 'GH', 'NH', 'NOH']
        bid_tables_all_gamemodes = []

        for game_mode_ind, game_mode in enumerate(game_modes):
            bid_tables_gamemode_all_skats = []
            for current_skat_inds in self.skat_comb_inds:
                # Rohzustand vorbereiten mit Skatkarten in eigener Hand (danach 12 Karten) und Abzug von Gegnerhand (danach 20 Karten)
                raw_state_prep = copy.deepcopy(self.raw_state)
                skat = [raw_state_prep['others_hand'][current_skat_inds[0]], raw_state_prep['others_hand'][current_skat_inds[1]]]
                raw_state_prep['current_hand'] = skat + raw_state_prep['current_hand']
                # Achtung! Rest vom State wird nicht geändert, da derzeit ab hier nicht mehr als current_hand genutzt wird!
                bid_tables_gamemode_all_skats.append(self.simulated_data_bidder.get_bid_value_table(raw_state_prep, game_mode, blind_hand_values[game_mode_ind], penalty=penalty))
            bid_tables_gamemode_all_skats = np.stack(bid_tables_gamemode_all_skats)
            bid_tables_all_gamemodes.append(np.mean(bid_tables_gamemode_all_skats, axis=0))

        if return_only_max:
            bid_table = np.max(np.stack(bid_tables_all_gamemodes), axis=0)
            bid_table_dict = dict(zip(self.simulated_data_bidder.bids, bid_table))
            return bid_table_dict
        else:
            bid_table_dict_gamemodes = {}
            for game_mode_ind, game_mode in enumerate(game_modes):
                bid_table_dict_gamemodes[game_mode] = dict(zip(self.simulated_data_bidder.bids, bid_tables_all_gamemodes[game_mode_ind]))
            return bid_table_dict_gamemodes

    def find_best_game_and_discard(self, raw_state_prep):
        best_discard = {'C': [], 'S': [], 'H': [], 'D': [], 'G': [], 'N': [], 'NO': []}
        bid_value_table_skat = np.full((self.simulated_data_bidder.bids.size,), -170)
        for game_mode in ['C', 'S', 'H', 'D', 'G', 'N', 'NO']:
            raw_state_gamemode_prep = copy.deepcopy(raw_state_prep)
            self.prepare_state(game_mode, raw_state_gamemode_prep)

            # Performance hotfix -> TODO: Make better
            if (len(self.estimates[game_mode]) > 5 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -90 or
                len(self.estimates[game_mode]) > 20 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -60):
                if game_mode in ['C', 'S', 'H', 'D'] and raw_state_gamemode_prep['current_hand'][0][0] != 'D' and raw_state_gamemode_prep['current_hand'][1][0] != 'D':
                    continue
                if game_mode in ['N', 'NO'] and raw_state_gamemode_prep['current_hand'][0][1] not in ['7', '8', '9'] and raw_state_gamemode_prep['current_hand'][1][1] not in ['7', '8', '9']:
                    continue
                if game_mode == 'G' and raw_state_gamemode_prep['current_hand'][0][1] not in ['A', 'J'] and raw_state_gamemode_prep['current_hand'][1][1] not in ['A', 'J']:
                    continue

            raw_state_gamemode_prep["drueck"] = True
            raw_state_gamemode_prep["actions"] = available_actions(raw_state_gamemode_prep["current_hand"])
            original_state = copy.deepcopy(self.env.game.state)
            self.env.game.state = copy.deepcopy(raw_state_gamemode_prep)
            state = extract_state(raw_state_gamemode_prep, self.env.get_legal_actions())

            agent_id = 0
            if raw_state_gamemode_prep['trump'] == 'J':
                agent_id = 3
            if raw_state_gamemode_prep['trump'] is None:
                agent_id = 6
            _, vals_cards = self.env.agents[agent_id].predict(state, raw=True)

            best_val = max(vals_cards)

            if game_mode in ['C', 'S', 'H']:
                best_discard[game_mode] = swap_colors(raw_state_gamemode_prep["actions"][np.argmax(vals_cards)], game_mode, "D")
            else:
                best_discard[game_mode] = raw_state_gamemode_prep["actions"][np.argmax(vals_cards)]

            self.env.game.state = original_state

            bid_value_table_game = self.simulated_data_bidder.get_bid_value_table(raw_state_gamemode_prep, game_mode, best_val, penalty=True)
            bid_value_table_skat = np.maximum(bid_value_table_skat, bid_value_table_game)

            self.estimates[game_mode].append(best_val)

        return best_discard, bid_value_table_skat


    def update_value_estimates(self):
        # Rohzustand vorbereiten mit Skatkarten in eigener Hand (danach 12 Karten) und Abzug von Gegnerhand (danach 20 Karten)
        raw_state_prep = copy.deepcopy(self.raw_state)
        current_skat_inds = self.skat_comb_inds[self.current_skat]
        skat = [raw_state_prep['others_hand'][current_skat_inds[0]], raw_state_prep['others_hand'][current_skat_inds[1]]]
        #print(skat)
        raw_state_prep['current_hand'] = skat + raw_state_prep['current_hand']
        raw_state_prep['others_hand'] = [i for j, i in enumerate(raw_state_prep['others_hand']) if j not in current_skat_inds]
        raw_state_prep['blind_hand'] = False

        _, bid_value_table_skat = self.find_best_game_and_discard(raw_state_prep)
        self.bid_value_table_list.append(bid_value_table_skat)

        self.current_skat += 1

        self.bid_table = [float(sum(col))/len(col) for col in zip(*self.bid_value_table_list)]

        return self.estimates, dict(zip(self.simulated_data_bidder.bids, self.bid_table))
