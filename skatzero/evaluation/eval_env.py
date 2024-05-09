from skatzero.env.feature_transformations import extract_state
from skatzero.env.skat import SkatEnv


class EvalEnv(SkatEnv):
    def __init__(self, blind_hand_chance = 0.1, seed=None, gametype='D', open_hand_chance = 0.1, lstm=[True, False, False]):
        super().__init__(blind_hand_chance, seed, gametype, open_hand_chance, False)
        self.lstm_list = lstm

        if lstm[0]:
            self.state_shape[0][0] -= 1050
        if lstm[1]:
            self.state_shape[1][0] -= 1050
        if lstm[2]:
            self.state_shape[2][0] -= 1050

    def extract_state(self, state, player_id):
        extracted_state = extract_state(state, self.get_legal_actions(), self.lstm_list[player_id])
        return extracted_state

    def reset(self):
        if self.base_seed is not None:
            self.base_seed += 1
            self.seed(self.base_seed)
        is_blind_hand = self.np_random.rand() < self.blind_hand_chance
        is_open_hand = self.np_random.rand() < self.open_hand_chance
        state, player_id = self.game.init_game(blind_hand=is_blind_hand, open_hand=is_open_hand)

        return self.extract_state(state, player_id), player_id

    def step(self, action):
        action = self.decode_action(action)
        self.timestep += 1
        next_state, player_id = self.game.step(action)
        self.current_player_id = player_id

        return self.extract_state(next_state, player_id), player_id
    
    def get_state(self, player_id):
        self.current_player_id = player_id
        return self.extract_state(self.game.get_state(player_id), player_id)
