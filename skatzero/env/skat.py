from skatzero.env.feature_transformations import cards2array, extract_state, card2array, get_card_encoding, convert_action_id_to_card, convert_card_to_action_id
from skatzero.evaluation.utils import print_turn
from skatzero.game.game import Game
from skatzero.evaluation.seeding import np_random


class SkatEnv(object):
    def __init__(self, seed=None, gametype='D'):
        self.name = 'skat'
        self.game = Game(gametype=gametype)

        self.num_players = self.game.get_num_players()
        self.num_actions = self.game.get_num_actions()

        self.timestep = 0

        self.base_seed = seed
        self.seed(seed)

        self.agents = None

        self.state_shape = [[551], [573], [573]]
        self.set_state_shape(gametype)

        self.action_shape = [[32] for _ in range(self.num_players)]

    def set_state_shape(self, gametype):
        if gametype == 'N':
            self.state_shape = [[310], [364], [364]]
        else:
            self.state_shape = [[551], [573], [573]]

    def reset(self):
        if self.base_seed is not None:
            self.base_seed += 1
            self.seed(self.base_seed)
        state, player_id = self.game.init_game()
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
            if not is_training:
                action, _ = self.agents[0].eval_step(state)
                if verbose > 0:
                    print_turn(state['raw_obs']['current_hand'], self.decode_action(action),
                                state['raw_obs']['self'], state['raw_obs']['trick'], state['raw_obs']['trump'], verbose)
            else:
                action = self.agents[0].step(state)

            trajectories[0].append(state)
            trajectories[0].append(action)

            action = self.decode_action(action)
            state = self.game.druecken(action)

            state = self.extract_state(state)


        trajectories[player_id].append(state)
        while not self.is_over():
            if not is_training:
                action, _ = self.agents[player_id].eval_step(state)
                if verbose > 0:
                    print_turn(state['raw_obs']['current_hand'], self.decode_action(action),
                               state['raw_obs']['self'], state['raw_obs']['trick'], state['raw_obs']['trump'], verbose)
            else:
                action = self.agents[player_id].step(state)

            next_state, next_player_id = self.step(action)

            trajectories[player_id].append(action)

            state = next_state
            player_id = next_player_id

            if not self.game.is_over():
                trajectories[player_id].append(state)

        for player_id in range(self.num_players):
            state = self.get_state(player_id)
            trajectories[player_id].append(state)

        rewards = self.get_rewards(is_training)

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
