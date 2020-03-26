import os

import cv2
import numpy as np
from itertools import product

from calibrate_icons.match_icon import get_icon_name
from calibrate_icons.crop_white import get_white_shield
from calibrate_icons.get_position.position_constant import crop_position


def has_sth(im):
    canny = cv2.Canny(im, 30, 100) / 255
    c_sum = np.sum(canny)
    if c_sum > 10:
        return True
    return False


def has_white(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    if np.max(r) > 220 and np.max(g) > 220 and np.max(b) > 220:
        return True
    return False


def center_shield(im):
    canny = cv2.Canny(im, 30, 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    iClose = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel).astype(np.uint8)
    iClose = (iClose / 255).astype(np.uint8)
    return np.concatenate((im * iClose[:, :, np.newaxis], iClose[:, :, np.newaxis]), axis=-1)


def get_same_part(ims):
    im0 = ims[0]
    im0_4c = np.concatenate((im0, np.ones_like(im0[:, :, [0]]) * 255), axis=-1).astype(np.uint8)
    for im in ims[1:]:
        im_diff = np.abs(im.astype(np.int) - im0.astype(np.int))
        im_same = np.where(im_diff == 0, 1, 0)
        im_same = im_same[:, :, 0] & im_same[:, :, 1] & im_same[:, :, 2]
        im0_4c *= im_same[:, :, np.newaxis].astype(np.uint8)
    return im0_4c


if __name__ == '__main__':

    save_dir = 'position_icon/'
    crop_dir = 'screens/white'
    os.makedirs(save_dir, exist_ok=True)

    # # in-tab -------------------------------------
    # for im_name in os.listdir(crop_dir):
    #     im = cv2.imread(os.path.join(crop_dir, im_name))
    #     y1, x1, y2, x2 = crop_position['in-tab']
    #     rect_im = im[y1:y2, x1:x2]
    #     if has_sth(rect_im):
    #         crop_name, shield = crop_white(rect_im)
    #         if shield is not None:
    #             pos_n = 'in-tab'
    #             os.makedirs(os.path.join(save_dir, pos_n), exist_ok=True)
    #             cv2.imwrite(os.path.join(save_dir, pos_n, crop_name + '.png'), shield)
    #             break
    #
    # # fire-mode -------------------------------------
    # for im_name in os.listdir(crop_dir):
    #     im = cv2.imread(os.path.join(crop_dir, im_name))
    #     y1, x1, y2, x2 = crop_position['fire-mode']
    #     rect_im = im[y1:y2, x1:x2]
    #     if has_white(rect_im):
    #         cv2.imshow('rect_im', rect_im)
    #         shield = get_white_shield(rect_im)
    #         cv2.imshow('sh', shield)
    #         cv2.waitKey()
    #         os.makedirs(os.path.join(save_dir, 'fire-mode'), exist_ok=True)
    #         cv2.imwrite(os.path.join(save_dir, 'fire-mode', im_name), shield)

    # # posture -------------------------------------
    # for im_name in os.listdir(crop_dir):
    #     im = cv2.imread(os.path.join(crop_dir, im_name))
    #     y1, x1, y2, x2 = crop_position['posture']
    #     rect_im = im[y1:y2, x1:x2]
    #     if has_white(rect_im):
    #         shield = get_white_shield(rect_im, 210)
    #         # cv2.imshow('rect_im', rect_im)
    #         # cv2.imshow('sh', shield)
    #         # cv2.waitKey()
    #         os.makedirs(os.path.join(save_dir, 'posture'), exist_ok=True)
    #         cv2.imwrite(os.path.join(save_dir, 'posture', im_name), shield)

    # gun_name -------------------------------------
    # icon_list = list()
    # for im_name in os.listdir(crop_dir):
    #     im = cv2.imread(os.path.join(crop_dir, im_name))
    #     for pos_name, pos_rect in crop_position.items():
    #         if 'white' in pos_name:
    #             y1, x1, y2, x2 = pos_rect
    #             rect_im = im[y1:y2, x1:x2]
    #             if has_sth(rect_im):
    #                 crop_name, shield = crop_white(rect_im)
    #                 if shield is not None:
    #                     pos_n = pos_name.split('_')[-1]
    #                     os.makedirs(os.path.join(save_dir, pos_n), exist_ok=True)
    #                     cv2.imwrite(os.path.join(save_dir, pos_n, crop_name + '.png'), shield)

    # # attach -------------------------------------
    # crop_dir_list = ['screens/icon1', 'screens/icon4']
    #
    # position_filtered = dict(filter(lambda x: ('icon' in x[0]), crop_position.items()))
    # for pos_name, pos_rect in position_filtered.items():
    #     y1, x1, y2, x2 = pos_rect
    #
    #     cropns = list()
    #     for crop_dir in crop_dir_list:
    #         cropis = list()
    #         for im_name in os.listdir(crop_dir):
    #             im = cv2.imread(os.path.join(crop_dir, im_name))
    #             cropis.append(im[y1:y2, x1:x2])
    #         cropns.append(cropis)
    #
    #     for crop_product in product(*cropns):
    #         crop_same = get_same_part(crop_product)
    #         if np.sum(crop_same[:, :, -1]) / 255 > 100:
    #             crop_name = get_icon_name(crop_same)
    #             os.makedirs(os.path.join(save_dir, pos_name.split('_')[-1]), exist_ok=True)
    #             cv2.imwrite(os.path.join(save_dir, pos_name.split('_')[-1], crop_name + '.png'), crop_same)
