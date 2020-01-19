import os
import cv2
import numpy as np
import pytesseract

from screen_parameter import white_min_rgb, min_white_area
from all_states import all_guns
from calibrate_icons.get_position.position_constant import screen_white_position


def save_white_crop(im):
    os.makedirs('white_areas', exist_ok=True)
    for pos_name, rect in screen_white_position.items():
        y1, x1, y2, x2 = rect
        white_area = im[y1:y2, x1:x2]
        shield = get_white_shield(white_area, white_min_rgb)
        if np.sum(shield / 255) > min_white_area:
            area_name = get_white_name(shield)
            cv2.imwrite('white_areas/' + pos_name + '-' + area_name + '.png', shield)


def get_white_shield(im, min_rgb):
    shield_rgb = np.where(im > min_rgb, 255, 0).astype(np.uint8)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield


def get_white_name(shield):
    _shield = 255 - shield[:, :, np.newaxis]
    shield_rgb = np.concatenate((_shield, _shield, _shield), axis=-1)
    shield_name = pytesseract.image_to_string(shield_rgb)
    print(shield_name)
    for gun_name in all_guns:
        if gun_name in shield_name:
            return gun_name
    return shield_name


if __name__ == '__main__':
    im_dir = 'screen_white_areas'

    for im_name in os.listdir(im_dir):
        im = cv2.imread(os.path.join(im_dir, im_name))
        save_white_crop(im)
