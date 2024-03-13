import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    NUM_GAMES = 10000
    MODEL = "skat_17_new_baseline"
    FRAMES = "10"
    NUM_ACTORS = 10

    save_evaluation_duel(MODEL, FRAMES, NUM_GAMES, NUM_ACTORS)
