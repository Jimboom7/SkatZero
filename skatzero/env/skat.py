from skatzero.game.utils import action_2_id, id_2_action
from skatzero.env.feature_transformations import extract_state, card2array
from skatzero.game.game import Game
from skatzero.evaluation.seeding import np_random


class SkatEnv(object):
    def __init__(self, seed=None):
        self.name = 'skat'
        self.game = Game()

        self.action_recorder = []

        self.num_players = self.game.get_num_players()
        self.num_actions = self.game.get_num_actions()

        self.timestep = 0

        self.seed(seed)

        self.agents = None

        self.state_shape = [[1490], [1522], [1522]]
        self.action_shape = [[32] for _ in range(self.num_players)]

    def reset(self):
        state, player_id = self.game.init_game()
        self.action_recorder = []
        return self.extract_state(state), player_id

    def step(self, action):
        action = self.decode_action(action)
        self.timestep += 1
        self.action_recorder.append((self.get_player_id(), action))
        next_state, player_id = self.game.step(action)

        return self.extract_state(next_state), player_id

    def set_agents(self, agents):
        self.agents = agents

    def run(self, is_training=False):
        trajectories = [[] for _ in range(self.num_players)]
        state, player_id = self.reset()

        trajectories[player_id].append(state)
        while not self.is_over():

            if not is_training:
                action, _ = self.agents[player_id].eval_step(state)
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

        rewards = self.get_rewards()

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
        extracted_state = extract_state(state, self.game, self.get_legal_actions(), self.action_recorder)
        return extracted_state

    def get_rewards(self):
        return self.game.compute_rewards()

    def decode_action(self, action_id):
        return id_2_action(action_id)

    def get_legal_actions(self):
        legal_actions = self.game.state['actions']
        legal_actions = {action_2_id(action): card2array(action) for action in legal_actions}
        return legal_actions

    def get_action_feature(self, action):
        return card2array(self.decode_action(action))
