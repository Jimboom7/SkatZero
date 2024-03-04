import os

import rlcard
from rlcard.agents.dmc_agent import DMCTrainer

def train():
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    #os.environ["OPENBLAS_NUM_THREADS"] = "1"
    #os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    #os.environ["NUMEXPR_NUM_THREADS"] = "1"

    # Make the environment
    env = rlcard.make('skat')

    # Initialize the DMC trainer
    trainer = DMCTrainer(
        env,
        cuda="0", # Empty = everything on cpu, 0 = GPU enabled
        xpid='skat_0',
        savedir='experiments/skat',
        save_interval=10, # in million frames
        num_actors=15, # should be equal to number of physical cores, +- some
        training_device="0", # 0 for GPU, needs cuda set to 1 to work
        load_model=False,
        eval=True,
        actor_device='cpu',
        total_frames=100000000 # 1 million takes around 3 minutes
    )

    # Train DMC Agents
    trainer.start()

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    train()
