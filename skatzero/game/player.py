from copy import deepcopy


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.current_hand = []
        self.role = ''
        self.played_cards = None

    def get_state(self, public, others_hands, points, actions, trick, blind_hand):
        state = {}
        state['soloplayer'] = public['soloplayer']
        state['trace'] = public['trace']
        state['played_cards'] = public['played_cards']
        state['self'] = self.player_id
        state['current_hand'] = self.current_hand
        state['others_hand'] = others_hands
        state['points'] = points
        state['actions'] = actions
        state['trick'] = trick
        state['blind_hand'] = blind_hand

        return deepcopy(state)

    def available_actions(self, suit=None, trump='D'):
        playable_cards = []
        if suit is not None:
            for card in self.current_hand:
                if (card[0] == suit and card[1] != 'J') or (suit == trump and card[1] == 'J'):
                    playable_cards.append(card)

        if suit is None or not playable_cards:
            for card in self.current_hand:
                playable_cards.append(card)

        return playable_cards

    def play(self, action):
        for i, card in enumerate(self.current_hand):
            if card[0] == action[0] and card[1] == action[1]:
                self.current_hand.remove(self.current_hand[i])
                break
        self.played_cards = action
