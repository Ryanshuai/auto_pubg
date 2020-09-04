import numpy as np


def get_white_shield(img, min_rgb=None):
    if min_rgb is None:
        rgb_equal = np.equal(img[:, :, 0], img[:, :, 1]) & np.equal(img[:, :, 0], img[:, :, 2])
        rgb_equal = rgb_equal.astype(np.uint8)[:, :, np.newaxis]
        white_img = rgb_equal * img
        min_rgb = np.max(white_img) - 5

    shield_rgb = np.where(img > min_rgb, 255, 0)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield


if __name__ == '__main__':
    import cv2

    img = cv2.imread("320.png")
    img_shield = get_white_shield(img)
