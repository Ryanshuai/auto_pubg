from collections import OrderedDict
import torch.nn as nn
import torch


import time

def one_card_model(state_dict):
    # create new OrderedDict that does not contain `module.`
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        if k.startswith('module.'):
            new_state_dict[k[7:]] = v
        else:
            new_state_dict[k] = v


    return new_state_dict


def fill_dict(notrain_dict, pretrain_dict):
    for key in notrain_dict:
        if key in pretrain_dict.keys():
            notrain_dict[key] = pretrain_dict[key]

    return notrain_dict


def load_pretrain(net: nn.Module, pre_train_model_path):
    pretrained_dict = torch.load(pre_train_model_path, map_location=lambda storage, loc: storage)
    if 'state_dict' in pretrained_dict:
        pretrained_dict = pretrained_dict['state_dict']
    pretrained_dict = one_card_model(pretrained_dict)

    notrain_dict = net.state_dict()
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in notrain_dict}

    notrain_dict.update(pretrained_dict)
    net.load_state_dict(notrain_dict)
    return net


if __name__ == '__main__':
    from net.cpsn_370k.cascaded_pyramid_shuffle_net import CPN

    net = CPN(10)
    pre_train_model = '/home/ys/Data/pose_estimate_save/ys/ys-full_net_expend-2018_09_07_14_58_34/models/snapshot_epoch1_batch13000_model'

    load_pretrain(net, pre_train_model)
