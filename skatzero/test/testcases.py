from skatzero.test.utils import construct_state_from_history

def case1(raw_state):
    print("Trumpf ziehen")
    # https://www.youtube.com/watch?v=rc0C9xftSfs
    raw_state['self'] = 0
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ["SJ", "HJ", "DJ", "DK", "D9", "D7", "HA", "HK", "H8"]
    raw_state['trace'] = [(1, "S7"), (2, "SQ"), (0, "SA")]
    raw_state['skat'] = ['CQ', 'S9']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick

    return raw_state, ('SJ', 'HJ', 'DJ')

def case2(raw_state):
    print("Letzten Trumpf korrekt ziehen")
    # Sollte nicht D8 priorisieren, da Gegner nurnoch D9 Trumpf haben
    raw_state['self'] = 0
    raw_state['points'] = [50, 11]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 1, 'N': 0},
                    {'D': 0, 'H': 1, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 1, 1]

    raw_state['current_hand'] = ["CJ", "DA", "D8", "SA", "S8"]
    raw_state['trace'] = [(1, "HT"), (2, "HA"), (0, "DT"), (0, "DJ"), (1, "SJ"), (2, "DK"), (1, "H8"), (2, "HQ"), (0, "C7"), (2, "CA"), (0, "DQ"), (1, "C9"), (0, "HJ"), (1, "CQ"), (2, "D7")]
    raw_state['skat'] = ["H7", "HK"]
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick

    return raw_state, ('CJ', 'DA')

def case3(raw_state):
    print("Schweres Youtube Rätsel")
    # Schweres Rätsel: https://www.youtube.com/watch?v=7VCsp3BiJvQ - Nur Herz Ass führt zum Sieg
    raw_state['self'] = 0
    raw_state['points'] = [13, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DA', 'DT', 'DQ', 'D7', 'CA', 'HA', 'H9']
    raw_state['trace'] = [(1, 'H8'), (2, 'HQ'), (0, 'HK'), (0, 'SJ'), (1, 'D8'), (2, 'S7')]
    raw_state['skat'] = ["S8", "CK"]
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HA')

def case4(raw_state):
    print("Schmieren als Letzter")
    raw_state['self'] = 2
    raw_state['points'] = [3, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['S7', 'S8', 'SQ', 'ST', 'SA', 'CA', 'HA', 'H9', 'HQ']
    raw_state['trace'] = [(0, 'DQ'), (1, 'D9'), (2, 'D8'), (0, 'DA'), (1, 'CJ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('ST', 'SA', 'CA', 'HA')

def case5(raw_state):
    print("Schmieren als Zweiter I")
    raw_state['self'] = 1
    raw_state['points'] = [3, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['S7', 'S8', 'SQ', 'ST', 'SA', 'CA', 'HA', 'H9', 'HQ']
    raw_state['trace'] = [(0, 'DQ'), (1, 'D9'), (2, 'D8'), (0, 'D7')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('ST', 'SA', 'CA', 'HA')

def case6(raw_state):
    print("Schmieren als Zweiter II")
    raw_state['self'] = 1
    raw_state['points'] = [3, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['S7', 'S8', 'SQ', 'ST', 'SA', 'CA', 'HA', 'H9', 'HQ']
    raw_state['trace'] = [(0, 'DQ'), (1, 'D9'), (2, 'D8'), (0, 'DJ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('ST', 'SA', 'CA', 'HA')

def case7(raw_state):
    print("Tauchen für 10 als Letzter")
    raw_state['self'] = 0
    raw_state['points'] = [27, 12]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DA', 'D8', 'D9', 'DQ', 'DK', 'HA', 'H7', 'S7']
    raw_state['trace'] = [(0, 'CJ'), (1, 'SJ'), (2, 'HJ'), (0, 'D7'), (1, 'DJ'), (2, 'DT'), (1, 'H8'), (2, 'HK')]
    raw_state['skat'] = ['ST', 'SA']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('H7')

def case8(raw_state):
    print("Abwerfen")
    raw_state['self'] = 0
    raw_state['points'] = [20, 12]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DA', 'D8', 'D9', 'DQ', 'DK', 'HA', 'H7', 'S7']
    raw_state['trace'] = [(0, 'CJ'), (1, 'SJ'), (2, 'HJ'), (0, 'D7'), (1, 'DJ'), (2, 'DT'), (1, 'C8'), (2, 'C9')]
    raw_state['skat'] = ['ST', 'HK']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S7')

def case9(raw_state):
    print("Niedrig stechen")
    # https://www.youtube.com/watch?v=F4GpL5C0S04
    raw_state['self'] = 0
    raw_state['points'] = [3, 10]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['SJ', 'HJ', 'DJ', 'DT', 'DQ', 'D8', 'HA', 'HQ', 'H7']
    raw_state['trace'] = [(1, 'C8'), (2, 'CT'), (0, 'C7'), (2, 'CQ')]
    raw_state['skat'] = ['S9', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('D8', 'DQ') # DT eventuell, aber laut Daniel nicht


def case10(raw_state):
    print("Trumpfgabel vorbereiten I")
    # https://www.youtube.com/watch?v=F4GpL5C0S04
    raw_state['self'] = 0
    raw_state['points'] = [11, 25]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DT', 'D8', 'HA', 'HQ', 'H7']
    raw_state['trace'] = [(1, 'C8'), (2, 'CT'), (0, 'C7'), (2, 'CQ'), (0, 'DQ'), (1, 'C9'), (0, 'SJ'), (1, 'D7'), (2, 'D9'),
                          (0, 'DJ'), (1, 'SA'), (2, 'CJ'), (2, 'S7')]
    raw_state['skat'] = ['S9', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('D8') # Nicht abwerfen, Trumpfgleichstand erreichen

def case11(raw_state):
    print("Trumpfgabel vorbereiten II")
    # https://www.youtube.com/watch?v=F4GpL5C0S04
    raw_state['self'] = 0
    raw_state['points'] = [11, 25]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DT', 'HA', 'HQ', 'H7']
    raw_state['trace'] = [(1, 'C8'), (2, 'CT'), (0, 'C7'), (2, 'CQ'), (0, 'DQ'), (1, 'C9'), (0, 'SJ'), (1, 'D7'), (2, 'D9'),
                          (0, 'DJ'), (1, 'SA'), (2, 'CJ'), (2, 'S7'), (0, 'D8'), (1, 'S8')]
    raw_state['skat'] = ['S9', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HA')

def case12(raw_state):
    print("Trumpfgabel vorbereiten III")
    # https://www.youtube.com/watch?v=F4GpL5C0S04
    raw_state['self'] = 0
    raw_state['points'] = [22, 25]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DT', 'HQ', 'H7']
    raw_state['trace'] = [(1, 'C8'), (2, 'CT'), (0, 'C7'), (2, 'CQ'), (0, 'DQ'), (1, 'C9'), (0, 'SJ'), (1, 'D7'), (2, 'D9'),
                          (0, 'DJ'), (1, 'SA'), (2, 'CJ'), (2, 'S7'), (0, 'D8'), (1, 'S8'), (0, 'HA'), (1, 'H9'), (2, 'H8')]
    raw_state['skat'] = ['S9', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('H7')

def case13(raw_state):
    print("Trumpfgabel vorbereiten IV")
    # https://www.youtube.com/watch?v=F4GpL5C0S04
    raw_state['self'] = 0
    raw_state['points'] = [22, 39]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DT', 'HQ']
    raw_state['trace'] = [(1, 'C8'), (2, 'CT'), (0, 'C7'), (2, 'CQ'), (0, 'DQ'), (1, 'C9'), (0, 'SJ'), (1, 'D7'), (2, 'D9'),
                          (0, 'DJ'), (1, 'SA'), (2, 'CJ'), (2, 'S7'), (0, 'D8'), (1, 'S8'), (0, 'HA'), (1, 'H9'), (2, 'H8'),
                          (0, 'H7'), (1, 'HK'), (2, 'HT'), (2, 'SK')]
    raw_state['skat'] = ['S9', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HQ')

def case14(raw_state):
    print("Trumpfgabel ausführen")
    # https://www.youtube.com/watch?v=F4GpL5C0S04
    raw_state['self'] = 0
    raw_state['points'] = [22, 56]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DT']
    raw_state['trace'] = [(1, 'C8'), (2, 'CT'), (0, 'C7'),
                          (2, 'CQ'), (0, 'DQ'), (1, 'C9'),
                          (0, 'SJ'), (1, 'D7'), (2, 'D9'),
                          (0, 'DJ'), (1, 'SA'), (2, 'CJ'),
                          (2, 'S7'), (0, 'D8'), (1, 'S8'),
                          (0, 'HA'), (1, 'H9'), (2, 'H8'),
                          (0, 'H7'), (1, 'HK'), (2, 'HT'),
                          (2, 'SK'), (0, 'HQ'), (1, 'ST'),
                          (1, 'CK'), (2, 'DK')]
    raw_state['skat'] = ['S9', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DT')

def case15(raw_state):
    print("Schneider machen")
    # https://www.youtube.com/watch?v=gwtw25mHM-U
    raw_state['self'] = 0
    raw_state['points'] = [35, 22]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['D8', 'D9', 'DQ', 'H8', 'HT', 'HA']
    raw_state['trace'] = [(0, 'CJ'), (1, 'DK'), (2, 'DJ'),
                          (0, 'SJ'), (1, 'S7'), (2, 'HJ'),
                          (0, 'D7'), (1, 'CA'), (2, 'DA'),
                          (2, 'CT'), (0, 'DT'), (1, 'C7')]
    raw_state['skat'] = ['S8', 'CQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('H8') # Idee: Beste Schneiderchance, da wenn Herz 1/3 steht beide bedienen müssen und maximal 7 Augen möglich sind

def case16(raw_state):
    print("Abwerfen trotz Vollem")
    # https://www.youtube.com/watch?v=XPA0vd3ybik
    raw_state['self'] = 0
    raw_state['points'] = [7, 13]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['C8', 'C9', 'CJ', 'DJ', 'DA', 'DT', 'DK', 'DQ']
    raw_state['trace'] = [(0, 'D9'), (1, 'HJ'), (2, 'D8'),
                          (1, 'HA'), (2, 'H7'), (0, 'H9'),
                          (1, 'HT'), (1, 'H8')]
    raw_state['skat'] = ['SQ', 'SK']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('C8', 'C9') # Idee: Verlustrechnung, man sollte Kreuz abwerfen

def case17(raw_state):
    print("Farbe vor Trumpf")
    # https://www.youtube.com/watch?v=XPA0vd3ybik
    raw_state['self'] = 0
    raw_state['points'] = [28, 13]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['C8', 'C9', 'CJ', 'DJ', 'DT', 'DK', 'DQ']
    raw_state['trace'] = [(0, 'D9'), (1, 'HJ'), (2, 'D8'),
                          (1, 'HA'), (2, 'H7'), (0, 'H9'),
                          (1, 'HT'), (1, 'H8'), (0, 'DA')]
    raw_state['skat'] = ['SQ', 'SK']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('C8', 'C9') # Idee: Trumpf spielen gibt einem Gegner die Chance abzuwerfen

def case18(raw_state):
    print("Gegenspieler: Kurze Farbe abwerfen")
    # https://www.youtube.com/watch?v=tpHryzjFa5A -> Erster Zug: Blanke Pik 9 (kurze Farbe)
    raw_state['self'] = 1
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'SJ', 'D7', 'DT', 'HA', 'H9', 'S9', 'C8', 'C9', 'CQ']
    raw_state['trace'] = []
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S9') # Idee: Einzelne Farbe abwerfen

def case19(raw_state):
    print("Gegenspieler: Trumpf spielen")
    # https://www.youtube.com/watch?v=1FSASQ9hQaY
    raw_state['self'] = 1
    raw_state['points'] = [0, 7]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'H7', 'H8', 'HQ', 'HK', 'S7', 'SK', 'C7', 'CK']
    raw_state['trace'] = [(0, 'D9'), (1, 'DK'), (2, 'DQ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('CJ') # Idee: Man will später nicht mehr am Stich sein, damit Partner stärker ist

def case20(raw_state):
    print("Alleinspieler: Korrekten Trumpf spielen")
    # https://www.youtube.com/watch?v=fOu3rGDIKc4
    raw_state['self'] = 0
    raw_state['points'] = [22, 21]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'D9', 'DK', 'H8', 'HT', 'S8', 'ST']
    raw_state['trace'] = [(0, 'SJ'), (1, 'DJ'), (2, 'D8'),
                          (0, 'D7'), (1, 'DA'), (2, 'DT'),
                          (1, 'CK'), (2, 'C9'), (0, 'CA')]
    raw_state['skat'] = ['C8', 'CQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HJ') # Idee: Falls Trümpfe auf einer Hand sind kann man später mit dem König noch die Dame abgreifen

def case21(raw_state):
    print("Gegenspieler: Kurze Farbe starten")
    # https://www.youtube.com/watch?v=rbF94L7M8L0
    raw_state['self'] = 1
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['SJ', 'DJ', 'DT', 'CQ', 'CK', 'CT', 'S8', 'SK', 'H8', 'H9']
    raw_state['trace'] = []
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('SK') # König aus der kurzen Farbe

def case22(raw_state):
    print("Gegenspieler Ausnahme: Lange Farbe starten")
    # https://www.youtube.com/watch?v=rbF94L7M8L0
    raw_state['self'] = 1
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'D8', 'S7', 'S9', 'SQ', 'SA', 'H8', 'HT', 'C7', 'C8']
    raw_state['trace'] = []
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S7', 'S9') # Lusche aus der langen Farbe

def case23(raw_state):
    print("Gegenspieler: Zweite Karte I")
    # https://www.youtube.com/watch?v=rbF94L7M8L0
    raw_state['self'] = 2
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DK', 'S7', 'SQ', 'ST', 'H8', 'HT', 'C7', 'CA']
    raw_state['trace'] = [(1, 'HQ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('H8') # 8 auf Dame ist Pflicht

def case24(raw_state):
    print("Gegenspieler: Zweite Karte II")
    # https://www.youtube.com/watch?v=rbF94L7M8L0
    raw_state['self'] = 2
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DK', 'S7', 'SQ', 'ST', 'H8', 'HT', 'C7', 'CA']
    raw_state['trace'] = [(1, 'H7')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HT') # 10 auf Lusche ist Pflicht

def case25(raw_state):
    print("Gegenspieler: Zweite Karte III")
    # https://www.youtube.com/watch?v=rbF94L7M8L0
    raw_state['self'] = 2
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DK', 'S7', 'SQ', 'ST', 'H8', 'HT', 'C7', 'CA']
    raw_state['trace'] = [(1, 'SK')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S7')

def case26(raw_state):
    print("Gegenspieler: Zweite Karte IV")
    # https://www.youtube.com/watch?v=rbF94L7M8L0
    raw_state['self'] = 2
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DK', 'S7', 'SQ', 'ST', 'H8', 'HT', 'C7', 'CA']
    raw_state['trace'] = [(1, 'S9')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('SQ', 'S7')

