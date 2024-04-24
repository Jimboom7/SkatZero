import copy
import itertools
import random
import numpy as np

from skatzero.env.feature_transformations import extract_state
from skatzero.evaluation.utils import swap_colors, swap_bids
from skatzero.game.utils import get_points
from skatzero.test.utils import construct_state_from_history
from bidding.bidder_simulated_data import SimulatedDataBidder

class AdvancedBidder:

    def __init__(self, env, raw_state, pos = "0", gegenreizung_penalties = {'D': 25, 'G': 40, 'N': 25, 'NO': 25}):
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
        self.drueck_comb_inds = list(itertools.combinations(list(range(12)), 2)) # Skat wird vor die Handkarten gesetzt.

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
        if self.pos == 0: # Forehand: No discards
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
            return sum(values[:5]) / 5


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


    def find_best_game_and_discard(self, raw_state_prep):
        best_discard = {'C': [], 'S': [], 'H': [], 'D': [], 'G': [], 'N': [], 'NO': []}
        bid_value_table_skat = np.full((self.simulated_data_bidder.bids.size,), -1000)
        for game_mode in ['C', 'S', 'H', 'D', 'G', 'N', 'NO']:
            raw_state_gamemode_prep = copy.deepcopy(raw_state_prep)
            self.prepare_state(game_mode, raw_state_gamemode_prep)

            # Performance hotfix -> TODO: Make better
            if (len(self.estimates[game_mode]) > 5 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -60 or
                len(self.estimates[game_mode]) > 20 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -60):
                continue

            vals_drueckungen = []
            best_state = None
            original_state = copy.deepcopy(self.env.game.state)
            for drueck_inds in self.drueck_comb_inds:
                current_raw_state = copy.deepcopy(raw_state_gamemode_prep)
                # drücken (Skat und Hand updaten)
                current_raw_state['skat'] = [current_raw_state['current_hand'][drueck_inds[0]], current_raw_state['current_hand'][drueck_inds[1]]]
                current_raw_state['current_hand'] = [i for j, i in enumerate(current_raw_state['current_hand']) if j not in drueck_inds]
                current_raw_state['actions'] = current_raw_state['current_hand']
                current_raw_state['points'] = [get_points(current_raw_state['skat'][0]) + get_points(current_raw_state['skat'][1]), 0]

                self.env.game.state = copy.deepcopy(current_raw_state)
                state = extract_state(current_raw_state, self.env.get_legal_actions())
                agent_id = 0
                if current_raw_state['trump'] == 'J':
                    agent_id = 3
                elif current_raw_state['trump'] is None:
                    agent_id = 6
                _, vals_cards = self.env.agents[agent_id].predict(state, raw=True)
                if len(vals_drueckungen) == 0 or max(vals_cards) > max(vals_drueckungen):
                    if game_mode in ['C', 'S', 'H']:
                        best_discard[game_mode] = swap_colors(current_raw_state["skat"], game_mode, "D")
                    else:
                        best_discard[game_mode] = current_raw_state["skat"]
                    best_state = current_raw_state
                vals_drueckungen.append(max(vals_cards))
                #print(f'Gedrückt: {swap_colors(current_raw_state["skat"], game_mode, "D")}, Value: {max(vals_cards)}')

            #print(f'{game_mode}: {max(vals_drueckungen)}')
            self.env.game.state = original_state
            best_val = self.simulate_player_discards(best_state)

            bid_value_table_game = self.simulated_data_bidder.get_bid_value_table(raw_state_gamemode_prep, game_mode, best_val)
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

        best_discard, bid_value_table_skat = self.find_best_game_and_discard(raw_state_prep)
        if self.bid_table is None:
            self.bid_table = bid_value_table_skat
        else:
            # Implementierung hier als laufend aktualisierter Mittelwert
            factor_old = (self.current_skat) / (self.current_skat+1)
            factor_new = 1 - factor_old
            self.bid_table = factor_old * self.bid_table + factor_new * bid_value_table_skat

        self.current_skat += 1
        return self.estimates, dict(zip(self.simulated_data_bidder.bids, self.bid_table))
