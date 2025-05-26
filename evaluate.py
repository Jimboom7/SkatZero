import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    NUM_GAMES = 10000
    GAMETYPE = 'G'
    MODEL1 = "14730"
    MODEL2 = "14630"
    NUM_ACTORS = 12
    FOLDER = "skat_lstm_" + GAMETYPE
    FOLDER2 = "skat_lstm_" + GAMETYPE
    SEED = 42

    save_evaluation_duel(FOLDER, FOLDER2, MODEL1, MODEL2, NUM_GAMES, NUM_ACTORS, GAMETYPE, SEED, dealer_from_log=True)
