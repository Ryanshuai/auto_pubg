import cv2
import numpy as np
import torch
from torch import tensor
from torch.nn import functional as F

from model.net import SiamRPN
from model.test_pre_process import Test_Pre
from data.data_utils import *

class Tracker:
    def __init__(self, arg, first_im, target_center_pos, target_size, net: SiamRPN):
        self.device = arg.device
        self.u_size = arg.model.u_size
        self.z_size = arg.model.z_size
        self.res_size = arg.model.res_size
        self.stride = arg.tracker.total_stride
        self.penalty_size = 0.055
        self.cos_win_rate = 0.42
        self.lr = 0.295

        self.t_c_pos = target_center_pos
        self.t_size = target_size
        self.im_h = first_im.shape[0]
        self.im_w = first_im.shape[0]
        self.pre = Test_Pre(arg)

        # if ((target_size[0] * target_size[1]) / float(self.im_h * self.im_w)) < 0.004:
        #     self.u_size = 287  # small object big search region
        # else:
        #     self.u_size = 271

        # self.res_size = (self.u_size - self.z_size) // self.stride + 1

        cos_win = np.outer(np.hanning(self.res_size), np.hanning(self.res_size))
        self.cos_win = np.tile(cos_win.flatten(), self.pre.anchor_num)

        self.net = net.to(self.device).eval()
        self.warm_up(self.net)

        model_z = self.pre.get_z_from_im(first_im, target_center_pos, target_size)

        # print(model_z.shape)
        # cv2.imshow('z_crop', model_z)
        # cv2.waitKey()

        z = np_to_tensor(model_z, self.device)

        self.net.template(z)

    def warm_up(self, net):
        for i in range(10):
            net.template(torch.FloatTensor(1, 3, 127, 127).to(self.device))
            net(torch.FloatTensor(1, 3, 255, 255).to(self.device))

    def track(self, u_im: np.ndarray):
        self.u_im = u_im
        model_u = self.pre.get_u_from_im(u_im, self.t_c_pos, self.t_size)
        self.model_u = model_u

        print(model_u.shape)
        cv2.imshow('u_train', model_u)
        cv2.waitKey()

        u = np_to_tensor(model_u, self.device)
        cls_predict, reg_predict = self.net(u)

        # # # # # # # # for test
        # cls_predict_soft = F.softmax(cls_predict[0].view(2, -1), dim=0)
        # cls_predict_show = cls_predict_soft.view(10, 17, 17).cpu().data.numpy()
        # for i in range(10):
        #     cls_show = (cls_predict_show[i] * 255).astype(np.uint8)
        #     cv2.imshow('cls_show'+str(i), cls_show)
        #     cv2.waitKey(0)

        self.post_process(cls_predict, reg_predict, self.pre.scale_z)

        return self.t_c_pos, self.t_size

    def post_process(self, cls_predict: tensor, reg_predict: tensor, scale_z):
        scores = F.softmax(cls_predict[0].view(2, -1), dim=0).data[1, :].cpu().numpy()

        # # # # # # # # # for test
        # cls_predict_soft = F.softmax(cls_predict[0].view(2, -1), dim=0).data[1, :]
        # cls_predict_show = cls_predict_soft.view(5, 17, 17).cpu().data.numpy()
        # for i in range(5):
        #     cls_show = (cls_predict_show[i] * 255).astype(np.uint8)
        #     cv2.imshow('cls_show'+str(i), cls_show)
        #     cv2.waitKey(0)

        regress = reg_predict[0].view(4, -1).data.cpu().numpy()

        deltas = regress_2_cord(regress, self.pre.anchors)

        # draw_anchors_with_predict(self.u_im, self.t_c_pos, self.pre.scale_z, self.pre.anchors, scores, regress)

        def change(r):
            return np.maximum(r, 1./r)

        def sz(w, h):
            pad = (w + h) * 0.5
            sz2 = (w + pad) * (h + pad)
            return np.sqrt(sz2)

        def sz_wh(wh):
            pad = (wh[0] + wh[1]) * 0.5
            sz2 = (wh[0] + pad) * (wh[1] + pad)
            return np.sqrt(sz2)

        # size penalty
        s_c = change(sz(deltas[2, :], deltas[3, :]) / (sz_wh(self.t_size * scale_z)))  # scale penalty
        r_c = change((self.t_size[0] / self.t_size[1]) / (deltas[2, :] / deltas[3, :]))  # ratio penalty

        penalty = np.exp(-(r_c * s_c - 1.) * self.penalty_size)
        pscore = penalty * scores

        # window float
        pscore = pscore * (1 - self.cos_win_rate) + self.cos_win * self.cos_win_rate
        best_pscore_id = np.argmax(pscore)

        target = deltas[:, best_pscore_id] / scale_z
        target_sz = self.t_size
        self.lr = penalty[best_pscore_id] * scores[best_pscore_id] * self.lr

        res_x = target[0] + self.t_c_pos[0]
        res_y = target[1] + self.t_c_pos[1]

        res_w = target_sz[0] * (1 - self.lr) + target[2] * self.lr
        res_h = target_sz[1] * (1 - self.lr) + target[3] * self.lr

        self.t_c_pos = np.array([res_x, res_y])
        self.t_size = np.array([res_w, res_h])

        # self.t_c_pos[0] = max(0, min(self.im_w, self.t_c_pos[0]))
        # self.t_c_pos[1] = max(0, min(self.im_h, self.t_c_pos[1]))
        # self.t_size[0] = max(10, min(self.im_w, self.t_size[0]))
        # self.t_size[1] = max(10, min(self.im_h, self.t_size[1]))


# for test
def draw_anchors_with_predict(im, center_xy, scale_z, anchors, scores, regresses):
    for i, score in enumerate(scores):
        if score > 0.7:
            anchor = anchors[i]
            a_x, a_y, a_w, a_h = anchor
            a_w /= scale_z
            a_h /= scale_z
            a_x += center_xy[0]
            a_y += center_xy[1]
            a_x, a_y, a_w, a_h = int(a_x), int(a_y), int(a_w), int(a_h)
            im = cv2.rectangle(im, (a_x - a_w//2, a_y - a_h//2), (a_x + a_w//2, a_y + a_h//2), color=(0, 255, 0))

            regress = regresses[:, i]
            r_x, r_y, r_w, r_h = regress_2_cord(regress, anchor)
            r_x /= scale_z
            r_y /= scale_z
            r_w /= scale_z
            r_h /= scale_z
            r_x += center_xy[0]
            r_y += center_xy[1]
            r_x, r_y, r_w, r_h = int(r_x), int(r_y), int(r_w), int(r_h)
            im = cv2.rectangle(im, (r_x - r_w//2, r_y - r_h//2), (r_x + r_w//2, r_y + r_h//2), color=(255, 255, 0))

            # cv2.imshow('im with predict', im)
            # cv2.waitKey()

    # cv2.imshow('im with predict', im)
    # cv2.waitKey()


