import os
import cv2
import numpy as np
from skimage.measure import label, regionprops

big_icon_dir = 'icon_templates/big_icon'


def calculate_diff_average(im_4c: np.ndarray, im_4c1: np.ndarray):
    im = im_4c[:, :, 0:3]
    im_1 = im_4c1[:, :, 0:3]
    shield = (im_4c[:, :, [3]] // 255).astype(np.uint8)
    shield1 = (im_4c1[:, :, [3]] // 255).astype(np.uint8)

    shield_diff = shield ^ shield1
    shield_diff_sum = np.sum(shield_diff) * 100

    im_diff = np.abs(im.astype(np.int) - im_1.astype(np.int)).astype(np.uint8)
    im_diff *= shield
    im_diff_sum = np.sum(im_diff)

    average = (shield_diff_sum + im_diff_sum) / np.sum(shield)
    return average


def get_icon_name(icon_4c):
    assert icon_4c.shape[2] == 4
    shield = icon_4c[:, :, 3]
    label_im = label(shield, connectivity=shield.ndim)
    props = regionprops(label_im)
    max_area = 0
    bbox = [0, 0, 0, 0]
    for prop in props:
        area = prop.area
        if area > max_area:
            max_area = area
            bbox = prop.bbox
    y1, x1, y2, x2 = bbox
    icon = icon_4c[y1:y2, x1:x2]
    icon_h, icon_w = icon.shape[0], icon.shape[1]

    min_average_diff = 1000000
    icon_name = ''
    for big_icon_name in os.listdir(big_icon_dir):
        big_icon = cv2.imread(os.path.join(big_icon_dir, big_icon_name), cv2.IMREAD_UNCHANGED)
        big_icon = cv2.resize(big_icon, (icon_w, icon_h))

        average_diff = calculate_diff_average(big_icon, icon)
        if average_diff < min_average_diff:
            min_average_diff = average_diff
            icon_name = big_icon_name

    return icon_name


if __name__ == '__main__':
    test_icon_path = 'icons/weapon1grip-451.png'
    test_icon = cv2.imread(test_icon_path, cv2.IMREAD_UNCHANGED)

    name = get_icon_name(test_icon)
    print(name)
