import numpy as np
import torch
import torch.backends.cudnn as cudnn


def run_train_pre_settings(random_seed: int):
    cudnn.benchmark = True
    torch.manual_seed(random_seed)
    np.random.seed(random_seed)


def get_available_device_object():
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
