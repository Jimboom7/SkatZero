import copy
import itertools
import random

from skatzero.evaluation.utils import swap_colors
from skatzero.game.utils import get_points

class Bidder:

    def __init__(
        self,
        env,
        raw_state,
    ):
        self.env = env
        self.raw_state = raw_state
        self.raw_state['self'] = 0
        self.raw_state_cpy = copy.deepcopy(self.raw_state)
        self.estimates = {'C': [], 'S': [], 'H': [], 'D': []}
        self.skat_comb_inds = list(itertools.combinations(list(range(22)), 2))
        self.current_skat = 0
        random.shuffle(self.skat_comb_inds)
        self.drueck_comb_inds = list(itertools.combinations(list(range(12)), 2)) # Skat wird vor die Handkarten gesetzt.

    def get_hand_cards(self):
        return self.raw_state['current_hand']

    def get_blind_hand_values(self):
        values = []
        for game_mode in ['C', 'S', 'H', 'D']:
            current_raw_state = copy.deepcopy(self.raw_state_cpy)
            current_raw_state['trump'] = 'D'
            self.env.game.round.trump = 'D'

            # Trumpf ist immer Karo, daher müssen die Farben getauscht werden
            current_raw_state['current_hand'] = swap_colors(current_raw_state['current_hand'], 'D', game_mode)
            current_raw_state['others_hand'] = swap_colors(current_raw_state['others_hand'], 'D', game_mode)
            current_raw_state['skat'] = swap_colors(current_raw_state['skat'], 'D', game_mode) # nicht zwingend nötig, da Hand

            tmp = current_raw_state['bids'][1]['D']
            current_raw_state['bids'][1]['D'] = current_raw_state['bids'][1][game_mode]
            current_raw_state['bids'][1][game_mode] = tmp
            tmp = current_raw_state['bids'][2]['D']
            current_raw_state['bids'][2]['D'] = current_raw_state['bids'][2][game_mode]
            current_raw_state['bids'][2][game_mode] = tmp

            state = self.env.extract_state(current_raw_state)

            _, vals_cards = self.env.agents[0].predict(state)
            values.append(max(vals_cards))
        return values

    def find_best_game_and_discard(self, raw_state_prep):
        best_discard = {'C': [], 'S': [], 'H': [], 'D': []}
        for game_mode in ['C', 'S', 'H', 'D']:
            raw_state_gamemode_prep = copy.deepcopy(raw_state_prep)
            raw_state_gamemode_prep['trump'] = 'D'
            self.env.game.round.trump = 'D'

            raw_state_gamemode_prep['current_hand'] = swap_colors(raw_state_gamemode_prep['current_hand'], 'D', game_mode)
            raw_state_gamemode_prep['others_hand'] = swap_colors(raw_state_gamemode_prep['others_hand'], 'D', game_mode)

            # Performance hotfix -> TODO: Make better
            if (len(self.estimates[game_mode]) > 5 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -30 or
                len(self.estimates[game_mode]) > 20 and (sum(self.estimates[game_mode]) / len(self.estimates[game_mode])) < -10):
                continue

            vals_drueckungen = []
            for drueck_inds in self.drueck_comb_inds:
                current_raw_state = copy.deepcopy(raw_state_gamemode_prep)
                # drücken (Skat und Hand updaten)
                current_raw_state['skat'] = [current_raw_state['current_hand'][drueck_inds[0]], current_raw_state['current_hand'][drueck_inds[1]]]
                current_raw_state['current_hand'] = [i for j, i in enumerate(current_raw_state['current_hand']) if j not in drueck_inds]
                current_raw_state['actions'] = current_raw_state['current_hand']
                current_raw_state['points'] = [get_points(current_raw_state['skat'][0]) + get_points(current_raw_state['skat'][1]), 0]

                state = self.env.extract_state(current_raw_state)
                _, vals_cards = self.env.agents[0].predict(state)
                if len(vals_drueckungen) == 0 or max(vals_cards) > max(vals_drueckungen):
                    best_discard[game_mode] = swap_colors(current_raw_state["skat"], game_mode, "D")
                vals_drueckungen.append(max(vals_cards))
                #print(f'Gedrückt: {swap_colors(current_raw_state["skat"], game_mode, "D")}, Value: {max(vals_cards)}')

            #print(f'{game_mode}: {max(vals_drueckungen)}')
            self.estimates[game_mode].append(max(vals_drueckungen))
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
