import os
import time
import numpy as np
import subprocess

import torch
from torch import nn
from visdom import Visdom
import torchvision.utils as vutils
from tensorboardX import SummaryWriter


class Vis:
    """Vis class .

        a visualization tool for training/valid/test deep learning model.

    line:
        draw lines used in loss, accuracy etc.
    img:
        show img
    weight:
        show weights of a model.
    gradient:
        show gradient of all parameter of a model.
    model:
        show structure of a model.
    """
    def __init__(self, arg):
        self.use_visdom = False
        if arg.visdom.enable:
            self.use_visdom = True
            self.vis = Visdom(env=arg.stamp.experiment_name, server=arg.visdom.server, port=arg.visdom.port)
            self.wins = []

        self.use_tensor_board = False
        if arg.tensorboard.enable:
            self.use_tensor_board = True
            self.tb_writer = SummaryWriter(arg.save.tensorboard)

            cmd = os.environ['HOME'] + "'/anaconda3/bin/'tensorboard --logdir=" + arg.save.tensorboard
            self.tb_log_out_process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

    def __del__(self):
        if self.use_tensor_board:
            self.tb_log_out_process.kill()

    def line(self, win, name, x, y: float):
        if self.use_tensor_board:
            self.tb_writer.add_scalar(win+'/'+name, y, x)
        if self.use_visdom:
            if win not in self.wins:
                new_win = self.vis.line(win=win, name=name,
                                        X=np.array([x]), Y=np.array([y]),
                                        update=None, opts=dict(showlegend=True))
                self.wins.append(new_win)
            else:
                self.vis.line(win=win, name=name,
                              X=np.array([x]), Y=np.array([y]),
                              update='append', opts=dict(showlegend=True))

    def img(self, win, name, image, x=None, normalize=False, scale_each=False):
        if self.use_tensor_board:
            if isinstance(image, np.ndarray):
                image = torch.from_numpy(image)
            if image.dim() == 4:
                image = vutils.make_grid(image, normalize=normalize, scale_each=scale_each)
            if image.shape[-1] == 3:
                if image.dim() == 4:
                    image = image.permute(0, 3, 1, 2)
                elif image.dim() == 3:
                    image = image.permute(2, 0, 1)
            self.tb_writer.add_image(win + '/' + name, image, global_step=x)

    def weight(self, model, x):
        for k, v in model.state_dict().items():
            self.tb_writer.add_histogram('weight' + '/' + k, v, global_step=x)
            if v.grad is not None:
                print(v)

    def gradient(self, model, x):
        for m in model.named_modules():
            k, v = m[0], m[1]
            if isinstance(v, nn.Conv2d):
                w_grad = v.weight.grad
                self.tb_writer.add_histogram('gradient' + '/' + k + '_w_grad', w_grad, global_step=x)
                if v.bias is not None:
                    b_grad = v.bias.grad
                    self.tb_writer.add_histogram('gradient' + '/' + k + '_b_grad', b_grad, global_step=x)
            elif isinstance(v, nn.BatchNorm2d):
                pass
            elif isinstance(v, nn.Linear):
                w_grad = v.weight.grad
                self.tb_writer.add_histogram('gradient' + '/' + k + '_w_grad', w_grad, global_step=x)
                if v.bias is not None:
                    b_grad = v.bias.grad
                    self.tb_writer.add_histogram('gradient' + '/' + k + '_b_grad', b_grad, global_step=x)

    def model(self, model, input_to_model):
        self.tb_writer.add_graph(model, input_to_model=input_to_model)


if __name__ == '__main__':
    from config.siam_rpn.default_ys2_ubuntu import ARG
    arg = ARG()

    myvis = Vis(arg)
    for i in range(1, 10):
        # myvis.text('links', 'sdfasdfasdddddddddddddddddd')
        myvis.line('loss', 'train', i, -9 * i)
        myvis.line('loss', 'tst', i, 3 * i)
        time.sleep(1)
        print(i)
