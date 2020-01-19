import numpy as np


def get_white_shield(im, min_rgb):
    shield_rgb = np.where(im > min_rgb, 255, 0)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield
