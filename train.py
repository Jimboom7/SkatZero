import os

from skatzero.dmc.arguments import parser
from skatzero.dmc.dmc import train

if __name__ == '__main__':
    flags = parser.parse_args()
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = flags.gpu_devices

    # Fast access default values
    flags.num_actors = 16
    flags.load_model = True
    flags.xpid = "skat_12_fixed_card_distribution"
    flags.num_threads = 2
    flags.actor_device_cpu = True

    train(flags)
