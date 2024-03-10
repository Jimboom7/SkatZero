import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/"
    MODEL = "skat_6_noblack_smooth_reward"
    FRAMES = "30009600"
    HAND_QUALITY = "medium"
    BLIND_HAND_CHANCE = "0"

    NUM_WORKERS = 10
    NUM_GAMES = 10000

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

    save_evaluation_duel(CHECKPOINT_DIR, MODEL, FRAMES, NUM_WORKERS, NUM_GAMES, HAND_QUALITY, BLIND_HAND_CHANCE)
