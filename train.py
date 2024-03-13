import os

from skatzero.env.skat import SkatEnv
from skatzero.dmc.trainer import DMCTrainer

if __name__ == '__main__':
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    env = SkatEnv()

    trainer = DMCTrainer(
        env,
        cuda="0", # Empty = everything on cpu, 0 = GPU enabled
        xpid='skat_17_new_baseline',
        savedir='checkpoints',
        save_interval=10, # in million frames
        num_actors=16, # should be equal to number of physical cores, +- some
        training_device="0", # 0 for GPU, needs cuda set to 1 to work
        load_model=True,
        num_threads=2,
        eval=True,
        actor_device='cpu',
        total_frames=200000000 # 1 million takes around 3 minutes
    )

    trainer.start()
