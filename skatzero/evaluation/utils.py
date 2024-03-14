import functools

from skatzero.game.utils import card_suit_as_number, card_rank_as_number, compare_cards

def skat_sort_card_string(card_1, card_2):
    key = []
    for card in [card_1, card_2]:
        key.append((card_suit_as_number[card[0]] * 10) + card_rank_as_number[card[1]])
        if card[1] == "J":
            key[-1] *= -1
    if key[0] > key[1]:
        return 1
    if key[0] < key[1]:
        return -1
    return 0


def format_card(card):
    suits = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣' }

    output = ""
    if card[1] == "J":
        output += "\033[95m"
    elif card[0] == "D":
        output += "\033[33m"
    elif card[0] == "H":
        output += "\033[31m"
    elif card[0] == "S":
        output += "\033[34m"
    elif card[0] == "C":
        output += "\033[32m"

    if card[1] == "T":
        output += "10" + suits[card[0]] + "\033[0m"
    else:
        output += card[1] + suits[card[0]] + "\033[0m"

    return output


def format_hand(cards):
    cards.sort(key=functools.cmp_to_key(skat_sort_card_string))

    hand = ""
    for c in cards:
        hand += format_card(c) + " \033[0m"
    return hand

def print_turn(cards, action, player_nr, trick, trump, verbose):
    player = player_number_to_name(player_nr)

    if verbose == 2:
        print(player + " Hand: " + format_hand(cards))
    print(player + " Throws: " + format_card(action))

    if len(trick) == 2:
        check_trick(trick, action, player_nr, trump)

def check_trick(trick, action, player_nr, trump):
    suit = trick[0][1][0]
    trick_winner = trick[0][0].player_id
    card1 = trick[0][1]
    card2 = trick[1][1]
    card3 = action
    highest_card = card1
    if not compare_cards(card1, card2, trump, suit):
        highest_card = card2
        trick_winner = trick[1][0].player_id
    if not compare_cards(highest_card, card3, trump, suit):
        trick_winner = player_nr
    print(player_number_to_name(trick_winner) + " wins the Trick: " + format_card(card1) + ", " + format_card(card2) + ", " + format_card(card3))

def player_number_to_name(player_nr):
    player = 'Soloplayer'
    if player_nr == 1:
        player = 'Opponent Right'
    if player_nr == 2:
        player = 'Opponent Left'
    return player
