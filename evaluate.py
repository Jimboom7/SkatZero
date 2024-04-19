import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    NUM_GAMES = 10000
    GAMETYPE = 'G'
    MODEL1 = "1200"
    MODEL2 = "1000"
    BLIND_HAND_CHANCE = 0.1
    NUM_ACTORS = 6
    FOLDER = "skat_" + GAMETYPE
    SEED = 42

    save_evaluation_duel(FOLDER, MODEL1, MODEL2, NUM_GAMES, BLIND_HAND_CHANCE, NUM_ACTORS, GAMETYPE, SEED)
