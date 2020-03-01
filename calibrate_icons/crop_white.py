import numpy as np

from screen_parameter import white_min_rgb, min_white_rate
from calibrate_icons.gun_name_OCR import get_ocr_name


def crop_white(rect_im):
    shield = get_white_shield(rect_im, white_min_rgb)
    if np.sum(shield) > 255:
        shield_ocr = 255 - get_white_shield(rect_im, 190)
        ocr_name = get_ocr_name(shield_ocr)
        # cv2.imshow('', shield)
        # cv2.waitKey()
        return ocr_name, shield
    return '', None


def get_white_shield(im, min_rgb=white_min_rgb):
    shield_rgb = np.where(im > min_rgb, 255, 0).astype(np.uint8)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield


if __name__ == '__main__':
    pass