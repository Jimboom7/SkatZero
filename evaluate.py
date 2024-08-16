import os

from skatzero.evaluation.simulation import save_evaluation_duel

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    NUM_GAMES = 10000
    GAMETYPE = 'G'
    MODEL1 = "10800"
    MODEL2 = "10460"
    NUM_ACTORS = 4
    FOLDER = "skat_lstm_" + GAMETYPE
    FOLDER2 = "skat_lstm_" + GAMETYPE
    SEED = 42

    save_evaluation_duel(FOLDER, FOLDER2, MODEL1, MODEL2, NUM_GAMES, NUM_ACTORS, GAMETYPE, SEED)

    # for i in range(11790, int(MODEL1) + 10, 10):
    #     save_evaluation_duel(FOLDER, FOLDER2, i, MODEL2, NUM_GAMES, BLIND_HAND_CHANCE, NUM_ACTORS, GAMETYPE, SEED)

    # for model1 in [12410, 12400]:
    #     i = 1
    #     score1 = 0
    #     score2 = 0
    #     for model2 in [9500]:
    #         res1, res2 = save_evaluation_duel(FOLDER, FOLDER2, model1, model2, NUM_GAMES, BLIND_HAND_CHANCE, NUM_ACTORS, GAMETYPE, SEED * i)
    #         score1 += res1
    #         score2 += res2
    #         i += 100000
    #     for model2 in [9000, 10000, 11000, 11500, 12000]:
    #         res1, res2 = save_evaluation_duel(FOLDER, FOLDER, model1, model2, NUM_GAMES, BLIND_HAND_CHANCE, NUM_ACTORS, GAMETYPE, SEED * i)
    #         score1 += res1
    #         score2 += res2
    #         i += 100000
    #     print("Overall: " + str(score1 - score2))
    #     with open("testresults/evaluate_log2.txt", "a", encoding='utf-8') as logfile:
    #         logfile.write(str(model1) + "x overall: " + str(round(score1 - score2, 2)) + "\n")
    #         logfile.write(str(model1) + "x solo: " + str(round(score1, 2)) + "\n")
    #         logfile.write(str(model1) + "x oppo: " + str(round(score2, 2)) + "\n")
