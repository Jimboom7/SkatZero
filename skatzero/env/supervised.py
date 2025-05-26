"""
Untested class for supervised learning via a iss log file.
"""
import os
from iss.SkatMatch import SkatMatch
from skatzero.env.feature_transformations import cards2array, extract_state, card2array, get_card_encoding, convert_action_id_to_card, convert_card_to_action_id
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import set_dealer_data
from skatzero.evaluation.utils import print_turn
from skatzero.evaluation.seeding import np_random


class SupervisedEnv(SkatEnv):
    def __init__(self, seed=None, gametype='D'):
        super().__init__(seed, gametype)
        self.matches = []
        self.current_match = 0
        print("Reading File...")
        i = 0
        with open(os.path.join(os.getenv('SKAT_PATH'), 'skatgame-games-07-2024/skatgame-games-07-2024.sgf'), encoding='utf-8') as fRaw: # TODO: Change to other file
            line = fRaw.readline()
            while line:
                try:
                    match = SkatMatch(line)
                    if not match.overbid and match.gameType == self.game.gametype and len(match.history) > 2 and match.history[1] not in ['RE', 'SC', 'TI.0', 'TI.1', 'TI.2']:
                        self.matches.append(match)
                except:
                    pass
                line = fRaw.readline()
                i+=1
                if i > 100000:
                    break

    def reset(self):
        state, player_id = self.game.init_game()

        dealer = set_dealer_data(self.matches[self.current_match], self.game.gametype) # TODO: Farbspiele != D -> cardHistory muss auch geswitched werden

        self.game.round.initiate(self.game.players, dealer = dealer)
        self.game.players[0].current_hand += self.game.round.dealer.skat
        self.game.round.dealer.skat = []

        player_id = self.game.round.current_player
        state = self.game.get_state(player_id)
        self.game.state = state

        return self.extract_state(state), player_id

    def step(self, action):
        action = self.decode_action(action)
        self.timestep += 1
        next_state, player_id = self.game.step(action)

        return self.extract_state(next_state), player_id

    def set_agents(self, agents):
        self.agents = agents

    def run(self, is_training=False, verbose=0, state=None, player_id=None):
        trajectories = [[] for _ in range(self.num_players)]

        if state is None or player_id is None:
            state, player_id = self.reset()
        else:
            state = self.extract_state(state)

        if not self.game.round.blind_hand:
            state = self.game.get_state(0)
            self.game.state = state
            state = self.extract_state(state)

            card_encoding = get_card_encoding(self.game.state)
            action = convert_card_to_action_id(self.matches[self.current_match].gedrueckt_cards, card_encoding)

            trajectories[0].append(state)
            trajectories[0].append(action)

            action = self.decode_action(action)
            state = self.game.druecken(action)

            state = self.extract_state(state)

        trajectories[player_id].append(state)
        current_step = 1
        while not self.is_over():
            card_encoding = get_card_encoding(self.game.state)
            action = convert_card_to_action_id(self.matches[self.current_match].history[current_step], card_encoding)
            current_step += 2
            if len(self.matches[self.current_match].history) <= current_step or self.matches[self.current_match].history[current_step] in ['RE', 'SC', 'TI.0', 'TI.1', 'TI.2']:
                self.game.done = True
            if not is_training:
                print_turn(state['raw_obs']['current_hand'], self.decode_action(action),
                        state['raw_obs']['self'], state['raw_obs']['trick'], state['raw_obs']['trump'], verbose)

            next_state, next_player_id = self.step(action)

            trajectories[player_id].append(action)

            state = next_state
            player_id = next_player_id

            if not self.game.is_over():
                trajectories[player_id].append(state)

        for player_id in range(self.num_players):
            try:
                state = self.get_state(player_id)
            except:
                pass
            trajectories[player_id].append(state)

        rewards = self.get_rewards(is_training)
        self.current_match += 1

        return trajectories, rewards

    def is_over(self):
        return self.game.is_over()

    def get_player_id(self):
        return self.game.get_player_id()

    def get_state(self, player_id):
        return self.extract_state(self.game.get_state(player_id))

    def seed(self, seed=None):
        self.np_random, seed = np_random(seed)
        self.game.np_random = self.np_random
        return seed

    def extract_state(self, state):
        extracted_state = extract_state(state, self.get_legal_actions())
        return extracted_state

    def get_rewards(self, is_training):
        self.game.round.solo_points = self.matches[self.current_match].stichPoints
        self.game.round.opponent_points = 120 - self.matches[self.current_match].stichPoints
        return self.game.compute_rewards(is_training)

    def decode_action(self, action_id):
        card_encoding = get_card_encoding(self.game.state)
        return convert_action_id_to_card(action_id, card_encoding)

    def get_legal_actions(self):
        legal_actions = self.game.state['actions']
        card_encoding = get_card_encoding(self.game.state)
        if self.game.state["drueck"]:
            legal_actions = {convert_card_to_action_id(action, card_encoding): cards2array(action, card_encoding) for action in legal_actions}
        else:
            legal_actions = {convert_card_to_action_id(action, card_encoding): card2array(action, card_encoding) for action in legal_actions}
        return legal_actions

    def get_action_feature(self, action):
        card_encoding = get_card_encoding(self.game.state)
        if action < 100:
            return card2array(self.decode_action(action), card_encoding)
        else:
            return cards2array(self.decode_action(action), card_encoding)
