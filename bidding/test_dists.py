import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append('D:\Git\skatzero')
from skatzero.game.utils import calculate_max_bids

values = np.load('data/values_G.npy')

dists = np.load('data/outcome_distributions_G.npy')

plt.figure()
plt.plot(values, np.mean(dists, axis=1)[:,0])
plt.plot(values, np.mean(dists, axis=1)[:,1])
plt.plot(values, np.mean(dists, axis=1)[:,2])
plt.plot(values, np.mean(dists, axis=1)[:,3])
plt.plot(values, np.mean(dists, axis=1)[:,4])
plt.plot(values, np.mean(dists, axis=1)[:,5])
plt.show()

possible_rewards = np.zeros((1, 1, 6))
#possible_rewards[0,0,:] = [-170, -150, -130, 70, 80, 90]    # Farbspiel!
possible_rewards[0,0,:] = [-282, -234, -186, 98, 122, 146]   # Grand!

true_vals_without_smooth_points = np.sum(np.mean(dists * possible_rewards, axis=1), axis=1)
plt.figure()
plt.plot(values, true_vals_without_smooth_points)
plt.plot([values[0], values[-1]], [values[0], values[-1]])
plt.xlabel('Value-Schätzung vom Modell')
plt.ylabel('Tatsächlicher Value (ohne Smooth Points)')
plt.show()


test = calculate_max_bids(['CA', 'H7', 'S9', 'HA'], 'G')

print('Ende')