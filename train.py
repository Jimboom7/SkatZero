import os

from skatzero.env.skat import SkatEnv
from skatzero.dmc.trainer import DMCTrainer
from skatzero.env.supervised import SupervisedEnv

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    GAMETYPE = 'G' # 'G' or 'D' or 'N'

    env = SkatEnv(gametype=GAMETYPE)

    trainer = DMCTrainer(
        env,
        cuda="0", # Empty = everything on cpu, 0 = GPU enabled
        xpid='skat_lstm_' +  GAMETYPE,
        savedir='models/checkpoints',
        save_interval=10, # in million frames
        num_actors=16, # should be equal to number of physical cores, +- some
        training_device="0", # 0 for GPU, needs cuda set to 1 to work
        load_model=True,
        num_threads=2,
        actor_device='cpu',
        total_frames=20000000000
    )

    trainer.start()

    # env = SupervisedEnv(gametype=GAMETYPE)

    # trainer = DMCTrainer(
    #     env,
    #     cuda="0", # Empty = everything on cpu, 0 = GPU enabled
    #     xpid='skat_supervised_' +  GAMETYPE,
    #     savedir='models/checkpoints',
    #     save_interval=10, # in million frames
    #     num_actors=1, # should be equal to number of physical cores, +- some
    #     training_device="0", # 0 for GPU, needs cuda set to 1 to work
    #     load_model=False,
    #     num_threads=4,
    #     actor_device='cpu',
    #     total_frames=20000000000
    # )

    # trainer.start()
