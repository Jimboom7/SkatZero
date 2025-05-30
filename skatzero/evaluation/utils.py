import functools

from skatzero.game.utils import card_suit_as_number, card_rank_as_number, compare_cards


def swap_colors(cards, color1, color2):
    return [color2+card[1] if card[0]==color1 and card[1]!='J' else color1+card[1] if card[0]==color2 and card[1]!='J' else card for card in cards]

def swap_bids(bids, color1, color2):
    tmp = bids[color1]
    bids[color1] = bids[color2]
    bids[color2] = tmp
    return bids

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
    else:
        return format_card(card[0]) + format_card(card[1]) # Druecken

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
    print(player + " Throws: " + format_card(action) + "\n")

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
    print(player_number_to_name(trick_winner) + " wins the Trick: " + format_card(card1) + ", " + format_card(card2) + ", " + format_card(card3) + "\n")

def player_number_to_name(player_nr):
    player = 'Soloplayer'
    if player_nr == 1:
        player = 'Opponent Left'
    if player_nr == 2:
        player = 'Opponent Right'
    return player

def parse_bid(bid_value, pos, bids, bid_jacks):
    d_bids = [18, 27, 45]
    h_bids = [20, 30, 40, 50]
    s_bids = [22, 33, 44, 55]
    c_bids = [24, 36, 48, 60]
    n_bids = [23, 35, 46, 59]

    if bid_value in d_bids:
        bids[pos]['D'] = 1
        if bid_value != 18:
            bid_jacks[pos] = int(bid_value / 9) - 1
    elif bid_value in h_bids:
        bids[pos]['H'] = 1
        bid_jacks[pos] = int(bid_value / 10) - 1
    elif bid_value in s_bids:
        bids[pos]['S'] = 1
        bid_jacks[pos] = int(bid_value / 11) - 1
    elif bid_value in c_bids:
        bids[pos]['C'] = 1
        bid_jacks[pos] = int(bid_value / 12) - 1
    elif bid_value in n_bids:
        bids[pos]['N'] = 1

    return bids, bid_jacks