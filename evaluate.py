import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/"
    MODEL = "skat_6_new_baseline"
    FRAMES = ["50016000"]
    HAND_QUALITY = ["bad", "medium", "good"]
    BLIND_HAND_CHANCE = "0"

    NUM_WORKERS = 6
    NUM_GAMES = 10000

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

    for frames in FRAMES:
        for qual in HAND_QUALITY:
            save_evaluation_duel(CHECKPOINT_DIR, MODEL, frames, NUM_WORKERS, NUM_GAMES, qual, BLIND_HAND_CHANCE)
