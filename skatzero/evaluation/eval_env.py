from skatzero.env.feature_transformations import extract_state
from skatzero.env.skat import SkatEnv


class EvalEnv(SkatEnv):
    def __init__(self, seed=None, gametype='D', lstm=[True, False, False], dealers=None):
        super().__init__(seed, gametype, False)
        self.lstm_list = lstm
        self.dealers = dealers
        self.dealer_id = 0

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
        state, player_id = self.game.init_game()

        if self.dealers is not None:
            self.game.round.initiate(self.game.players, dealer = self.dealers[self.dealer_id])
            self.dealer_id += 1
            player_id = self.game.round.current_player
            state = self.game.get_state(player_id)
            self.game.state = state

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
