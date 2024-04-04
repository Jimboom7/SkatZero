from skatzero.test.utils import construct_state_from_history

def case1_easy(raw_state):
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

def case2_easy(raw_state):
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

def case3_easy(raw_state):
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

def case4_easy(raw_state):
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

def case5_easy(raw_state):
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

def case6_easy(raw_state):
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

def case7_easy(raw_state):
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

def case8_easy(raw_state):
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

def case9_easy(raw_state):
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

def case10_easy(raw_state):
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

def case1_medium(raw_state):
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

def case2_medium(raw_state):
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

def case3_medium(raw_state):
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

def case4_medium(raw_state):
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

def case5_medium(raw_state):
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

def case6_medium(raw_state):
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

def case7_medium(raw_state):
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

def case8_medium(raw_state):
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

def case9_medium(raw_state):
    print("Gegenspieler: König aus kurzer Farbe starten")
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

def case10_medium(raw_state):
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

def case11_medium(raw_state):
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

def case12_medium(raw_state):
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

def case13_medium(raw_state):
    print("GameDuell Skat Masters: 10 (hoch) zurückbehalten")
    # https://www.youtube.com/watch?v=TXCF53VsLdM 2:30 Minuten
    raw_state['self'] = 0
    raw_state['points'] = [28, 22]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'DT', 'D8', 'D7', 'ST', 'SQ', 'S7']
    raw_state['trace'] = [(1, 'SA'), (2, 'SK'), (0, 'S8'),
                          (1, 'C7'), (2, 'CK'), (0, 'CA'),
                          (0, 'D9'), (1, 'DQ'), (2, 'DK'),
                          (2, 'S9')]
    raw_state['skat'] = ['HT', 'HQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('SQ') # [Mittel] Eindeutig richtiger Zug, 10 oder 7 wäre int

def case14_medium(raw_state):
    print("GameDuell Skat Masters: Farbe weiterspielen")
    # https://youtu.be/TXCF53VsLdM?feature=shared&t=473
    raw_state['self'] = 2
    raw_state['points'] = [0, 14]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DA', 'DK', 'CA', 'C7', 'SK', 'S9', 'S7', 'HA', 'H7']
    raw_state['trace'] = [(1, 'S8'), (2, 'SA'), (0, 'SQ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('SK', 'S9', 'S7') # [Mittel] Idee: Teammate soll 10 stechen

def case15_medium(raw_state):
    print("GameDuell Skat Masters: 'Pik Ass rein, 60!'")
    # https://youtu.be/TXCF53VsLdM?feature=shared&t=1145
    raw_state['self'] = 1
    raw_state['points'] = [18, 45]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CT', 'C7', 'SA']
    raw_state['trace'] = [(2, 'HA'), (0, 'H9'), (1, 'HK'),
                          (2, 'HT'), (0, 'HQ'), (1, 'H7'),
                          (2, 'H8'), (0, 'D7'), (1, 'DT'),
                          (1, 'S8'), (2, 'SQ'), (0, 'CK'),
                          (2, 'C8'), (0, 'CA'), (1, 'C9'),
                          (0, 'DJ'), (1, 'D9'), (2, 'D8'),
                          (0, 'CJ'), (1, 'S7'), (2, 'DQ'),
                          (0, 'HJ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('SA') # [Mittel] Nur Pik Ass gewinnt das Spiel!

def case16_medium(raw_state):
    print("Mit Ass stechen")
    # https://youtu.be/Szf4DtWNgZ8?si=W0Poyk0OhxhJ42j6&t=203
    raw_state['self'] = 0
    raw_state['points'] = [17, 4]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 1, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 1, 0]

    raw_state['current_hand'] = ['DJ', 'DA', 'DT', 'DQ', 'SA', 'ST', 'S9', 'C9']
    raw_state['trace'] = [(1, 'H7'), (2, 'HQ'), (0, 'HA'),
                          (0, 'D9'), (1, 'D8'), (2, 'DK'),
                          (2, 'HT')]
    raw_state['skat'] = ['C8', 'CQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DA', 'DT') # Mit Ass oder Zehn stechen

def case17_medium(raw_state):
    print("Tauchen um später überzustechen")
    # https://youtu.be/Szf4DtWNgZ8?si=vIUSVzTxvZjTuNS1&t=420
    raw_state['self'] = 1
    raw_state['points'] = [23, 11]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 1, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 1, 0]

    raw_state['current_hand'] = ['CJ', 'DQ', 'SA', 'ST', 'SK', 'S9', 'C8', 'C7']
    raw_state['trace'] = [(1, 'HA'), (2, 'H9'), (0, 'H8'),
                          (1, 'HT'), (2, 'HQ'), (0, 'DT'),
                          (0, 'DJ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DQ') # Mit Ass oder Zehn stechen

def case18_medium(raw_state):
    print("Gegenspieler: Trümpfe ziehen")
    # https://youtu.be/Szf4DtWNgZ8?si=DQT21F6B0WIEnH9P&t=1104
    raw_state['self'] = 2
    raw_state['points'] = [14, 22]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 1, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 1, 0]

    raw_state['current_hand'] = ['HJ', 'DK', 'DQ', 'ST', 'HT', 'CK', 'CQ']
    raw_state['trace'] = [(1, 'H7'), (2, 'H8'), (0, 'DT'),
                          (0, 'CJ'), (1, 'SJ'), (2, 'D7'),
                          (0, 'D8'), (1, 'HA'), (2, 'DA')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HJ', 'DK', 'DQ') # Gegner hat nurnoch 2 Trumpf - kann man abziehen

def case19_medium(raw_state):
    print("Gegenspieler: Schnibbeln")
    # https://youtu.be/Szf4DtWNgZ8?si=cf6oYrRgNRGnzO0r&t=2412
    raw_state['self'] = 1
    raw_state['points'] = [22, 9]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 1, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 1, 0]

    raw_state['current_hand'] = ['CJ', 'C8', 'SA', 'SK', 'HA', 'HK']
    raw_state['trace'] = [(2, 'S7'), (0, 'DA'), (1, 'S8'),
                          (0, 'D7'), (1, 'D9'), (2, 'DJ'),
                          (2, 'C9'), (0, 'CA'), (1, 'C7'),
                          (0, 'DQ'), (1, 'HJ'), (2, 'SJ'),
                          (2, 'H7'), (0, 'HQ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HK') # Schnibbeln

def case20_medium(raw_state):
    print("Gegenspieler: Tauchen für Trumpf Ass")
    # https://youtu.be/Szf4DtWNgZ8?si=G3ePirdr9ZlJjUWW&t=2845
    raw_state['self'] = 0
    raw_state['points'] = [34, 17]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DT', 'DK', 'C8', 'S9', 'H9']
    raw_state['trace'] = [(2, 'S7'), (0, 'SA'), (1, 'SQ'),
                          (0, 'D8'), (1, 'D9'), (2, 'DQ'),
                          (2, 'SK'), (0, 'S8'), (1, 'ST'),
                          (1, 'SJ'), (2, 'DJ')]
    raw_state['skat'] = ['CT', 'HT']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DK') # So kriegt man Trumpf Ass später

def case21_medium(raw_state):
    print("Alleinspieler: Rest korrekt mitnehmen")
    # https://youtu.be/Szf4DtWNgZ8?si=hyenosTTx5Vo7kk2&t=2909
    raw_state['self'] = 0
    raw_state['points'] = [34, 43]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DT', 'S9']
    raw_state['trace'] = [(2, 'S7'), (0, 'SA'), (1, 'SQ'),
                          (0, 'D8'), (1, 'D9'), (2, 'DQ'),
                          (2, 'SK'), (0, 'S8'), (1, 'ST'),
                          (1, 'SJ'), (2, 'DJ'), (0, 'DK'),
                          (1, 'CK'), (2, 'CA'), (0, 'C8'),
                          (2, 'C9'), (0, 'H9'), (1, 'CQ'),
                          (1, 'C7'), (2, 'HQ')]
    raw_state['skat'] = ['CT', 'HT']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DT') # Damit hat man danach Rest. Mit S9 gewinnt man eigentlich auch

def case22_medium(raw_state):
    print("Alleinspieler: Trumpf von oben, dann von unten")
    # https://www.youtube.com/watch?v=02uYiQxAO8s
    raw_state['self'] = 0
    raw_state['points'] = [4, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'SJ', 'DT', 'DQ', 'D7', 'CA', 'CT', 'CK', 'C8', 'S8']
    raw_state['trace'] = []
    raw_state['skat'] = ['HK', 'S9']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('CJ', 'SJ') # Ersten von oben. Damit bei 3:3 Verteilung den Überstich abgewehrt

def case23_medium(raw_state):
    print("Alleinspieler: Trumpf von oben, dann von unten")
    # https://www.youtube.com/watch?v=02uYiQxAO8s
    raw_state['self'] = 0
    raw_state['points'] = [6, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'DT', 'DQ', 'D7', 'CA', 'CT', 'CK', 'C8', 'S8']
    raw_state['trace'] = [(0, 'SJ'), (1, 'D8'), (2, 'D9')]
    raw_state['skat'] = ['HK', 'S9']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('D7') # Zweiten Trumpf von unten, gegen ungleiche Verteilung

def case24_medium(raw_state):
    print("Gegenspieler: Lusche auf Ass in langer Farbe")
    # https://www.youtube.com/live/Y00gGYC7lxk?si=LrYn_A6CAQEpeGD2&t=955
    raw_state['self'] = 2
    raw_state['points'] = [0, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DA', 'D8', 'D7', 'CT', 'CK', 'SK', 'SQ', 'S8', 'S7', 'H9']
    raw_state['trace'] = [(1, 'SA')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S8', 'S7') # Lusche schmeißen, da Alleinspieler Farbe vermutlich nicht hat

def case25_medium(raw_state):
    print("Gegenspieler: Trumpf Ass schmieren")
    # https://www.youtube.com/live/Y00gGYC7lxk?si=LrYn_A6CAQEpeGD2&t=960
    raw_state['self'] = 2
    raw_state['points'] = [14, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DA', 'D8', 'D7', 'CT', 'CK', 'SK', 'SQ', 'S7', 'H9']
    raw_state['trace'] = [(1, 'SA'), (2, 'S8'), (0, 'DQ'),
                          (0, 'SJ'), (1, 'CJ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DA') # Ass schmieren, da sonst vermutlich weg

def case26_medium(raw_state):
    print("Gegenspieler: Korrekt weiterspielen")
    # https://youtu.be/r4_dH-1v-fY?si=nZvjeZc0RzmmTPrr&t=550
    raw_state['self'] = 1
    raw_state['points'] = [25, 36]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['D9', 'C8', 'CA', 'S8', 'SK']
    raw_state['trace'] = [(2, 'HA'), (0, 'H8'), (1, 'HK'),
                          (2, 'H9'), (0, 'HT'), (1, 'H7'),
                          (0, 'DJ'), (1, 'HJ'), (2, 'DK'),
                          (1, 'C7'), (2, 'CK'), (0, 'DA'),
                          (0, 'D8'), (1, 'DT'), (2, 'DQ')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('C8')

def case27_medium(raw_state):
    print("Alleinspieler: Mit Ass mitnehmen")
    # https://www.youtube.com/watch?v=IWzVGxln9Gk
    raw_state['self'] = 0
    raw_state['points'] = [3, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DJ', 'DK', 'D9', 'D8', 'HA', 'H8', 'CA', 'CK', 'C7']
    raw_state['trace'] = [(2, 'H7')]
    raw_state['skat'] = ['HQ', 'S8']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('HA')

def case28_medium(raw_state):
    print("Alleinspieler: Mit 10 drüber gehen in Mittelhand")
    # https://www.youtube.com/watch?v=hM46xJppJ1M
    raw_state['self'] = 0
    raw_state['points'] = [7, 0]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['SJ', 'DJ', 'DA', 'DK', 'D9', 'D8', 'D7', 'CT', 'CQ', 'C9']
    raw_state['trace'] = [(2, 'CK')]
    raw_state['skat'] = ['HK', 'SQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('CT') # Kriegt man so eventuell durch. Wird ansonsten bestimmt gestochen

def case29_medium(raw_state):
    print("Alleinspieler: Mit vollem Trumpf mitnehmen")
    # https://www.youtube.com/watch?v=i-wmCji271A
    raw_state['self'] = 0
    raw_state['points'] = [13, 21]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DJ', 'DA', 'DT', 'D9', 'D8', 'SA', 'SK', 'S9']
    raw_state['trace'] = [(0, 'HJ'), (1, 'SQ'), (2, 'SJ'),
                          (2, 'CQ'), (0, 'C7'), (1, 'CA'),
                          (1, 'CK'), (2, 'C8')]
    raw_state['skat'] = ['CT', 'HQ']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('DA', 'DT')

def case30_medium(raw_state):
    print("Alleinspieler: Achttrümpfer nicht verlieren")
    # https://www.youtube.com/watch?v=tLFYl08ufec
    raw_state['self'] = 0
    raw_state['points'] = [7, 11]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['HJ', 'DA', 'DT', 'DK', 'DQ', 'D9', 'D8', 'D7', 'HQ']
    raw_state['trace'] = [(1, 'H7'), (2, 'HA'), (0, 'H8'),
                          (2, 'C9')]
    raw_state['skat'] = ['SQ', 'HK']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('D7', 'D8', 'D9', 'DQ') # Herz Dame Abwurf verliert das Spiel eventuell!

def case1_hard(raw_state):
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

def case2_hard(raw_state):
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

def case3_hard(raw_state):
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

def case4_hard(raw_state):
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

def case5_hard(raw_state):
    print("GameDuell Skat Masters: Abwerfen statt stechen")
    # https://youtu.be/TXCF53VsLdM?feature=shared&t=1095
    raw_state['self'] = 0
    raw_state['points'] = [14, 28]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'DJ', 'DA', 'DK', 'D7', 'CA', 'CK']
    raw_state['trace'] = [(2, 'HA'), (0, 'H9'), (1, 'HK'),
                          (2, 'HT'), (0, 'HQ'), (1, 'H7'),
                          (2, 'H8')]
    raw_state['skat'] = ['ST', 'SK']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('CK') # [?] Laut Kommentator ist abwerfen besser als stechen

def case6_hard(raw_state):
    print("Zehn abwerfen")
    # https://youtu.be/Szf4DtWNgZ8?si=eDtBhDkaIVl7PP8Y&t=1177
    raw_state['self'] = 2
    raw_state['points'] = [50, 36]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['DK', 'ST', 'HT']
    raw_state['trace'] = [(1, 'H7'), (2, 'H8'), (0, 'DT'),
                          (0, 'CJ'), (1, 'SJ'), (2, 'D7'),
                          (0, 'D8'), (1, 'HA'), (2, 'DA'),
                          (2, 'HJ'), (0, 'D9'), (1, 'SK'),
                          (2, 'DQ'), (0, 'DJ'), (1, 'C8'),
                          (0, 'CA'), (1, 'H9'), (2, 'CQ'),
                          (0, 'CT'), (1, 'SQ'), (2, 'CK'),
                          (0, 'C9'), (1, 'S8')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('ST') # Kommt dann mit den anderen beiden Stichen genau auf 60 Augen

def case7_hard(raw_state):
    print("Abwerfen trotz 2 Voller")
    # https://www.youtube.com/watch?v=X5yenRmK1iw
    raw_state['self'] = 0
    raw_state['points'] = [20, 25]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'SJ', 'HJ', 'DT', 'DQ', 'D9', 'D8', 'H9']
    raw_state['trace'] = [(2, 'SK'), (0, 'SQ'), (1, 'SA'),
                          (1, 'C7'), (2,  'CK'), (0, 'CQ'),
                          (1, 'CA')]
    raw_state['skat'] = ['ST', 'CT']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('H9') # Gegner kommen so nur auf genau 58 Augen. Trumpf wird entweder überstochen oder man verschwendet einen Buben

def case8_hard(raw_state):
    print("Gegenspieler: Ass aufsparen, nicht schmieren")
    # https://youtu.be/r4_dH-1v-fY?si=uG1ao3Q4YvwhxWGy&t=609
    raw_state['self'] = 1
    raw_state['points'] = [37, 38]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CA', 'S8', 'SK']
    raw_state['trace'] = [(2, 'HA'), (0, 'H8'), (1, 'HK'),
                          (2, 'H9'), (0, 'HT'), (1, 'H7'),
                          (0, 'DJ'), (1, 'HJ'), (2, 'DK'),
                          (1, 'C7'), (2, 'CK'), (0, 'DA'),
                          (0, 'D8'), (1, 'DT'), (2, 'DQ'),
                          (1, 'C8'), (2, 'CT'), (0, 'SJ'),
                          (1, 'D7'), (2, 'D9'), (0, 'CJ'),
                          (2, 'HQ'), (0, 'S9')]
    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S8')

def case9_hard(raw_state):
    print("Alleinspieler: Stich herschenken für Sieg")
    # https://www.youtube.com/watch?v=_HVMkGlokTM
    raw_state['self'] = 0
    raw_state['points'] = [42, 45]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CJ', 'HJ', 'D8', 'SK', 'S7']
    raw_state['trace'] = [(0, 'D7'), (1, 'DT'), (2, 'D9'),
                          (1, 'C9'), (2, 'CA'), (0, 'CQ'),
                          (2, 'H9'), (0, 'DA'), (1, 'HQ'),
                          (2, 'S9'), (0, 'ST'), (1, 'SA'),
                          (1, 'H8'), (2, 'DK'), (0, 'HT')]
    raw_state['skat'] = ['CT', 'HK']
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('S7')

def case10_hard(raw_state):
    print("Gegenspieler: Endspiel korrekte Karten behalten")
    # https://www.youtube.com/watch?v=wI9nIiex_RU
    raw_state['self'] = 1
    raw_state['points'] = [43, 36]
    raw_state['blind_hand'] = False
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]

    raw_state['current_hand'] = ['CK', 'C7', 'S9']
    raw_state['trace'] = [(1, 'S7'), (2, 'SK'), (0, 'SA'),
                          (0, 'D9'), (1, 'D8'), (2, 'DA'),
                          (2, 'H8'), (0, 'HA'), (1, 'H9'),
                          (0, 'DJ'), (1, 'SJ'), (2, 'D7'),
                          (1, 'HQ'), (2, 'HK'), (0, 'DT'),
                          (0, 'DQ'), (1, 'ST'), (2, 'HJ'),
                          (2, 'CJ'), (0, 'DK'), (1, 'SQ'),
                          (2, 'HT'), (0, 'C9')]

    raw_state['skat'] = []
    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick
    return raw_state, ('C7') # Damit man die 2 Farben fürs Endspiel hat (Nächster Zug mit König an Stich, dann mit Karo höchste Karte haben)
