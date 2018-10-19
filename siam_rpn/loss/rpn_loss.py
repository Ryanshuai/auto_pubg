import torch
from torch import nn


class RPN_Loss(nn.Module):
    def __init__(self):
        super().__init__()
        self.classify_loss = nn.CrossEntropyLoss(reduce=False)
        self.regression_loss = nn.SmoothL1Loss(reduce=False)

    def forward(self, cls_predict, cls_target, cls_mask, reg_predict, reg_target, reg_mask):
        # assert type(cls_target) == type(cls_predict) == type(reg_target) == type(reg_predict)
        # assert cls_target.shape[-3] == cls_target.shape[-3] == cls_target.shape[-3] == cls_target.shape[-3] \
        #        == cls_target.shape[-3] == self.f_h
        # assert cls_target.shape[-2] == cls_target.shape[-2] == cls_target.shape[-2] == cls_target.shape[-2] \
        #        == cls_target.shape[-2] == self.f_h
        # assert cls_target.shape[-1] == cls_target.shape[-1] == cls_target.shape[-1] == cls_target.shape[-1] \
        #        == cls_target.shape[-1] == self.a_n

        c_loss = self.classify_loss(cls_predict, cls_target)  # shape(1445,)
        c_loss_mask_mean = torch.mean((c_loss*cls_mask.type(torch.cuda.FloatTensor)))

        r_loss = self.regression_loss(reg_predict, reg_target)  # shape(1445, 4)
        r_loss_ = torch.mean(r_loss, dim=1)  # shape(1445,)
        r_loss_mask_mean = torch.mean((r_loss_*reg_mask.type(torch.cuda.FloatTensor)))

        loss = torch.add(c_loss_mask_mean, r_loss_mask_mean)

        return loss, c_loss_mask_mean, r_loss_mask_mean

