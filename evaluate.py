import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/"
    MODEL = "skat_2_mod3_history"
    FRAMES = "200016000"

    NUM_WORKERS = 6
    NUM_GAMES = 10000

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

    save_evaluation_duel(CHECKPOINT_DIR, MODEL, FRAMES, NUM_WORKERS, NUM_GAMES)
