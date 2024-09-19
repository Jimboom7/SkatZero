from skatzero.game.utils import init_32_deck

def run_testcase(testcase, raw_state, env, agents, log_to_file=False):
    raw_state, expected = testcase(raw_state)

    state = env.extract_state(raw_state)

    if log_to_file:
        with open('obs.txt', 'a') as the_file:
            for obs in state['obs']:
                the_file.write('    ' + str(obs) + ',\n')

    _, info = agents[raw_state['self']].eval_step(state)

    print(testcase.__name__)
    print("Expected: " + str(expected))
    print("Output: " + str(info))
    wrong_difference = 999
    correct_difference = 999
    for c in info['values']:
        if c in expected and max(info['values'].values()) - info['values'][c] < wrong_difference:
            wrong_difference = max(info['values'].values()) - info['values'][c]
    for c in info['values']:
        if c not in expected and max(info['values'].values()) - info['values'][c] < correct_difference:
            correct_difference = max(info['values'].values()) - info['values'][c]
    if raw_state['self'] != 0:
        wrong_difference *= 4
        correct_difference *= 4
    if wrong_difference == 0:
        print("\033[32mPassed!\033[0m Difference: " + str(correct_difference) + "\n")
    if correct_difference == 0:
        print("\033[31mFailed!\033[0m Difference: " + str(-wrong_difference) + "\n")
    return -wrong_difference, correct_difference, raw_state["self"]

def construct_state_from_history(current_hand, card_history, skat, trump='D'):
    played_cards = [[],[],[]]
    others_cards = init_32_deck()
    for p, c in card_history:
        played_cards[p].append(c)
        others_cards.remove(c)
    for c in current_hand:
        others_cards.remove(c)
    for c in skat:
        others_cards.remove(c)

    trick = []
    if len(card_history) % 3 == 1:
        trick.append(card_history[-1])
    if len(card_history) % 3 == 2:
        trick.append(card_history[-2])
        trick.append(card_history[-1])

    if len(trick) == 0:
        actions = available_actions(current_hand, suit=None, trump=trump)
    else:
        suit = trick[0][1][0]
        if trick[0][1][1] == 'J' and trump is not None:
            suit = trump
        actions = available_actions(current_hand, suit, trump)

    return played_cards, others_cards, trick, actions

def available_actions(current_hand, suit=None, trump='D'):
    playable_cards = []
    if len(current_hand) == 12:
        for i, card in enumerate(current_hand):
            for j, card2 in enumerate(current_hand):
                if i >= j:
                    continue
                playable_cards.append([card, card2])
    else:
        if suit is not None:
            for card in current_hand:
                if (card[0] == suit and card[1] != 'J') or (suit == trump and card[1] == 'J') or (card[0] == suit and trump is None):
                    playable_cards.append(card)

        if suit is None or not playable_cards:
            for card in current_hand:
                playable_cards.append(card)

    return playable_cards
