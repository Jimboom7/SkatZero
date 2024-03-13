import numpy as np

from skatzero.env.game import GameEnv
from skatzero.env.feature_transformations import get_obs
from skatzero.env.utils import get_hand_distribution, evaluate_hand_strength, get_startplayer

suit_list = ['D', 'H', 'S', 'C']
rank_list = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [suit + rank for suit in suit_list for rank in rank_list]

class Env:
    """
    Skat multi-agent wrapper
    """
    def __init__(self):
        """
        Here, we use dummy agents.
        This is because, in the original game, the players
        are `in` the game. Here, we want to isolate
        players and environments to have a more gym style
        interface. To achieve this, we use dummy players
        to play. For each move, we tell the corresponding
        dummy player which action to play, then the player
        will perform the actual action in the game engine.
        """

        # Initialize players
        # We use three dummy player for the target position
        self.players = {}
        for position in ['soloplayer', 'opponent_left', 'opponent_right']:
            self.players[position] = DummyAgent(position)

        # Initialize the internal environment
        self._env = GameEnv(self.players)

        self.infoset = None

    def reset(self):
        """
        Every time reset is called, the environment
        will be re-initialized with a new deck of cards.
        This function is usually called when a game is over.
        """
        self._env.reset()

        # Randomly shuffle the deck
        _deck = deck.copy()
        np.random.shuffle(_deck)
        basic_cards = {'0': _deck[:10],
                          '1': _deck[10:20],
                          '2': _deck[20:30],
                          'skat_cards': _deck[30:32],
                          'suit': 'D',
                          'bids': {'0': 0, '1': 0, '2': 0},
                          'hand': np.random.randint(0, 9) == -1# 10% Handgame
            }
        #card_play_data = get_hand_distribution(basic_cards) # Only playing good hands leads to worse results

        strongest = 0
        s0 = evaluate_hand_strength(basic_cards['0'], 'D')[0][1]
        s1 = evaluate_hand_strength(basic_cards['1'], 'D')[0][1]
        s2 = evaluate_hand_strength(basic_cards['2'], 'D')[0][1]
        if s1 > s0 and s1 > s2:
            strongest = 1
        if s2 > s1 and s2 > s0:
            strongest = 2

        card_play_data = {'0': basic_cards[str(strongest)],
                          '1': basic_cards[str((strongest + 1) % 3)],
                          '2': basic_cards[str((strongest + 2) % 3)],
                          'suit': basic_cards['suit'],
                          'skat_cards': basic_cards['skat_cards'],
                          'hand': basic_cards['hand'],
                          'startplayer': get_startplayer(),
            }

        # Initialize the cards
        self._env.init_new_game(card_play_data)
        self.infoset = self._game_infoset

        return get_obs(self.infoset)

    def step(self, action):
        """
        Step function takes as input the action, which
        is a list of integers, and output the next obervation,
        reward, and a Boolean variable indicating whether the
        current game is finished. It also returns an empty
        dictionary that is reserved to pass useful information.
        """
        assert action in self.infoset.legal_actions
        self.players[self._acting_player_position].set_action(action)
        self._env.step()
        self.infoset = self._game_infoset
        done = False
        reward = 0.0
        if self._game_over:
            done = True
            reward = self._get_reward()
            obs = None
        else:
            obs = get_obs(self.infoset)
        return obs, reward, done, {}

    def _get_reward(self):
        """
        This function is called in the end of each
        game. It returns either 1/-1 for win/loss,
        or ADP, i.e., every bomb will double the score.
        Reward will be made non negative later for opponents.
        """
        return self._env.solo_reward - self._env.opponent_reward

    @property
    def _game_infoset(self):
        """
        Here, inforset is defined as all the information
        in the current situation, incuding the hand cards
        of all the players, all the historical moves, etc.
        That is, it contains perfect infomation. Later,
        we will use functions to extract the observable
        information from the views of the three players.
        """
        return self._env.game_infoset

    @property
    def _game_winner(self):
        """ A string of soloplayer/opponents
        """
        return self._env.get_winner()

    @property
    def _acting_player_position(self):
        """
        The player that is active. It can be soloplayer,
        landlod_down, or opponent_left.
        """
        return self._env.acting_player_position

    @property
    def _game_over(self):
        """ Returns a Boolean
        """
        return self._env.game_over

class DummyAgent(object):
    """
    Dummy agent is designed to easily interact with the
    game engine. The agent will first be told what action
    to perform. Then the environment will call this agent
    to perform the actual action. This can help us to
    isolate environment and agents towards a gym like
    interface.
    """
    def __init__(self, position):
        self.position = position
        self.action = None

    def act(self, infoset):
        """
        Simply return the action that is set previously.
        """
        assert self.action in infoset.legal_actions
        return self.action

    def set_action(self, action):
        """
        The environment uses this function to tell
        the dummy agent what to do.
        """
        self.action = action
