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
        save_interval=10, # save model every 10 minutes
        num_actors=12, # when training on gpu and actors on cpu: should be equal to number of cores
        training_device="0", # 0 for GPU, needs cuda set to 1 to work
        load_model=True,
        eval=True,
        actor_device='cpu',
        total_frames=10000000 # 1 million takes around 3 minutes
    )

    # Train DMC Agents
    trainer.start()

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    train()
