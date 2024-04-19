import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append('D:\Git\skatzero')
from skatzero.game.utils import calculate_max_bids

values = np.load('values.npy')

dists = np.load('outcome_distributions.npy')

test = calculate_max_bids(['CA', 'H7', 'S9', 'HA'], 'G')

print('Ende')