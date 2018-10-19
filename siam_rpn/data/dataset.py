import os
import cv2
import numpy as np
import fileinput
import torch
from torchvision import transforms
from torch.utils.data import Dataset

from model.train_pre_process import Train_Pre, draw_anchors_with_annotation, draw_anchors
from data.xml_2_dict import xml_2_xywh
from data.data_utils import *
from config.siam_rpn.default_ys2_ubuntu import ARG


class VID_Tracking_Dataset(Dataset):
    def __init__(self, arg: ARG):
        super().__init__()
        self.arg = arg
        self.pre = Train_Pre(arg)
        self.z_size = arg.model.z_size
        self.u_size = arg.model.u_size
        self.root_path = arg.data.dataset.train.root_path
        self.data_path = arg.data.dataset.train.data_path
        self.anno_path = arg.data.dataset.train.annotation_path
        self.data_path_list = []
        self.anno_path_list = []
        self.fold_len_list = []
        for line in fileinput.input('../data/relative_paths.txt'):
            data_path, anno_path = line.split()
            self.data_path_list.append(os.path.join(self.root_path, data_path))
            self.anno_path_list.append(os.path.join(self.root_path, anno_path))

    def __len__(self):
        return len(self.data_path_list)

    def __getitem__(self, idx):
        # try:
        data_fold_path = self.data_path_list[idx]
        anno_fold_path = self.anno_path_list[idx]

        # get z u image
        z_num, u_num = random_z_u_in_100(anno_fold_path)
        z_im_path = os.path.join(data_fold_path, z_num+'.JPEG')
        u_im_path = os.path.join(data_fold_path, u_num+'.JPEG')
        z_im_origin = cv2.imread(z_im_path)
        u_im_origin = cv2.imread(u_im_path)

        # get z u position and size
        z_anno_path = os.path.join(anno_fold_path, z_num+'.xml')
        u_anno_path = os.path.join(anno_fold_path, u_num+'.xml')
        zx, zy, zw, zh = xml_2_xywh(z_anno_path)
        ux, uy, uw, uh = xml_2_xywh(u_anno_path)

        # print('x', u_im_path, u_anno_path)
        # print('z', z_im_path, z_anno_path)
        # show_rect('z_im_origin', z_im_origin, x=zx, y=zy, w=zw, h=zh)
        # show_rect('u_im_origin', u_im_origin, x=ux, y=uy, w=uw, h=uh)

        z_center_pos, z_size = rect_to_cxy_wh((zx, zy, zw, zh))
        u_center_pos, u_size = rect_to_cxy_wh((ux, uy, uw, uh))

        z = self.pre.get_z_from_im(z_im_origin, z_center_pos, z_size)
        u = self.pre.get_u_from_im(u_im_origin, u_center_pos, u_size)

        cls_target, cls_mask, reg_target, reg_mask, p_idx, n_idx = self.pre.return_ct_cm_rt_rm()

        # # # # # # # for test data set
        # rect_im = draw_anchors(u, self.pre)
        # cv2.imshow('z_im', z)
        # cv2.waitKey(0)
        # rect_im = draw_anchors_with_annotation(u, self.pre)
        # cv2.imshow('rect_u_im', rect_im)
        # cv2.waitKey(0)

        z = transforms.ToTensor()(z)
        u = transforms.ToTensor()(u)

        c_target = torch.from_numpy(cls_target)
        c_mask = torch.from_numpy(cls_mask)
        r_target = torch.from_numpy(reg_target)
        r_mask = torch.from_numpy(reg_mask)
        p_idx = torch.from_numpy(p_idx)
        n_idx = torch.from_numpy(n_idx)

        return z, u, c_target, c_mask, r_target, r_mask
        # except Exception as e:
        #     print('exception at dataloader: ', self.data_path_list[idx])
        #     print(e)
        #     return self.__getitem__(random.randrange(0, len(self.data_path_list) - 1))


def random_z_u_in_100(fold):
    num_list = []
    for itm in os.listdir(fold):
        num = int(itm[0:-4])
        num_list.append(num)
    num_list.sort()

    z_i = np.random.randint(0, len(num_list))
    z_pos = num_list[z_i]

    x_min = max(z_pos-50, 0)
    x_max = min(z_pos+50, num_list[-1])

    x_list = []
    for i in range(x_min, x_max+1):
        if i in num_list:
            x_list.append(i)

    x_i = np.random.randint(0, len(x_list))
    x_pos = num_list[x_i]

    z_num = str(z_pos).zfill(6)
    x_num = str(x_pos).zfill(6)
    return z_num, x_num


if __name__ == '__main__':
    from config.siam_rpn.default_ys2_ubuntu import ARG as win_ARG
    arg = win_ARG()
    dataset = VID_Tracking_Dataset(arg)
    for i in range(len(dataset)):
        print("#################################################")
        dataset.__getitem__(i)

