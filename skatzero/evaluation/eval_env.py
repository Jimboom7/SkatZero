from skatzero.env.feature_transformations import extract_state
from skatzero.env.skat import SkatEnv


class EvalEnv(SkatEnv):
    def __init__(self, seed=None, gametype='D', dealers=None):
        super().__init__(seed, gametype)
        self.dealers = dealers
        self.dealer_id = 0

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

        return self.extract_state(state), player_id

    def step(self, action):
        action = self.decode_action(action)
        self.timestep += 1
        next_state, player_id = self.game.step(action)
        self.current_player_id = player_id

        return self.extract_state(next_state), player_id

    def get_state(self, player_id):
        self.current_player_id = player_id
        return self.extract_state(self.game.get_state(player_id))
