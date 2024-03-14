import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    NUM_GAMES = 10000
    MODEL = "skat_21_bids"
    FRAMES = "30"
    BLIND_HAND_CHANCE = 0.1
    NUM_ACTORS = 12

    save_evaluation_duel(MODEL, FRAMES, NUM_GAMES, BLIND_HAND_CHANCE, NUM_ACTORS)
