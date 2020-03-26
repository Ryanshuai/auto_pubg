import cv2
import numpy as np

from screen_parameter import min_icon_area
from calibrate_icons.match_icon import get_icon_name


def crop_same_icon(icon1_4c, icon2_4c):
    icon1_3c = icon1_4c[:, :, 0:3]
    icon2_3c = icon2_4c[:, :, 0:3]

    icon_diff = np.abs(icon1_3c.astype(np.int) - icon2_3c.astype(np.int))
    icon_same = np.where(icon_diff == 0, 1, 0).astype(np.uint8)
    icon_same = icon_same[:, :, 0] & icon_same[:, :, 1] & icon_same[:, :, 2]

    icon_same = icon_same[:, :, np.newaxis]
    icon_3c = icon1_3c * icon_same

    icon_4c = np.concatenate((icon_3c, icon_same * 255), axis=-1)
    icon_name = get_icon_name(icon_4c)

    return icon_name, icon_4c


def calculate_diff_average(im_4c: np.ndarray, im_4c1: np.ndarray):
    im = im_4c[:, :, 0:3]
    im_1 = im_4c1[:, :, 0:3]
    shield = (im_4c[:, :, [3]] // 255).astype(np.uint8)
    shield1 = (im_4c1[:, :, [3]] // 255).astype(np.uint8)

    shield_diff = shield ^ shield1
    shield_diff_sum = np.sum(shield_diff) * 100

    im_diff = np.abs(im.astype(np.int) - im_1.astype(np.int)).astype(np.uint8)
    im_diff *= np.bitwise_or(shield, shield1)
    im_diff_sum = np.sum(im_diff)

    average = (shield_diff_sum + im_diff_sum) / np.sum(shield)
    return average


if __name__ == '__main__':
    pass
