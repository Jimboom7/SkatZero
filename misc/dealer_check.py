import os
import numpy as np
from skatzero.game.dealer import Dealer
from skatzero.game.player import Player
from skatzero.game.utils import evaluate_hand_strength

d = Dealer(np.random.RandomState())
players = [{},{},{}]
players[0] = Player(0)
players[1] = Player(1)
players[2] = Player(2)

valuelist = []
count_gegenreizung = 0
for i in range (0,10000):
    d.deal_cards(players, 'G')
    # valuelist.append(d.max_bids[1])
    # valuelist.append(d.max_bids[2])
    valuelist.append(evaluate_hand_strength(players[0].current_hand, 'G')['G'])

#     print(players[0].current_hand)
#     print(players[1].current_hand)
#     print(players[2].current_hand)
#     print(d.max_bids)
#     print(d.bids)
#     print(d.bid_jacks)
#     print(d.blind_hand)
#     if d.max_bids[1] != 0 or d.max_bids[2] != 0:
#         count_gegenreizung += 1
#     print("#######")
# print(count_gegenreizung)
# print("Null Closed: " + str(d.counter1)) # 3,0% anstatt 3,2%(set valid_game to True and Gametype == N, multiply by 3)
# print("Null Hand: " + str(d.counter2)) # 0,24% Volltreffer (set valid_game to True and Gametype == N, multiply by 3)
# print("Null Ouvert: " + str(d.counter3)) # 2,9% Volltreffer (set valid_game to True and Gametype == N, multiply by 3)
# print("Null Ouvert Hand: " + str(d.counter4)) # 0,4% anstatt 0,3% (set valid_game to True and Gametype == N, multiply by 3)
# print("Null Gesamt: " + str(d.counter5)) # 6,3% anstatt 6,7% (set valid_game to True and Gametype == N, multiply by 3)
# print("Hand: " + str(d.counter6)) # D: 9,4% anstatt 14%, G: 7,3% anstatt 12% (valid_game nicht setzen, für D und G testen. Handspiele noch zu Farb/Grand dazu addieren)
# print("Farbspiel: " + str(d.counter7)) # 60% anstatt 63% (set valid_game to True, multiply by 3)
# print("Grand: " + str(d.counter8)) # 30% Volltreffer (set valid_game to True, multiply by 3)
# print("Eingepasst: " + str(d.counter9)) # 1,8% anstatt 1,9% (set valid_game to True)
# Null gereizt (von irgendwem): 13% der Spiele

# from iss.SkatMatch import SkatMatch
# from skatzero.evaluation.simulation import set_dealer_data

# valuelist = []
# for line in list(open(os.path.join(os.getenv('SKAT_PATH'), 'skatgame-games-07-2024/high_elo_D.txt'), encoding='utf-8')):
#     match = SkatMatch(line)
#     if not match.eingepasst:
#         dealer = set_dealer_data(match, 'D')
#         # valuelist.append(evaluate_null_strength(dealer.deck[:10]))
#         valuelist.append(match.maxReizungen[(match.alleinspielerInd + 1) % 3])
#         valuelist.append(match.maxReizungen[(match.alleinspielerInd + 2) % 3])

import statistics
print(statistics.mean(valuelist))
print(statistics.stdev(valuelist))

import matplotlib.pyplot as plt
import numpy as np

plt.hist(valuelist, density=True, bins=50)
plt.ylabel('Probability')
plt.xlabel('Value')
plt.show()