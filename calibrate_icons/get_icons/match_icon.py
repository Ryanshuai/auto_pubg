import os
import cv2
import numpy as np

from screen_parameter import min_icon_area
from calibrate_icons.get_position.position_constant import screen_icon_position


def save_icon(im0, im):
    os.makedirs('icons', exist_ok=True)
    for pos_name, rect in screen_icon_position.items():
        y1, x1, y2, x2 = rect
        icon0 = im0[y1:y2, x1:x2]
        icon = im[y1:y2, x1:x2]
        icon_diff = np.abs(icon.astype(np.int) - icon0.astype(np.int))
        icon_same = np.where(icon_diff == 0, 1, 0).astype(np.uint8)
        icon_same = icon_same[:, :, 0] & icon_same[:, :, 1] & icon_same[:, :, 2]
        if np.sum(icon_same) > min_icon_area:
            icon_same = icon_same[:, :, np.newaxis]
            icon_3c = icon * icon_same
            icon_name = get_icon_name(icon_3c)
            icon_4c = np.concatenate((icon_3c, icon_same * 255), axis=-1)
            cv2.imwrite('icons/' + pos_name + '-' + icon_name + '.png', icon_4c)


def get_icon_name(icon):
    rint = np.random.randint(0, 1000)
    return str(rint)


if __name__ == '__main__':
    im_dir1 = 'screen_icon1'
    im_dir2 = 'screen_icon2'

    for im_name1 in os.listdir(im_dir1):
        im1 = cv2.imread(os.path.join(im_dir1, im_name1))
        for im_name2 in os.listdir(im_dir2):
            im2 = cv2.imread(os.path.join(im_dir2, im_name2))
            save_icon(im1, im2)
