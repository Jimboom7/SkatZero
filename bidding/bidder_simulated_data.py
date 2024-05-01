import os
import numpy as np
import copy

from skatzero.game.utils import calculate_max_bids
from skatzero.evaluation.utils import swap_colors

class SimulatedDataBidder:

    def __init__(self, gegenreizung_penalties):
        self.gegenreizung_penalties = gegenreizung_penalties
        self.rewards = {'D': [-170, -150, -130, 70, 80, 90],     # Eigenschwarz, ..., Schwarz
                        'DH': [-190, -170, -150, 80, 90, 100],
                        'G': [-282, -234, -186, 98, 122, 146],
                        'GH': [-330, -282, -234, 122, 146, 170]}
        self.values = {}
        self.dists = {}
        self.bids = self.get_bid_list()
        self.load_data()


    def get_bid_list(self):
        bids_game = [23, 35, 46, 59] # Null
        for base in range(9, 13):
            bids_game = np.concatenate((bids_game, base * np.arange(2, 13))) # Farbspiel bis Spiel 12
        bids_game = np.concatenate((bids_game, 24 * np.arange(2, 8))) # Grand bis Spiel 7
        return np.sort(np.unique(bids_game))


    def load_data(self):
        # data dimensions:
        # n: number of simulated values
        # m: number of simulated hands for a value
        # 6: Eigenschwarz, Eigenschneider, Verloren, Gewonnen, Schneider, Schwarz
        #
        # data content:
        # values: expected rewards
        # dists: probabilities [0, 1]

        for gametype in ['D', 'G', 'DH', 'GH']:
            basedir = os.path.dirname(os.path.realpath(__file__))
            values = np.load(f'{basedir}/data/values_{gametype}.npy')                # shape: (n,)
            dists = np.load(f'{basedir}/data/outcome_distributions_{gametype}.npy')  # shape: (n, m, 6)

            # reduce dists by hands dimension
            dists = np.mean(dists, axis = 1) # shape: (n, 6)

            # preprend and append extreme values (Eigenschwarz, Schwarz) to ensure interpolation will always work
            values = np.concatenate(([-1000, self.rewards[gametype][0]-2], values, [self.rewards[gametype][-1]+2, 1000])) #-2/+2 for smooth points
            dist_always_own_black = [[1, 0, 0, 0, 0, 0]]
            dist_always_black     = [[0, 0, 0, 0, 0, 1]]
            dists = np.concatenate((dist_always_own_black, dist_always_own_black, dists, dist_always_black, dist_always_black), axis=0)

            self.values[gametype] = values
            self.dists[gametype] = dists


    def get_bid_value_table_with_penalty(self, raw_state, game_mode, normal_value):
        game_mode, bid_values_gamemode = self.get_bid_value_table(raw_state, game_mode, normal_value)

        # Über 18, also bei Gegenreizung, wird eine durchschnittliche Penalty vom Value abgezogen
        bid_values_gamemode[self.bids > 18] -= self.gegenreizung_penalties[game_mode]
        
        return bid_values_gamemode

    def get_bid_value_table(self, raw_state, game_mode, normal_value):
        bid_values_gamemode = np.zeros((self.bids.size,))

        if game_mode[0] in ['C', 'S', 'H', 'D', 'G']:
            current_hand = raw_state['current_hand']
            if game_mode[0] != 'G':
                current_hand = swap_colors(current_hand, game_mode[0], 'D')
            max_bids = calculate_max_bids(current_hand, game_mode)
            if game_mode[0] != 'G':
                game_mode = 'D' + game_mode[1:] # später ist nur noch interessant, ob es ein Farbspiel ist

            normal_inds = self.bids <= max_bids['Normal']
            schneider_inds = np.logical_and(self.bids > max_bids['Normal'], self.bids <= max_bids['Schneider'])
            schwarz_inds = np.logical_and(self.bids > max_bids['Schneider'], self.bids <= max_bids['Schwarz'])
            lost_inds = self.bids > max_bids['Schwarz']

            bid_values_gamemode[normal_inds] = normal_value

            # Schneider: value ausrechnen
            rewards_schneider = copy.deepcopy(self.rewards[game_mode])
            rewards_schneider[3] = -130 # normaler Sieg reicht nicht: gilt als verloren!
            value = 0
            for outcome_ind in range(6):
                value += np.interp(normal_value, self.values[game_mode], self.dists[game_mode][:, outcome_ind]) * rewards_schneider[outcome_ind]
            bid_values_gamemode[schneider_inds] = value

            # Schwarz: value ausrechnen
            rewards_schwarz = copy.deepcopy(self.rewards[game_mode])
            rewards_schwarz[3] = -130 # normaler Sieg reicht nicht: gilt als verloren!
            rewards_schwarz[4] = -130 # Schneider reicht leider auch nicht: gilt als verloren!
            value = 0
            for outcome_ind in range(6):
                value += np.interp(normal_value, self.values[game_mode], self.dists[game_mode][:, outcome_ind]) * rewards_schwarz[outcome_ind]
            bid_values_gamemode[schwarz_inds] = value

            bid_values_gamemode[lost_inds] = self.rewards[game_mode][0]

        elif game_mode == 'N':
            bid_values_gamemode[self.bids <= 23] = normal_value
            bid_values_gamemode[self.bids > 23] = -136

        elif game_mode == 'NO':
            bid_values_gamemode[self.bids <= 46] = normal_value
            bid_values_gamemode[self.bids > 46] = -182

        elif game_mode == 'NH':
            bid_values_gamemode[self.bids <= 35] = normal_value
            bid_values_gamemode[self.bids > 35] = -160

        elif game_mode == 'NOH':
            bid_values_gamemode[self.bids <= 59] = normal_value
            bid_values_gamemode[self.bids > 59] = -208

        else:
            raise ValueError(f'game_mode ist {game_mode}, was scheinbar nicht unterstützt wird!')

        return game_mode, bid_values_gamemode