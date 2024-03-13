from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import get_bidding_data

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/skat_17_new_baseline"
    FRAMES = "70"

    MODEL = CHECKPOINT_DIR + "/0_" + FRAMES + ".pth"

    info = get_bidding_data(MODEL, True)

    sorted_info = dict(sorted(info.items(), key=lambda item: item[1], reverse=True))

    for action, value in sorted_info.items():
        print(format_card(action) + ": " + str(value))
